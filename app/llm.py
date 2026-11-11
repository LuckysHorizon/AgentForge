from litellm import completion

from app.config import(
    get_api_key,
    get_model
)

def call_llm(
    messages,
    temperature = 0.7,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    max_tokens=500,
    stop=None     
):
    
    api_key = get_api_key()

    response = completion(
        model = get_model(),
        messages=messages,
        api_key=api_key,

        temperature = temperature,
        top_p = top_p,

        frequency_penalty = frequency_penalty,
        presence_penalty=presence_penalty,

        max_tokens = max_tokens,
        stop=stop 
    )
    # text = response.choices[0].message.content

    # usage_data = response.usage 

    # usage = {
    #     "input_tokens": usage_data.prompt_tokens,
    #     "output_tokens": usage_data.completion_tokens,
    #     "total_tokens": usage_data.total_tokens
    # } 

    # total_cost = cost(
    #     usage,
    #     PRICE_INPUT,
    #     PRICE_OUTPUT
    # )

    return response


def stream_llm(messages, **kwargs):
    api_key = get_api_key()
    response = completion(
        model = get_model(),
        messages=messages,
        api_key=api_key,
        stream=True,
        **kwargs
    )

    for chunk in response:
        content =(
            chunk.choices[0].delta.content
        )

        if content:
            yield content 


def generate_structured(
        messages,
        response_model
):
    response = completion(
        model = get_model(),
        messages = messages,
        api_key=get_api_key(),
        response_format=response_model
    )

    content = response.choices[0].message.content 

    return response_model.model_validate_json(content)
