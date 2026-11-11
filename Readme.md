# AgentForge

**A provider-agnostic LLM integration framework built with Python, FastAPI, and LiteLLM.**

AgentForge provides a unified interface for integrating multiple Large Language Model (LLM) providers, including OpenAI, Groq, and Anthropic.

It abstracts provider-specific API implementations, allowing developers to switch between supported LLM providers through environment configuration without modifying application logic.

The project also provides token counting, usage tracking, and token-based cost estimation.

## Features

- **Multi-provider support:** Integrate OpenAI, Groq, Anthropic, and other LiteLLM-supported providers.
- **Unified LLM interface:** Interact with different providers through a common function.
- **Provider configuration:** Switch providers and models using environment variables.
- **REST API:** Expose LLM functionality through FastAPI endpoints.
- **Request validation:** Validate API requests using Pydantic.
- **Tokenization:** Count tokens in natural language, source code, and non-English text.
- **Usage tracking:** Track input, output, and total token consumption.
- **Cost estimation:** Calculate estimated API costs based on token usage and model pricing.
- **Environment-based configuration:** Manage API credentials securely outside the source code.
- **Automated testing:** Support unit and API testing using Pytest.

## Architecture

```text
                    Client
                      |
                      v
                FastAPI Backend
                      |
          +-----------+-----------+
          |           |           |
          v           v           v
        /health      /echo       /chat
                                  |
                                  v
                         AgentForge LLM Layer
                                  |
                                  v
                           call_llm()
                                  |
                                  v
                               LiteLLM
                                  |
              +-------------------+-------------------+
              |                   |                   |
              v                   v                   v
            OpenAI               Groq              Anthropic
              |                   |                   |
              +-------------------+-------------------+
                                  |
                                  v
                           LLM Response
                                  |
                    +-------------+-------------+
                    |             |             |
                    v             v             v
                   Text         Usage          Cost
```

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| FastAPI | REST API framework |
| LiteLLM | Unified LLM provider integration |
| Pydantic | Data validation and serialization |
| tiktoken | Token counting |
| python-dotenv | Environment variable management |
| Uvicorn | ASGI server |
| Pytest | Automated testing |

## Project Structure

```text
agentforge/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── schemas.py
│   ├── llm.py
│   ├── pricing.py
│   └── tokenization.py
│
├── tests/
│   ├── test_health.py
│   ├── test_echo.py
│   └── test_pricing.py
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.10 or later
- Git
- uv or pip
- An API key from a supported LLM provider

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/YOUR_USERNAME/agentforge.git

cd agentforge
```

**2. Create a virtual environment**

Using uv:

```bash
uv venv
```

Activate the environment.

Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Linux and macOS:

```bash
source .venv/bin/activate
```

**3. Install dependencies**

```bash
uv pip install -r requirements.txt
```

**4. Configure environment variables**

Create a `.env` file in the project root.

```env
# LLM Provider Configuration
LLM_PROVIDER=groq
LLM_MODEL=groq/your-model-id
LLM_API_KEY=your_api_key

# Model Pricing (USD per 1 million tokens)
PRICE_INPUT_PER_MILLION=0.10
PRICE_OUTPUT_PER_MILLION=0.50
```

Replace the placeholder values with the appropriate provider, model identifier, API key, and pricing.
`LLM_API_KEY` is used when the selected provider's specific key is not set.

## Supported LLM Providers

AgentForge uses LiteLLM to provide a common interface for supported LLM providers.

### Groq

```env
LLM_PROVIDER=groq
LLM_MODEL=groq/your-model-id
LLM_API_KEY=your_groq_api_key
```

### OpenAI

```env
LLM_PROVIDER=openai
LLM_MODEL=openai/your-model-id
LLM_API_KEY=your_openai_api_key
```

### Anthropic

```env
LLM_PROVIDER=anthropic
LLM_MODEL=anthropic/your-model-id
LLM_API_KEY=your_anthropic_api_key
```

Provider switching requires updating the provider, model identifier, and corresponding API key.

