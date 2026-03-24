from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver
from src.agent.state import AgentState
from src.agent.nodes import call_llm
from src.config.settings import settings

def build_graph():
    conn = SqliteSaver.from_conn_string(settings.db_path)
    checkpointer = conn.__enter__()

    builder = StateGraph(AgentState)
    builder.add_node("llm", call_llm)
    builder.set_entry_point("llm")
    builder.add_edge("llm", END)
    return builder.compile(checkpointer=checkpointer)

agent = build_graph()