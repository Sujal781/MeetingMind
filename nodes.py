import json
import re
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from prompts import SUMMARIZE_PROMPT, EXTRACT_TASKS_PROMPT, GENERATE_EMAIL_PROMPT


def get_llm(temperature=0.3):
    return ChatOpenAI(model="gpt-4o-mini", temperature=temperature)


def summarize_node(state: dict) -> dict:
    llm = get_llm(temperature=0.3)
    prompt = SUMMARIZE_PROMPT.format(transcript=state["transcript"])
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"summary": response.content}


def extract_tasks_node(state: dict) -> dict:
    llm = get_llm(temperature=0.1)
    prompt = EXTRACT_TASKS_PROMPT.format(transcript=state["transcript"])
    response = llm.invoke([HumanMessage(content=prompt)])

    raw = response.content.strip()
    # Strip markdown code fences if GPT wraps output in ```json ... ```
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)

    try:
        tasks = json.loads(raw)
        if not isinstance(tasks, list):
            tasks = []
    except json.JSONDecodeError:
        tasks = []

    return {"tasks": tasks}


def generate_email_node(state: dict) -> dict:
    llm = get_llm(temperature=0.4)

    tasks = state.get("tasks", [])
    if tasks:
        tasks_text = "\n".join(
            f"- {t.get('task','')} (Owner: {t.get('owner','Unassigned')}, Due: {t.get('due','Not specified')})"
            for t in tasks
        )
    else:
        tasks_text = "No action items identified."

    prompt = GENERATE_EMAIL_PROMPT.format(
        summary=state.get("summary", ""),
        tasks=tasks_text,
    )
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"email": response.content}