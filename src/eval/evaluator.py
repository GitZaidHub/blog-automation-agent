from textstat import flesch_reading_ease
import re

def evaluate_text(text: str, citations: list):
    readability = flesch_reading_ease(text)
    paragraphs = max(1, len(re.split(r'\n\s*\n', text)))
    citation_ratio = len(citations) / paragraphs
    return {"readability": readability, "citation_ratio": citation_ratio, "num_citations": len(citations)}
