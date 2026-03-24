🤖 Simple Agent Pro

Agente conversacional construido con LangGraph y OpenAI, desarrollado con arquitectura de producción desde cero.
Este proyecto demuestra las capacidades de diseño e implementación de sistemas agénticos en un ambiente empresarial real.


Autoría
Este proyecto fue diseñado, arquitecturado y codificado por David Cancino, Agent Architect con experiencia en construcción de sistemas de IA para producción.
La lógica de negocio, el diseño del estado, los nodos, el grafo, la configuración, el logging y la persistencia fueron escritos íntegramente por David. La sección de testing (tests/) fue construida con asistencia de Claude (Anthropic) debido a complejidades específicas de compatibilidad entre versiones de pytest-mock y langchain-openai.

Filosofía de desarrollo
Estos son los principios de arquitectura que aplico en todos mis proyectos:
Arquitectura primero, código después. Antes de escribir una línea de código se define la estructura completa del proyecto — carpetas, responsabilidades de cada módulo, contratos de datos. El estado (AgentState) es el diseño del sistema. Si no puedes definir el estado, no tienes claro el flujo.
Separación de responsabilidades. Cada archivo tiene una sola razón para cambiar. Los prompts no viven en la lógica. La configuración no vive en el código. Los nodos no saben nada del grafo que los contiene.
Fail fast. Si la configuración está mal, el sistema no arranca. Si una llamada a la API falla, el error queda registrado en el estado sin romper el grafo. Los problemas se detectan lo más temprano posible en el flujo.
Portabilidad desde el inicio. El agente corre en un contenedor Docker desde el primer día — no como un paso final, sino como parte del diseño base.

Qué construye este proyecto
Un agente conversacional con memoria persistente entre sesiones, manejo de errores en tres niveles, logging estructurado, testing unitario y pipeline de CI/CD automatizado.
No es un chatbot de tutorial. Es la base mínima viable de lo que cualquier empresa mediana pondría en producción.

Stack tecnológico
CapaTecnologíaModeloGPT-4o-mini (OpenAI)Framework de agentesLangGraphOrquestación LLMLangChainConfiguraciónPydantic SettingsPersistenciaSQLite via LangGraph SqliteSaverLoggingPython logging estándarTestingpytest + pytest-mockContenedorizaciónDocker + Docker ComposeCI/CDGitHub Actions

Arquitectura
simple-agent-pro/
├── main.py                      # punto de entrada
├── src/
│   ├── agent/
│   │   ├── state.py             # schema del estado — TypedDict
│   │   ├── prompts.py           # system prompts separados de la lógica
│   │   ├── nodes.py             # nodos del grafo con manejo de errores
│   │   └── graph.py             # construcción del grafo con persistencia
│   ├── config/
│   │   └── settings.py          # configuración centralizada con Pydantic
│   └── utils/
│       └── logger.py            # logger estructurado a pantalla y archivo
├── tests/
│   ├── test_nodes.py            # unit tests con mocks
│   └── test_graph.py            # integration tests
├── .github/
│   └── workflows/
│       └── ci.yml               # pipeline CI/CD automatizado
├── Dockerfile                   # multi-stage build
├── docker-compose.yml           # orquestación local
├── requirements.txt             # dependencias de producción
├── requirements-dev.txt         # dependencias de desarrollo
└── .env.example                 # plantilla de configuración

