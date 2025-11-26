# src/llm_client.py
import os
import aiohttp
import asyncio
import logging
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

logger = logging.getLogger(__name__)

# --- Configuration ---
LLM_MODE = os.getenv("LLM_MODE", "demo").lower()  # "demo" or "gemini"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
# Default to Flash as it is free and fast
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
LLM_TIMEOUT = int(os.getenv("LLM_TIMEOUT", "60"))  # seconds

class LLMClient:
    def __init__(self):
        self.mode = LLM_MODE
        
        # specific check for Gemini mode
        if self.mode == "gemini" and not GEMINI_API_KEY:
            logger.warning("LLM_MODE=gemini but GEMINI_API_KEY is empty — falling back to demo mode.")
            self.mode = "demo"

    @retry(wait=wait_exponential(min=1, max=10), stop=stop_after_attempt(3), retry=retry_if_exception_type(Exception))
    async def complete(self, prompt: str, max_tokens: int = 4000, temperature: float = 0.2) -> str:
        """
        Return a text completion (string). 
        Uses Google Gemini API via REST when LLM_MODE=gemini.
        """
        # --- 1. DEMO MODE ---
        if self.mode == "demo":
            await asyncio.sleep(0.2)
            return f"[DEMO LLM OUTPUT]\n\n{prompt[:300]}"

        # --- 2. GEMINI MODE ---
        # Construct the URL for the specific model
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
        
        headers = {"Content-Type": "application/json"}
        
        # Gemini uses "contents" -> "parts" structure, not "messages"
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": float(temperature),
                "maxOutputTokens": int(max_tokens)
            }
        }

        timeout = aiohttp.ClientTimeout(total=LLM_TIMEOUT)
        
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(url, headers=headers, json=payload) as resp:
                text = await resp.text()
                
                if resp.status >= 400:
                    logger.error("LLM API error status=%s, body=%s", resp.status, text[:1000])
                    raise Exception(f"LLM API error {resp.status}: {text}")
                
                data = await resp.json()
                
                # Defensive path: Parse Gemini Response
                try:
                    # Gemini structure: candidates[0].content.parts[0].text
                    return data["candidates"][0]["content"]["parts"][0]["text"]
                except (KeyError, IndexError) as e:
                    # Sometimes Gemini blocks content (safety settings) and returns no candidates
                    logger.exception("Unexpected Gemini response shape or Safety Block: %s", data)
                    # Fallback or detailed error
                    if "promptFeedback" in data:
                        return f"Error: Content blocked by safety filters. Details: {data['promptFeedback']}"
                    return text