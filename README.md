# 🇭🇺 Magyar AI Chat

Élő demo: **[chat.istvanszechenyi.uk](https://chat.istvanszechenyi.uk)**

Magyar nyelvű AI chat alkalmazás, Alibaba Qwen API-val, Oracle Cloud always-free infrastruktúrán.

## Stack

| Réteg | Technológia |
|---|---|
| Backend | FastAPI (Python) |
| AI | Alibaba Qwen API (qwen-plus / turbo / max) |
| Frontend | Vanilla HTML/CSS/JS |
| Reverse proxy | Caddy (auto HTTPS / Let's Encrypt) |
| Hosting | Oracle Cloud Always Free AMD VM |
| IaC | OpenTofu (Terraform) |

## Funkciók

- Magyar nyelvű AI asszisztens (Qwen LLM)
- Model választó: qwen-plus / qwen-turbo / qwen-max
- Conversation history kezelés
- Zero frontend framework — gyors, lightweight
- Production HTTPS, automatikus cert megújítás

## Architektúra

```
User → chat.istvanszechenyi.uk
         ↓ HTTPS (Caddy + Let's Encrypt)
       OCI AMD VM (Always Free)
         ↓ reverse proxy → 127.0.0.1:8000
       FastAPI (uvicorn)
         ↓ OpenAI-compatible API
       Alibaba DashScope (Qwen LLM)
```

## Deploy

```bash
# 1. API key
echo 'DASHSCOPE_API_KEY=sk-...' > ~/.env.hu-ai-chat

# 2. Setup (Ubuntu 22.04)
bash deploy/setup.sh
```

## Infrastruktúra

Az OCI infrastruktúra Terraform/OpenTofu kóddal van definiálva: [portfolio-infra](https://github.com/gaiagent0/portfolio-infra)

- VCN + public subnet + security list
- AMD VM (VM.Standard.E2.1.Micro) — always free
- ARM A1 VM (4 OCPU / 24 GB) — always free (capacity retry)

## Licensz

MIT
