FROM node:24-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip curl \
    && rm -rf /var/lib/apt/lists/* \
    && pip3 install flask --break-system-packages

# Install Claude Code CLI — the whole point of this container
RUN npm install -g @anthropic-ai/claude-code

# Create non-root user — Claude CLI refuses --dangerously-skip-permissions as root
RUN useradd -ms /bin/bash reviewer

COPY server.py /app/server.py
RUN chown -R reviewer:reviewer /app

WORKDIR /app
USER reviewer

EXPOSE 7891
CMD ["python3", "-u", "server.py"]
