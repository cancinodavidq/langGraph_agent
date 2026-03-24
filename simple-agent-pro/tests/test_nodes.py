# tests/test_nodes.py

import pytest
import openai
from unittest.mock import patch
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage


class TestCallLlm:

    def test_respuesta_exitosa(self, mocker):
        # ARRANGE
        mocker.patch.object(
            ChatOpenAI,
            'invoke',
            return_value=AIMessage(content="respuesta de prueba")
        )
        state = {
            "messages": [HumanMessage(content="hola")],
            "error": None
        }

        # ACT
        from src.agent.nodes import call_llm
        resultado = call_llm(state)

        # ASSERT
        assert "messages" in resultado
        assert resultado["error"] is None
        assert isinstance(resultado["messages"][-1], AIMessage)
        assert resultado["messages"][-1].content == "respuesta de prueba"

    def test_rate_limit_error(self, mocker):
        # ARRANGE
        mocker.patch.object(
            ChatOpenAI,
            'invoke',
            side_effect=openai.RateLimitError(
                message="rate limit",
                response=mocker.Mock(status_code=429),
                body={}
            )
        )
        state = {
            "messages": [HumanMessage(content="hola")],
            "error": None
        }

        # ACT
        from src.agent.nodes import call_llm
        resultado = call_llm(state)

        # ASSERT
        assert resultado["error"] is not None
        assert "Rate limit" in resultado["error"]

    def test_agrega_system_message(self, mocker):
        # ARRANGE
        mocker.patch.object(
            ChatOpenAI,
            'invoke',
            return_value=AIMessage(content="respuesta")
        )
        state = {
            "messages": [HumanMessage(content="hola")],
            "error": None
        }

        # ACT
        from src.agent.nodes import call_llm
        resultado = call_llm(state)

        # ASSERT
        assert isinstance(resultado["messages"][0], SystemMessage)