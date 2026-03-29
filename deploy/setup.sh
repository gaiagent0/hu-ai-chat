#!/bin/bash
# Magyar AI Chat — OCI AMD VM setup
# Usage: bash deploy/setup.sh
set -e

echo "[1/6] System update..."
sudo apt-get update -qq && sudo apt-get upgrade -y -qq

echo "[2/6] Install deps..."
sudo apt-get install -y -qq python3-pip python3-venv git caddy

echo "[3/6] Clone / update repo..."
cd ~
if [ -d "hu-ai-chat" ]; then
  cd hu-ai-chat && git pull
else
  git clone git@github.com:gaiagent0/hu-ai-chat.git
  cd hu-ai-chat
fi

echo "[4/6] Python venv..."
python3 -m venv backend/.venv
backend/.venv/bin/pip install -q -r backend/requirements.txt

echo "[5/6] Systemd service..."
sudo tee /etc/systemd/system/hu-ai-chat.service > /dev/null <<SERVICE
[Unit]
Description=Magyar AI Chat
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/hu-ai-chat/backend
EnvironmentFile=/home/ubuntu/.env.hu-ai-chat
ExecStart=/home/ubuntu/hu-ai-chat/backend/.venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
SERVICE

sudo systemctl daemon-reload
sudo systemctl enable hu-ai-chat
sudo systemctl restart hu-ai-chat

echo "[6/6] Caddy config..."
sudo tee /etc/caddy/Caddyfile > /dev/null <<CADDY
chat.istvan.szechenyi.uk {
  reverse_proxy 127.0.0.1:8000
}
CADDY

sudo systemctl restart caddy
echo "Done! Status:"
sudo systemctl status hu-ai-chat --no-pager
