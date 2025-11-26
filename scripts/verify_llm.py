import asyncio
import os
from dotenv import load_dotenv

# Force reload of env vars for this script
load_dotenv(override=True)

from src.llm_client import LLMClient

async def main():
    print(f"Testing LLM with model: {os.getenv('GEMINI_MODEL')}")
    client = LLMClient()
    try:
        result = await client.complete("Hello, are you working?", max_tokens=50)
        print("LLM Result:", result)
    except Exception as e:
        print("LLM Failed:", e)

if __name__ == "__main__":
    asyncio.run(main())
