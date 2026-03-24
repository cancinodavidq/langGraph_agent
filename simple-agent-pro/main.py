from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from src.agent.graph import agent
import uuid
from src.utils.logger import logger

load_dotenv()

if __name__ == "__main__":
    print("🤖 Agente listo. Escribe 'salir' para terminar.\n")

    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    logger.info(f"sesión inciada con thread_id:{thread_id}")
    
    state = {
        "messages": [],
        "error": None
    }

    while True:
        user_input = input("Tú: ")
        if user_input.lower() == "salir":
            break

        state["messages"].append(HumanMessage(content=user_input))
        
        result = agent.invoke(state)
        state = result

        if state["error"]:
            print(f"❌ Error: {state['error']}\n")
        else:
            print(f"Agente: {state['messages'][-1].content}\n")