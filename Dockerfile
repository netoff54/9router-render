FROM node:20-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-full \
    python3-venv \
    curl \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy scripts and requirements
COPY sync.py /app/sync.py
COPY messaging_service.py /app/messaging_service.py
COPY messaging_api.py /app/messaging_api.py
COPY requirements.txt /app/requirements.txt
RUN chmod +x /app/sync.py

# Install Python dependencies with virtual environment
RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install -r /app/requirements.txt --no-cache-dir

# Install 9Router globally
RUN npm install -g 9router@latest

# Create data directory for persistence
RUN mkdir -p /app/data

# Default env vars (overridden by Render environment variables)
ENV DATA_DIR=/app/data
ENV PORT=20128
ENV MESSAGING_API_PORT=5000
ENV NODE_ENV=production
ENV AUTH_COOKIE_SECURE=false
ENV CI=true

# Only expose the single public port (Render assigns $PORT automatically)
EXPOSE 20128

# Write startup script
RUN cat > /app/start.sh << 'STARTSCRIPT'
#!/bin/bash
set -e

echo "================================================"
echo "  9Router - Starting on port $PORT"
echo "  DATA_DIR: $DATA_DIR"
echo "  HF sync: ${HF_TOKEN:+enabled (token set)}"
echo "  Messaging API: internal port $MESSAGING_API_PORT"
echo "================================================"

# [1] Start HuggingFace sync (restore data on boot + backup every 5min)
/opt/venv/bin/python /app/sync.py &
SYNC_PID=$!
echo "[sync] Started (PID $SYNC_PID)"

# Wait a bit for initial data restore before starting 9Router
sleep 10

# [2] Start Messaging API on internal port 5000 (NOT exposed publicly)
/opt/venv/bin/python /app/messaging_api.py &
API_PID=$!
echo "[messaging-api] Started internally on port $MESSAGING_API_PORT (PID $API_PID)"

# [3] Self-ping anti-sleep loop (every 5 minutes)
(
  sleep 90
  while true; do
    STATUS=$(curl -sf -o /dev/null -w "%{http_code}" "http://localhost:${PORT}/" 2>/dev/null || echo "fail")
    echo "[self-ping] $(date '+%H:%M:%S') - status: $STATUS"
    sleep 300
  done
) &
PING_PID=$!
echo "[self-ping] Anti-sleep loop started (PID $PING_PID)"

# [4] Start 9Router in foreground (this is the main process)
export DISPLAY=""
export WAYLAND_DISPLAY=""
export XDG_SESSION_TYPE=""
export QT_QPA_PLATFORM=""
export ELECTRON_RUN_AS_NODE="1"
export NODE_ENV="production"
export CI="true"

echo "[9router] Starting on port $PORT..."
cd /usr/local/lib/node_modules/9router
exec node cli.js --port "$PORT" --host 0.0.0.0 --skip-update --no-browser --log

# Cleanup (only runs if 9router exits)
kill $SYNC_PID 2>/dev/null || true
kill $API_PID 2>/dev/null || true
kill $PING_PID 2>/dev/null || true
STARTSCRIPT

RUN chmod +x /app/start.sh

CMD ["/app/start.sh"]