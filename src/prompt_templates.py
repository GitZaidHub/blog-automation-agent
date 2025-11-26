# src/prompt_templates.py
from textwrap import dedent

def draft_prompt(title: str, audience: str, brief: str, citations_text: str) -> str:
    return dedent(f"""
    You are a professional blog writer. Write a long-form, research-driven blog post that is factual and cites sources inline.

    Title: {title}
    Audience: {audience}
    Brief: {brief}

    Use the following citations where appropriate. Insert inline citation markers like [1], [2] and ensure every factual claim that can be cited includes at least one marker.
    Citations:
    {citations_text}

    Requirements:
    - Short intro (hook + thesis)
    - 4-8 sections with clear H2 headings, include H3 subheads where helpful
    - Use examples, short code blocks (if relevant), or bullet lists for actionable steps
    - Conclusion with 3 actionable takeaways
    - At the end include a "References" section that lists each citation in order with title and URL
    - Keep tone: helpful, instructive, developer-friendly

    Length: aim for 900-1500 words for long-form content unless brief specifies otherwise.
    """)

def editor_prompt(draft_text: str) -> str:
    return dedent(f"""
    You are an expert editor. Improve the following draft for clarity, grammar, tone, and structure.
    - Keep the author's meaning and citations intact
    - Fix grammar and awkward phrasing
    - Reorganize sections if it improves flow (keep section headings)
    - Identify any unverifiable claims and flag them with [VERIFY]
    - Return the edited draft only (no commentary)

    Draft:
    {draft_text}
    """)
