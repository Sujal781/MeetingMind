SUMMARIZE_PROMPT = """You are an expert meeting analyst. Given the transcript of a meeting, produce a clear, structured summary.

Format your response as:
**Meeting Overview**
[2-3 sentences capturing the essence of the meeting]

**Key Discussion Points**
- [Point 1]
- [Point 2]

**Decisions Made**
- [Decision 1]
(or "None recorded" if none)

Be concise. Do not add anything not mentioned in the transcript.

Transcript:
{transcript}
"""

EXTRACT_TASKS_PROMPT = """You are a project coordinator extracting action items from a meeting transcript.

Return a JSON array. Each item must have exactly these keys:
- "task": what needs to be done
- "owner": person responsible, or "Unassigned"
- "due": deadline, or "Not specified"

Return ONLY the JSON array, no other text.

Transcript:
{transcript}
"""

GENERATE_EMAIL_PROMPT = """You are a professional business writer. Write a follow-up email for this meeting.

Format exactly like this:

Subject: [subject line]

---

[email body]

Use the summary and action items below.

Meeting Summary:
{summary}

Action Items:
{tasks}
"""