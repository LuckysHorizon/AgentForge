from types import SimpleNamespace

from fastapi.testclient import TestClient
import pytest

from app import config, main


client = TestClient(main.app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "service": "AgentForge",
    }


def test_chat_returns_text_usage_and_cost(monkeypatch):
    response = SimpleNamespace(
        choices=[
            SimpleNamespace(
                message=SimpleNamespace(content="Hello!")
            )
        ],
        usage=SimpleNamespace(
            prompt_tokens=3,
            completion_tokens=5,
            total_tokens=8,
        ),
    )
    monkeypatch.setattr(main, "call_llm", lambda **kwargs: response)

    result = client.post("/chat", json={"message": "Hi"})

    assert result.status_code == 200
    assert result.json() == {
        "text": "Hello!",
        "usage": {
            "input_tokens": 3,
            "output_tokens": 5,
            "total_tokens": 8,
        },
        "cost": round(
            3 * main.PRICE_INPUT / 1_000_000
            + 5 * main.PRICE_OUTPUT / 1_000_000,
            8,
        ),
    }


def test_chat_stream_emits_server_sent_events(monkeypatch):
    monkeypatch.setattr(main, "stream_llm", lambda **kwargs: iter(["Hello!"]))

    response = client.post("/chat/stream", json={"message": "Hi"})

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/event-stream")
    assert 'data: {"token": "Hello!"}' in response.text
    assert "data: [DONE]" in response.text


def test_structured_chat_returns_model_data(monkeypatch):
    monkeypatch.setattr(
        main,
        "generate_structured",
        lambda **kwargs: main.StudentInfo(name="Ada", age=36, skills=["Python"]),
    )

    response = client.post(
        "/chat/structured",
        json={"message": "Return student information"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "name": "Ada",
        "age": 36,
        "skills": ["Python"],
    }


def test_api_key_uses_generic_fallback(monkeypatch):
    monkeypatch.setattr(config, "PROVIDER", "groq")
    monkeypatch.setitem(config.API_KEYS, "groq", None)
    monkeypatch.setenv("LLM_API_KEY", "test-key")

    assert config.get_api_key() == "test-key"


def test_provider_specific_api_key_takes_precedence(monkeypatch):
    monkeypatch.setattr(config, "PROVIDER", "groq")
    monkeypatch.setitem(config.API_KEYS, "groq", "provider-key")
    monkeypatch.setenv("LLM_API_KEY", "generic-key")

    assert config.get_api_key() == "provider-key"


def test_model_rejects_unreplaced_placeholder(monkeypatch):
    monkeypatch.setattr(config, "MODEL", "groq/YOUR-MODEL-ID")

    with pytest.raises(ValueError, match="LLM_MODEL"):
        config.get_model()
