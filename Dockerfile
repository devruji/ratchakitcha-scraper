# ─── Base image ────────────────────────────────────────────────────────────────
FROM python:3.12.3-slim

# ─── Metadata ──────────────────────────────────────────────────────────────────
LABEL maintainer="you@example.com"

# ─── Workdir ──────────────────────────────────────────────────────────────────
WORKDIR /app

# ─── Install Python deps + Playwright browsers in one go ───────────────────────
COPY requirements.txt .
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      wget \
      ca-certificates \
 && rm -rf /var/lib/apt/lists/* \
 && pip install --no-cache-dir -r requirements.txt \
 && python -m playwright install --with-deps

# ─── Copy your code ─────────────────────────────────────────────────────────────
COPY app/ .

# ─── Entrypoint ────────────────────────────────────────────────────────────────
ENTRYPOINT ["python", "pipeline_run.py"]
CMD []
