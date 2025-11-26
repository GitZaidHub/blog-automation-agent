import asyncio
from src.tools.websearch import WebSearchTool
from concurrent.futures import ThreadPoolExecutor

class ResearchAgent:
    def __init__(self, sessions, sid):
        self.sessions = sessions
        self.sid = sid
        self.tool = WebSearchTool()

    async def run_parallel_queries(self, payload):
        queries = [
            payload.get('brief', ''),
            f"background on {payload.get('title', '')}",
            f"recent developments {payload.get('title', '')}",
        ]
        tasks = [asyncio.create_task(self.tool.search(q)) for q in queries]
        results = await asyncio.gather(*tasks)
        citations = []
        for r in results:
            citations.extend(r[:3])
        # Deduplicate by url
        seen = set()
        filtered = []
        for c in citations:
            if c["url"] in seen:
                continue
            seen.add(c["url"])
            filtered.append(c)
        return filtered
