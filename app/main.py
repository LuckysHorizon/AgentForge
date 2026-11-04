from fastapi import FastAPI, Request 
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.schemas import(
    EchoRequest,
    ChatRequest,
    ChatResponse
)

from app.llm import call_llm

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


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    messages = [
        {
            "role": "user",
            "content": request.message
        }
    ]

    result = call_llm(messages)

    return result


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

