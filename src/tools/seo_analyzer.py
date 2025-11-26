import asyncio
from textstat import flesch_reading_ease

class SEOAnalyzer:
    async def run(self, text: str):
        await asyncio.sleep(0.05)
        wc = len(text.split())
        readability = flesch_reading_ease(text)
        score = min(100, max(0, 40 + (wc - 600)/10))  # heuristic
        notes = []
        if wc < 500:
            notes.append("Under 500 words")
        return {"word_count": wc, "readability": readability, "score": score, "notes": notes}
