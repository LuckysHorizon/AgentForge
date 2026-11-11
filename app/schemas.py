from pydantic import BaseModel, Field
from typing import Optional 

class EchoRequest(BaseModel):
    message:str 

class ChatRequest(BaseModel):
    message:str = Field(min_length=1)

    temperature: float =  Field(
        default=0.7,
        ge=0.0,
        le=2.0
    )

    top_p: float = Field(
        default=1.0,
        gt=0.0,
        le=1.0  
    )

    frequency_penalty: float = Field(
        default=0.0,
        ge=-2.0,
        le=2.0  
    )

    presence_penalty: float = Field(
            default=0.0,
            ge=-2.0,
            le=2.0  
    )

    max_tokens: Optional[int] = Field(
        default=500,
        gt=0
    )

    stop: Optional[list[str]] = None
    stream: bool = False  

class ChatResponse(BaseModel):
    text:str
    usage:dict[str, int]
    cost:float 

class StudentInfo(BaseModel):

    name : str 

    age: int = Field(
        ge=1,
        le=120
    )

    skills: list[str]

