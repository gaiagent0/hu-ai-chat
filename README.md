# 🇭🇺 Magyar AI Chat

Magyar nyelvű AI chat alkalmazás, Alibaba Qwen API-val, Oracle Cloud always-free infrastruktúrán.

**Élő demo:** [chat.istvanszechenyi.uk](https://chat.istvanszechenyi.uk)

---

## Stack

| Réteg | Technológia |
|---|---|
| Backend | FastAPI (Python) |
| AI | Alibaba Qwen API (qwen-plus / turbo / max) |
| Frontend | Vanilla HTML/CSS/JS |
| Reverse proxy | Caddy (auto HTTPS / Let's Encrypt) |
| Hosting | Oracle Cloud Always Free AMD VM |
| IaC | OpenTofu (Terraform) — lásd: [portfolio-infra](https://github.com/gaiagent0/portfolio-infra) |

---

## Architektúra

```
User → chat.istvanszechenyi.uk
         ↓ HTTPS (Caddy + Let's Encrypt)
       OCI AMD VM (Always Free)           ← ugyanaz a VM mint infra-insight!
         ↓ reverse proxy → 127.0.0.1:8000
       FastAPI (uvicorn)
         ↓ OpenAI-compatible API
       Alibaba DashScope (Qwen LLM)
```

### VM-en futó servicek (Caddy megosztás)

```
OCI AMD VM
  ├── hu-ai-chat    → port 8000 → chat.istvanszechenyi.uk
  └── infra-insight → port 8001 → infra.istvanszechenyi.uk
```

**Fontos:** `hu-ai-chat` és `infra-insight` ugyanazon az OCI VM-en él, közös Caddy reverse proxy alatt.  
Ha csak `hu-ai-chat` deploy scriptjét futtatod, a Caddyfile csak a `chat.*` domaint tartalmazza.  
Az `infra-insight` deploy scriptje írja ki a végleges Caddyfile-t mindkét domainnel.

**Ajánlott telepítési sorrend:**
1. `portfolio-infra` → VM provisionálás
2. `hu-ai-chat` deploy (setup.sh)
3. `infra-insight` deploy (setup.sh) — felülírja a Caddyfile-t, mindkét domaint beállítja

---

## Funkciók

- Magyar nyelvű AI asszisztens (Qwen LLM)
- Model választó: qwen-plus / qwen-turbo / qwen-max
- Conversation history kezelés
- Zero frontend framework — gyors, lightweight
- Production HTTPS, automatikus cert megújítás

---

## Lokális fejlesztés (laptop)

### Előfeltételek

- Python 3.11+
- Alibaba DashScope API key: [dashscope.aliyun.com](https://dashscope.aliyun.com)

### Backend indítása

```bash
git clone https://github.com/gaiagent0/hu-ai-chat.git
cd hu-ai-chat

# Python venv
python3 -m venv backend/.venv
source backend/.venv/bin/activate          # Windows: backend\.venv\Scripts\activate

# Függőségek
pip install -r backend/requirements.txt

# API key beállítása
echo "DASHSCOPE_API_KEY=sk-..." > .env
# vagy Windows PowerShell:
# "DASHSCOPE_API_KEY=sk-..." | Out-File .env

# Backend indítása
cd backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
# → http://127.0.0.1:8000
# → http://127.0.0.1:8000/docs  (Swagger UI)
```

### Frontend megnyitása

A frontend statikus HTML fájl, nincs build lépés:

```bash
# Böngészőből közvetlenül megnyitható:
start frontend/index.html   # Windows
open frontend/index.html    # macOS
```

> **Megjegyzés:** a frontend `http://127.0.0.1:8000`-re hív API-khoz. Ha a backend fut, azonnal működik.

### API végpontok tesztelése

```bash
# Chat üzenet küldése
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Szia!", "history": []}'

# Health check
curl http://127.0.0.1:8000/health
```

---

## OCI deploy (első telepítés)

> Előfeltétel: a VM már létezik (`portfolio-infra` után).

```bash
# 1. SSH az OCI VM-re
ssh ubuntu@<OCI_VM_IP>

# 2. API key beállítása
echo "DASHSCOPE_API_KEY=sk-..." > ~/.env.hu-ai-chat

# 3. Deploy script futtatása
git clone https://github.com/gaiagent0/hu-ai-chat.git
bash hu-ai-chat/deploy/setup.sh
```

A setup.sh elvégzi:
1. `apt` frissítés, Python + Caddy telepítés
2. Repo klónozás / git pull
3. Python venv + pip install
4. systemd service beállítás (`hu-ai-chat.service`, port 8000)
5. Caddyfile kiírása — **csak `chat.*` domain** (az `infra-insight` setup.sh bővíti ki)
6. Caddy újraindítás

### Frissítés (már telepített VM-en)

```bash
ssh ubuntu@<OCI_VM_IP>
cd ~/hu-ai-chat && git pull
source backend/.venv/bin/activate && pip install -r backend/requirements.txt
sudo systemctl restart hu-ai-chat
```

---

## Környezeti változók

| Változó | Hol kell | Leírás |
|---|---|---|
| `DASHSCOPE_API_KEY` | `~/.env.hu-ai-chat` (VM) vagy `.env` (lokális) | Alibaba DashScope API kulcs |

Az API key beszerzése: [Alibaba Cloud Console → DashScope → API Keys](https://dashscope.console.aliyun.com/apiKey)

---

## Kapcsolódó repók

| Repo | Kapcsolat |
|---|---|
| [portfolio-infra](https://github.com/gaiagent0/portfolio-infra) | OCI VM provisionálás — **előfeltétel** |
| [infra-insight](https://github.com/gaiagent0/infra-insight) | Ugyanazon a VM-en fut, figyeli a szerver metrikákat |

---

## Licensz

MIT
