from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.completion import router as completion_router
from .core.expansion import router as expansion_router

app = FastAPI(title="写作助手AI服务")

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 路由注册
app.include_router(completion_router, prefix="/api/ai", tags=["AI"])
app.include_router(expansion_router, prefix="/api/ai", tags=["AI"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
