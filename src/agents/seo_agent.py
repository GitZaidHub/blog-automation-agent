from src.tools.seo_analyzer import SEOAnalyzer

class SEOAgent:
    def __init__(self, sessions, sid):
        self.sessions = sessions
        self.sid = sid
        self.analyzer = SEOAnalyzer()

    async def analyze(self, text: str):
        return await self.analyzer.run(text)
