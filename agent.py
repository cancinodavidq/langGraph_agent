import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from typing import TypedDict, List
import os
from dotenv import load_dotenv
load_dotenv()  # lee el .env automáticamente

# 1. ESTADO — agrega aquí los campos que necesites
class AgentState(TypedDict):
    messages: List

# 2. MODELO — cambia modelo y temperature según el caso
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# 3. PERSONALIDAD — define aquí el rol del agente
SYSTEM_PROMPT = """
Eres un asistente especializado en historia.
-solo aporta información veridica.
"""

# 4. NODO PRINCIPAL — agrega más nodos según necesites
def call_llm(state: AgentState) -> AgentState:
    messages = state["messages"]
    response = llm.invoke(messages)
    return {"messages": messages + [response]}

# 5. GRAFO — agrega nodos y edges según el flujo
builder = StateGraph(AgentState)
builder.add_node("llm", call_llm)
builder.set_entry_point("llm")
builder.add_edge("llm", END)
agent = builder.compile()

# 6. LOOP — esto casi nunca cambia
if __name__ == "__main__":
    messages = [SystemMessage(content=SYSTEM_PROMPT)]
    
    while True:
        user_input = input("Tú: ")
        if user_input.lower() == "salir":
            break
        messages.append(HumanMessage(content=user_input))
        result = agent.invoke({"messages": messages})
        messages = result["messages"]
        print(f"Agente: {messages[-1].content}\n")