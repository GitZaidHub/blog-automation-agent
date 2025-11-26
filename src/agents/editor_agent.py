# src/agents/editor_agent.py
from src.llm_client import LLMClient
from src.prompt_templates import editor_prompt
import logging

logger = logging.getLogger(__name__)

class EditorAgent:
    def __init__(self, sessions, sid):
        self.sessions = sessions
        self.sid = sid
        self.llm = LLMClient()

    async def edit(self, draft_text: str):
        """
        Use editor_prompt to ask the LLM to edit the draft.
        Persist the edited draft to session under key 'edited'.
        """
        try:
            prompt = editor_prompt(draft_text)
            edited = await self.llm.complete(prompt, max_tokens=4000, temperature=0.1)
            # Save edited result into session store
            self.sessions.update(self.sid, {"edited": edited})
            return edited
        except Exception as e:
            logger.exception("EditorAgent failed for session %s: %s", self.sid, e)
            self.sessions.update(self.sid, {"edited_error": str(e)})
            return f"[ERROR editing draft: {e}]"
