from src.llm_client import LLMClient
from textwrap import dedent
import asyncio

class DraftAgent:
    def __init__(self, sessions, sid):
        self.sessions = sessions
        self.sid = sid
        self.llm = LLMClient()

    async def create_draft(self, payload, citations):
        title = payload.get("title", "Untitled")
        audience = payload.get("audience", "general")
        brief = payload.get("brief", "")
        citations_text = "\n".join([f"- [{i+1}] {c['title']} ({c['url']})" for i, c in enumerate(citations)])
        prompt = dedent(f"""
        You are a professional blog writer. Write a long-form, research-driven blog post.

        Title: {title}
        Audience: {audience}
        Brief: {brief}

        Use the following citations where appropriate. Insert inline citation markers like [1], [2].
        Citations:
        {citations_text}

        Structure:
        - Short intro (hook + thesis)
        - 3-6 sections with H2 headings and H3 subheads as needed
        - Conclusion and 3 actionable takeaways
        - At the end include a References section that enumerates the citations.

        Tone: helpful, instructive, concise.
        """)
        resp = await self.llm.complete(prompt, max_tokens=4000)
        return resp
