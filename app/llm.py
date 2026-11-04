from litellm import completion

from app.config import(
    MODEL,
    get_api_key,
    PRICE_INPUT,
    PRICE_OUTPUT
)

from app.pricing import cost

def call_llm(messages:list) -> dict:
    
    api_key = get_api_key()

    response = completion(
        model = MODEL,
        messages=messages,
        api_key=api_key
    )

    text = response.choices[0].message.content

    usage_data = response.usage 

    usage = {
        "input_tokens": usage_data.prompt_tokens,
        "output_tokens": usage_data.completion_tokens,
        "total_tokens": usage_data.total_tokens
    } 

    total_cost = cost(
        usage,
        PRICE_INPUT,
        PRICE_OUTPUT
    )

    return {
        "text": text,
        "usage": usage,
        "cost": total_cost
    }