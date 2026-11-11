import json

from fastapi import FastAPI, Request 
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse 

from app.schemas import(
    EchoRequest,
    ChatRequest,
    ChatResponse,
    StudentInfo
)

from app.config import PRICE_INPUT, PRICE_OUTPUT
from app.llm import call_llm, generate_structured, stream_llm
from app.pricing import cost

app = FastAPI(
    title="AgentForge",
    description="Provider-Agnostic LLM API",
    version="1.0.0"
)


def error_response(message, code, details=None):
    return{
        "error":{
            "message": message,
            "code": code,
            "details": details
        }
    }


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=422,
        content=error_response(
            "Invalid request",
            "VALIDATION_ERROR",
            exc.errors()
        )
    )

@app.get("/health")
def health():
    return{
        "status": "healthy",
        "service": "AgentForge"
    }

@app.post("/echo")
def echo(request: EchoRequest):
    return{
        "message": request.message
    }

@app.post("/chat/stream")
def chat_stream(request: ChatRequest):

    def generate():
        for token in stream_llm(
            messages=[
                {
                    "role": "user",
                    "content": request.message
                }
            ],
            temperature=request.temperature,
            top_p=request.top_p,
            max_tokens=request.max_tokens,
            stop=request.stop
        ):
            yield f"data: {json.dumps({'token': token})}\n\n"

        yield 'data: [DONE]\n\n'

    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    response = call_llm(
        messages = [
            {
                "role": "user",
                "content": request.message
            }
        ],
        temperature=request.temperature,
        top_p = request.top_p,

        frequency_penalty=request.frequency_penalty,
        presence_penalty=request.presence_penalty,

        max_tokens=request.max_tokens,
        stop=request.stop 
    )
    usage_data = response.usage
    if usage_data is None:
        raise ValueError("LLM response did not include token usage")

    usage = {
        "input_tokens": usage_data.prompt_tokens,
        "output_tokens": usage_data.completion_tokens,
        "total_tokens": usage_data.total_tokens,
    }
    if any(token_count is None for token_count in usage.values()):
        raise ValueError("LLM response returned incomplete token usage")

    return {
        "text": response.choices[0].message.content,
        "usage": usage,
        "cost": cost(usage, PRICE_INPUT, PRICE_OUTPUT),
    }


@app.post("/chat/structured")
def structured_chat(request:ChatRequest):
    result = generate_structured(
        messages=[
            {
                "role": "user",
                "content": request.message
            }
        ],
        response_model=StudentInfo
    )
    return result.model_dump()

@app.exception_handler(Exception)
async def general_exception_handler(
    request: Request,
    exc: Exception
):
    return JSONResponse(
        status_code=500,
        content=error_response(
            "Internal sever error",
            "INTERNAL_ERROR"
        )
    )
