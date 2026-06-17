from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from nodes import summarize_node, extract_tasks_node, generate_email_node


class MeetingState(TypedDict, total=False):
    transcript: str
    summary: str
    tasks: List[dict]
    email: str


def build_graph():
    builder = StateGraph(MeetingState)

    builder.add_node("summarize", summarize_node)
    builder.add_node("extract_tasks", extract_tasks_node)
    builder.add_node("generate_email", generate_email_node)

    builder.set_entry_point("summarize")
    builder.add_edge("summarize", "extract_tasks")
    builder.add_edge("extract_tasks", "generate_email")
    builder.add_edge("generate_email", END)

    return builder.compile()


def run_pipeline(transcript: str) -> dict:
    graph = build_graph()
    return graph.invoke({"transcript": transcript})