import asyncio
import uuid
import os
import logging
import time
from src.sessions.session_service import SessionService
from src.sessions.memory import Memory
from src.agents.research_agent import ResearchAgent
from src.agents.draft_agent import DraftAgent
from src.agents.editor_agent import EditorAgent
from src.agents.seo_agent import SEOAgent
from src.agents.publisher_agent import PublisherAgent
from src.eval.evaluator import evaluate_text

logger = logging.getLogger(__name__)

class Orchestrator:
    def __init__(self):
        self.sessions = SessionService()  # persistent session backed by sqlite
        self._locks = {}

    async def start_workflow(self, payload: dict):
        session_id = str(uuid.uuid4())
        self.sessions.create_session(session_id, payload)
        
        # Initialize memory for this session (optional, just to ensure logs exist)
        mem = Memory(self.sessions, session_id)
        mem.append_log("Workflow started", source="orchestrator")
        
        task = asyncio.create_task(self._run(session_id))
        self.sessions.set_task(session_id, task)
        logger.info(f'{{"event":"workflow_started","session": "{session_id}"}}')
        return session_id

    async def _run(self, sid: str):
        try:
            payload = self.sessions.get_session_payload(sid)
            # Research (parallel)
            research = ResearchAgent(self.sessions, sid)
            citations = await research.run_parallel_queries(payload)
            self.sessions.update(sid, {"citations": citations})
            await self._checkpoint_pause(sid)

            # Draft
            draft_agent = DraftAgent(self.sessions, sid)
            draft = await draft_agent.create_draft(payload, citations)
            self.sessions.update(sid, {"draft": draft})
            self._save_to_file(sid, "draft.md", draft)
            await self._checkpoint_pause(sid)

            # Edit
            editor = EditorAgent(self.sessions, sid)
            edited = await editor.edit(draft)
            self.sessions.update(sid, {"edited": edited})
            self._save_to_file(sid, "edited.md", edited)
            await self._checkpoint_pause(sid)

            # SEO
            seo = SEOAgent(self.sessions, sid)
            seo_report = await seo.analyze(edited)
            self.sessions.update(sid, {"seo": seo_report})
            await self._checkpoint_pause(sid)

            # Evaluate
            eval_result = evaluate_text(edited, citations)
            self.sessions.update(sid, {"evaluation": eval_result})

            # Publish (simulated or actual)
            publisher = PublisherAgent(self.sessions, sid)
            published = await publisher.publish(edited, payload)
            self.sessions.update(sid, {"published": published})

            self.sessions.set_state(sid, "completed")
            logger.info(f'{{"event":"workflow_completed","session":"{sid}"}}')
        except asyncio.CancelledError:
            self.sessions.set_state(sid, "cancelled")
            logger.info(f'{{"event":"workflow_cancelled","session":"{sid}"}}')
            raise
        except Exception as e:
            logger.exception(f"Workflow {sid} failed: {e}")
            self.sessions.set_state(sid, "failed")
            self.sessions.update(sid, {"error": str(e)})

    async def _checkpoint_pause(self, sid: str):
        """If session has pause flag, wait until resume."""
        s = self.sessions.get_session(sid)
        if s.get("paused"):
            logger.info(f'{{"event":"paused","session":"{sid}"}}')
        while s.get("paused"):
            await asyncio.sleep(0.5)
            s = self.sessions.get_session(sid)

    async def get_status(self, sid: str):
        return self.sessions.get_status(sid)

    def _save_to_file(self, sid: str, filename: str, content: str):
        """Helper to save content to a file in the outputs directory."""
        try:
            output_dir = os.path.join("outputs", sid)
            os.makedirs(output_dir, exist_ok=True)
            filepath = os.path.join(output_dir, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            logger.info(f"Saved {filename} to {filepath}")
        except Exception as e:
            logger.error(f"Failed to save {filename} for session {sid}: {e}")
