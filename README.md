🤖 Mi Primer Agente con LangGraph

Proyecto educativo para personas técnicas que están empezando con agentes de IA.
El objetivo es entender los conceptos fundamentales de LangGraph construyendo el agente más simple posible.


¿Qué vas a aprender?

Qué es un agente de IA y cómo funciona
Qué es LangGraph y por qué usarlo
Cómo estructurar un estado, un nodo y un grafo
Cómo conectar un LLM (GPT-4o-mini) a un flujo de ejecución
Cómo mantener historial de conversación manualmente


¿Qué NO cubre este proyecto?
Este proyecto es intencionalmente mínimo. No incluye:

Herramientas externas (búsqueda web, bases de datos, APIs)
Memoria persistente entre sesiones
Flujos condicionales
Multi-agente
Deploy a producción

Esos temas son el siguiente paso natural una vez domines esta base.

Requisitos previos
RequisitoVersión mínimaPython3.8+Cuenta en OpenAICon créditos disponiblesConocimiento de PythonBásico (funciones, clases, listas)

Instalación
1. Clona el repositorio
bashgit clone https://github.com/TU-USUARIO/mi-primer-agente.git
cd mi-primer-agente
2. Crea y activa un entorno virtual (opcional pero recomendado)
bashpython3 -m venv venv

# Mac / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
3. Instala las dependencias
bashpip install langgraph langchain langchain-openai python-dotenv
4. Configura tu API Key
Crea un archivo .env en la raíz del proyecto:
OPENAI_API_KEY=sk-proj-aqui-va-tu-key

⚠️ Nunca subas el archivo .env a Git. Ya está incluido en el .gitignore.


Uso
bashpython3 agent.py
Verás esto en la terminal:
🤖 Agente listo. Escribe 'salir' para terminar.

Tú:
Escribe lo que quieras. Para terminar la sesión escribe salir.

Estructura del proyecto
mi-primer-agente/
├── agent.py        # Código principal del agente
├── .env            # API Key (no se sube a Git)
├── .gitignore      # Archivos ignorados por Git
└── README.md       # Este archivo

Cómo funciona
El agente sigue este flujo en cada turno de conversación:
Usuario escribe un mensaje
        ↓
Se agrega como HumanMessage al historial
        ↓
El grafo arranca con el historial completo
        ↓
  ┌─────────────┐
  │  Nodo: llm  │  → llama a OpenAI con todo el historial
  └─────────────┘
        ↓
Se agrega la respuesta como AIMessage al historial
        ↓
Se imprime la respuesta en pantalla
        ↓
Vuelve a esperar input del usuario
Los 3 conceptos clave de LangGraph
Estado (AgentState)
Es el objeto que viaja entre todos los nodos del grafo. En este proyecto solo tiene una key: messages, que acumula todo el historial de la conversación.
Nodo (call_llm)
Una función que recibe el estado, hace algo con él, y retorna los cambios. En este proyecto solo hay un nodo que llama al LLM con el historial completo.
Grafo (StateGraph)
El mapa que conecta los nodos y define el orden de ejecución. En este proyecto el grafo es lineal: entrada → nodo llm → fin.

El código completo
pythonimport os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from typing import TypedDict, List

load_dotenv()

class AgentState(TypedDict):
    messages: List

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

SYSTEM_PROMPT = "Eres un asistente útil y conciso. Responde siempre en español."

def call_llm(state: AgentState) -> AgentState:
    messages = state["messages"]
    response = llm.invoke(messages)
    return {"messages": messages + [response]}

builder = StateGraph(AgentState)
builder.add_node("llm", call_llm)
builder.set_entry_point("llm")
builder.add_edge("llm", END)
agent = builder.compile()

if __name__ == "__main__":
    print("🤖 Agente listo. Escribe 'salir' para terminar.\n")
    messages = [SystemMessage(content=SYSTEM_PROMPT)]

    while True:
        user_input = input("Tú: ")
        if user_input.lower() == "salir":
            break
        messages.append(HumanMessage(content=user_input))
        result = agent.invoke({"messages": messages})
        messages = result["messages"]
        print(f"Agente: {messages[-1].content}\n")

Errores comunes
ErrorCausaSoluciónModuleNotFoundErrorDependencias no instaladasCorre pip install de nuevo con el venv activoAuthenticationErrorAPI Key incorrecta o no configuradaVerifica el archivo .envRateLimitErrorSin créditos en OpenAIAgrega créditos en platform.openai.com/billingEl agente no recuerda nadaReiniciaste el scriptEl historial solo vive en memoria durante la sesión

¿Qué sigue?
Una vez que entiendas este proyecto, los siguientes pasos naturales son:

Agregar herramientas — que el agente pueda buscar en Google, leer archivos o consultar una BD
Flujos condicionales — que el agente decida dinámicamente qué hacer
Memoria persistente — guardar el historial entre sesiones con SQLite o Redis
Multi-agente — varios grafos coordinados para tareas complejas


Recursos

Documentación oficial de LangGraph
Documentación de LangChain
API Reference de OpenAI


Licencia
MIT — úsalo, modifícalo y compártelo libremente.