Las 6 etapas de construcción
Este proyecto se construyó en 6 etapas progresivas. Cada etapa agrega una capa de madurez sobre la anterior.
Etapa 1 — Estructura de carpetas
La arquitectura va primero. Se definió la estructura completa del proyecto antes de escribir una sola línea de código. Cada carpeta tiene una responsabilidad única e inamovible.
Etapa 2 — Agente base con manejo de errores
El núcleo del sistema. Tres decisiones de diseño clave:
El estado como contrato. AgentState define exactamente qué datos circulan por el grafo. El campo error: Optional[str] permite que los fallos queden registrados en el estado sin romper el flujo de ejecución — el grafo siempre termina de forma controlada.
Configuración centralizada. Settings con pydantic-settings garantiza que si falta una variable de entorno el sistema no arranca en vez de fallar silenciosamente más adelante. La API key usa SecretStr para que nunca aparezca en logs.
Manejo de errores en tres niveles. RateLimitError para cuotas excedidas, APIConnectionError para problemas de red, y Exception genérico para cualquier otro fallo inesperado.
Etapa 3 — Logging y observabilidad
Dos canales simultáneos — pantalla con nivel DEBUG para desarrollo, archivo agent.log con nivel INFO para producción. El formato incluye timestamp, nivel, módulo de origen y mensaje en cada línea.
2026-03-24 12:27:34 | INFO | nodes | Llamando al LLM con 2 mensajes
2026-03-24 12:27:37 | INFO | nodes | Respuesta recibida correctamente
Etapa 4 — Testing
Tests unitarios con mocks para los tres escenarios críticos del nodo principal — respuesta exitosa, rate limit error, y verificación de inyección automática del SystemMessage. Los mocks reemplazan las llamadas reales a OpenAI para que los tests sean rápidos, determinísticos y sin costo.

Esta sección fue construida con asistencia de Claude (Anthropic) por incompatibilidades entre versiones de pytest-mock y langchain-openai.

Etapa 5 — Persistencia básica
SqliteSaver de LangGraph guarda el estado del grafo en disco después de cada nodo. Cada conversación tiene un thread_id único — si el proceso se cae, se puede retomar desde el último checkpoint con el mismo ID.
pythonconfig = {"configurable": {"thread_id": thread_id}}
agent.invoke(state, config=config)
Etapa 6 — Docker y CI/CD
Multi-stage Dockerfile — etapa builder para instalar dependencias, etapa production con solo lo necesario para correr. Imagen limpia, mínima y sin herramientas de desarrollo.
GitHub Actions — en cada push a main el pipeline corre los tests automáticamente. Si alguno falla, el merge se bloquea. Si pasan, construye la imagen Docker.

Instalación y uso
Requisitos

Python 3.11+
Docker Desktop
API Key de OpenAI

Setup local
bashgit clone https://github.com/TU-USUARIO/simple-agent-pro.git
cd simple-agent-pro

# crea el archivo de configuración
cp .env.example .env
# edita .env con tu API key

# instala dependencias
pip install -r requirements.txt

# corre el agente
python3.11 main.py
Con Docker
bashdocker compose up
Tests
bashpip install -r requirements-dev.txt
pytest tests/ -v

Variables de entorno
VariableRequeridaDefaultDescripciónOPENAI_API_KEY✅—API Key de OpenAIMODEL_NAME❌gpt-4o-miniModelo a usarTEMPERATURE❌0.7Creatividad del modelo (0-2)MAX_TOKENS❌1000Máximo de tokens por respuestaAGENT_NAME❌simple-agentNombre del agenteDB_PATH❌agent_memory.dbRuta del archivo SQLite

Flujo de ejecución
Usuario escribe mensaje
        ↓
HumanMessage agregado al estado
        ↓
agent.invoke(state, config)
        ↓
  ┌─────────────────────┐
  │     Nodo: llm       │
  │  agrega SystemMsg   │
  │  llama a OpenAI     │
  │  maneja errores     │
  └─────────────────────┘
        ↓
LangGraph guarda estado en SQLite
        ↓
¿error en estado?
    sí → mostrar error
    no → mostrar respuesta
        ↓
while True → siguiente mensaje

Roadmap de patrones
Este proyecto es el patrón 1 de 10 en mi roadmap personal de arquitectura de agentes:
#PatrónEstado1Simple LLM con capas de producción✅ Completado2Reflection Pattern✅ Completado3Tool Calling🔄 En progreso4ReAct⏳ Pendiente5Router⏳ Pendiente6Parallelization⏳ Pendiente7Human in the Loop⏳ Pendiente8RAG Agent⏳ Pendiente9Multi-Agent⏳ Pendiente10Self-Healing Code⏳ Pendiente

Licencia
MIT — construido para aprender, compartir y escalar.
