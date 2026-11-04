from pydantic import BaseModel
from typing import Literal 

class EchoRequest(BaseModel):
    message:str 

class ChatRequest(BaseModel):
    message:str 

class ChatResponse(BaseModel):
    text:str
    usage:dict
    cost:float 
