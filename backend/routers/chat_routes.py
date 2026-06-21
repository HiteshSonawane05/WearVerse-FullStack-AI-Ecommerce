from fastapi import APIRouter
from pydantic import BaseModel
import sys

sys.path.insert(0, r'C:\Users\Hitesh\Clothes_Ecommerce\chatbot')
sys.path.insert(0, r'C:\Users\Hitesh\Clothes_Ecommerce\chatbot\rag')

from query_generator import get_query_response
from agent import get_agent_response
from basic import get_rag_response

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

@router.post("/chat/query")
def chat_query(request: ChatRequest):
    response = get_query_response(request.message)
    return {"response": response}

@router.post("/chat/agent")
def chat_agent(request: ChatRequest):
    try:
        response = get_agent_response(request.message)
        return {"response": response}
    except Exception as e:
        print("AGENT ERROR:", str(e))
        return {"response": f"Sorry, I had trouble with that request. ({str(e)})"}
    
@router.post("/chat/policy")
def chat_policy(request: ChatRequest):
    response = get_rag_response(request.message)
    return {"response": response}