Refer to the [LiteLLM documentation](https://docs.litellm.ai/) for supported providers and model identifiers.

## Running the Application

Start the development server:

```bash
uvicorn app.main:app --reload
```

The application runs at:

```text
http://127.0.0.1:8000
```

API documentation:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## API Reference

### Health Check

**Endpoint:** `GET /health`

Checks application availability.

Example response:

```json
{
  "status": "healthy",
  "service": "AgentForge"
}
```

### Echo

**Endpoint:** `POST /echo`

Accepts a message and returns the same message.

Request:

```json
{
  "message": "Hello AgentForge"
}
```

Response:

```json
{
  "message": "Hello AgentForge"
}
```

### Chat

**Endpoint:** `POST /chat`

Sends a user message to the configured LLM provider and returns the generated response, token usage, and estimated cost.

Request:

```json
{
  "message": "Explain tokenization in simple terms."
}
```

Example response:

```json
{
  "text": "Tokenization is the process of splitting text into smaller units called tokens.",
  "usage": {
    "input_tokens": 12,
    "output_tokens": 14,
    "total_tokens": 26
  },
  "cost": 0.000009
}
```

Response values are illustrative. Actual values depend on the selected provider and model.

## Core Concepts

### Tokenization

Tokenization converts input text into smaller units called tokens.

AgentForge uses `tiktoken` to demonstrate token counting.

```python
import tiktoken

encoding = tiktoken.get_encoding("cl100k_base")

text = "Understanding Large Language Models"

tokens = encoding.encode(text)

print("Token IDs:", tokens)
print("Token Count:", len(tokens))
```

Tokenization can be tested using:

- English sentences
- Programming code
- Non-English sentences

Note: Tokenization differs between models and providers. `tiktoken` is used for learning and estimation, not as a universal billing counter.

### Context Windows

A context window represents the maximum amount of token-based context a model can process in a request.

It is relevant when working with:

- Long conversations
- Large documents
- Source code analysis
- Retrieval-Augmented Generation (RAG)

### Token-Based Pricing

LLM providers commonly calculate API costs based on input and output token consumption.

AgentForge estimates costs using the following formula:

```text
Total Cost =
    (Input Tokens / 1,000,000) * Input Price
  + (Output Tokens / 1,000,000) * Output Price
```

Pricing is configured through environment variables and should match the selected model's actual provider pricing.

## Testing

Run the automated test suite:

```bash
pytest -v
```

Testing should cover:

- Health endpoint
- Echo endpoint
- Request validation
- Error handling
- Token counting
- Cost calculation
- LLM integration using mocked provider responses

Live provider integration tests require valid API credentials and may incur API charges.

## Configuration Reference

| Variable | Description |
|---|---|
| `LLM_PROVIDER` | Selected LLM provider |
| `LLM_MODEL` | Provider-specific model identifier |
| `LLM_API_KEY` | Optional fallback API credential; provider-specific keys take precedence |
| `OPENAI_API_KEY`, `GROQ_API_KEY`, `ANTHROPIC_API_KEY` | Provider-specific API credentials |
| `PRICE_INPUT_PER_MILLION` | Input price per million tokens |
| `PRICE_OUTPUT_PER_MILLION` | Output price per million tokens |

## Security Considerations

- Do not commit API keys or `.env` files.
- Maintain a sanitized `.env.example`.
- Never expose provider credentials to frontend applications.
- Validate all incoming requests.
- Avoid logging sensitive user data or API credentials.
- Apply authentication and rate limiting before public deployment.
- Store production credentials using secure environment configuration.

## Roadmap

### Milestone 1: Multi-Provider LLM Foundation

- [ ] Initialize project structure and development environment.
- [ ] Implement FastAPI health and echo endpoints.
- [ ] Implement consistent JSON error responses.
- [ ] Integrate LiteLLM.
- [ ] Support OpenAI, Groq, and Anthropic.
- [ ] Implement token counting.
- [ ] Implement token-based cost calculation.
- [ ] Build the unified `call_llm(messages)` interface.
- [ ] Implement the `/chat` endpoint.
- [ ] Add automated tests.
- [ ] Document installation and usage.

### Future Enhancements

- [ ] Streaming responses
- [ ] Conversation history management
- [ ] Context window management
- [ ] Prompt templates
- [ ] Retrieval-Augmented Generation (RAG)
- [ ] Vector database integration
- [ ] Model fallback and retry mechanisms
- [ ] Logging and observability
- [ ] Docker support
- [ ] Authentication and rate limiting

## Contributing

Contributions are welcome.

To contribute:

1. Fork the repository.
2. Create a feature branch.
3. Implement your changes.
4. Add or update tests.
5. Commit your changes.
6. Push your branch.
7. Open a Pull Request.

Example:

```bash
git checkout -b feature/your-feature

git add .

git commit -m "feat: add your feature"

git push origin feature/your-feature
```

## References

- [LiteLLM Documentation](https://docs.litellm.ai/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [tiktoken](https://github.com/openai/tiktoken)
- [Groq Documentation](https://console.groq.com/docs)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Anthropic Documentation](https://docs.anthropic.com/)

## License

This project is intended to be released under the MIT License. See the `LICENSE` file for details.

---

**AgentForge** is an open-source learning project focused on building a reusable, provider-agnostic foundation for LLM-powered applications.