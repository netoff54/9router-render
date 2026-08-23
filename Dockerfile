FROM node:20-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy sync script and requirements
COPY sync.py /app/sync.py
COPY requirements.txt /app/requirements.txt
RUN chmod +x /app/sync.py

# Install Python dependencies
RUN pip3 install -r /app/requirements.txt --no-cache-dir

# Install 9Router globally
RUN npm install -g 9router

# Create data directory for persistence
RUN mkdir -p /app/data

# Set environment variables
ENV DATA_DIR=/app/data
ENV PORT=20128
ENV NODE_ENV=production

# Expose port
EXPOSE 20128

# Create startup script to run both 9Router and sync
RUN echo '#!/bin/bash\n\
echo "Starting 9Router with auto-sync..."\n\
echo "DATA_DIR: $DATA_DIR"\n\
echo "PORT: $PORT"\n\
echo "HF_TOKEN: ${HF_TOKEN:0:10}..."\n\
\n\
# Start sync script in background\n\
python3 /app/sync.py &\n\
SYNC_PID=$!\n\
\n\
# Start 9Router in foreground\n\
9router --port $PORT --host 0.0.0.0\n\
\n\
# Cleanup sync process on exit\n\
kill $SYNC_PID 2>/dev/null\n\
' > /app/start.sh && chmod +x /app/start.sh

# Start the application
CMD ["/app/start.sh"]