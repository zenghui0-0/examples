from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from transformers import pipeline
import openai
import os

router = APIRouter()

local_model = pipeline(
    "text-generation",
    model="gpt2",
    device="cuda" if torch.cuda.is_available() else "cpu"
)

class CompletionRequest(BaseModel):
    text: str
    max_length: int = 50
    creativity: float = 0.7

@router.post("/complete")
async def generate_completion(request: CompletionRequest):
    try:
        # 本地模型快速响应
        local_result = local_model(
            request.text,
            max_length=request.max_length,
            temperature=request.creativity,
            do_sample=True
        )[0]['generated_text']
        
        # 如果配置了OpenAI，则并行获取更好结果
        openai_result = ""
        if os.getenv("OPENAI_API_KEY"):
            openai_result = await get_openai_completion(
                request.text, 
                request.creativity
            )
        
        return {
            "suggestions": [
                local_result[len(request.text):].strip(),
                openai_result[len(request.text):].strip()
            ],
            "used_local": True
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_openai_completion(text, temperature):
    response = await openai.Completion.create(
        engine="text-davinci-003",
        prompt=text,
        temperature=temperature,
        max_tokens=100
    )
    return response.choices[0].text
