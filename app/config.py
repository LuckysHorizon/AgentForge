import os
from dotenv import load_dotenv
load_dotenv()

PROVIDER = os.getenv("LLM_PROVIDER","groq").lower()

MODEL = os.getenv(
    "LLM_MODEL",
    "groq/your-model-id"
)

API_KEYS = {
    "openai": os.getenv("OPENAI_API_KEY"),
    "groq": os.getenv("GROQ_API_KEY"),
    "anthropic": os.getenv("ANTHROPIC_API_KEY"),
}

PRICE_INPUT = float(
    os.getenv("PRICE_INPUT_PER_MILLION", "0")
)

PRICE_OUTPUT = float(
    os.getenv("PRICE_OUTPUT_PER_MILLION", "0")
)

def get_api_key():
    if PROVIDER not in API_KEYS:
        raise ValueError(
            f"unsupported provider: {PROVIDER}"
        )
    api_key = API_KEYS[PROVIDER]

    if not api_key:
        raise ValueError(
            f"Missing API key for {PROVIDER}"
        )
    return api_key