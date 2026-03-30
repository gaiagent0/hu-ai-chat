from fastapi import FastAPI, HTTPException, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI(title="Magyar AI Chat")

# --- API Key auth ---
APP_API_KEY = os.environ["APP_API_KEY"]
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def verify_api_key(key: str = Security(api_key_header)):
    if key != APP_API_KEY:
        raise HTTPException(status_code=403, detail="Forbidden")

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://chat.istvanszechenyi.uk"],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

client = OpenAI(
    api_key=os.environ["DASHSCOPE_API_KEY"],
    base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
)

SYSTEM_PROMPT = (
    "Te egy segitokesz magyar AI asszisztens vagy. "
    "Mindig magyarul valaszolj, kiveve ha a felhasznalo mas nyelven ir. "
    "Legyel baratsagos, tomer es pontos."
)

ALLOWED_MODELS = {"qwen-plus", "qwen-turbo", "qwen-max"}

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[Message]
    model: str = "qwen-plus"

@app.post("/api/chat", dependencies=[Security(verify_api_key)])
async def chat(req: ChatRequest):
    if req.model not in ALLOWED_MODELS:
        raise HTTPException(status_code=400, detail=f"Model not allowed. Use one of: {ALLOWED_MODELS}")
    try:
        response = client.chat.completions.create(
            model=req.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *[m.model_dump() for m in req.messages],
            ],
            max_tokens=1000,
        )
        return {"reply": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok"}

app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")
