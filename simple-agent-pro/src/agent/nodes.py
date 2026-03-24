from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from src.agent.state import AgentState
from src.agent.prompts import SYSTEM_PROMPT
from src.config.settings import settings
from src.utils.logger import logger

import openai

llm = ChatOpenAI(
    api_key = settings.openai_api_key.get_secret_value(),
    model = settings.model_name,
    temperature = settings.temperature,
    max_tokens = settings.max_tokens
)

def call_llm(state: AgentState) -> AgentState:
    messages= state["messages"]

    if not messages or not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages
    logger.info(f"LLamando al LLm con {len(messages)}")

    try:
        response =llm.invoke(messages)
        logger.info(f"exitosamente conectado a la API")
        return {"messages": messages + [response], "error" :None}
    except openai.RateLimitError as e:
        logger.error(f"rate limit excedido: {str[e]}")
        return {"error": f"Rate limit excedido: {str(e)}"}
    except openai.APIConnectionError as e:
        logger.error(f"rerror de conexion: {str[e]}")
        return {"error": f"Error de conexion: {str(e)}"}
    except Exception as e:
        logger.error(f"error generico malparido: {str[e]}")
        return {"error": f"error inesperado: {str(e)}"}
    