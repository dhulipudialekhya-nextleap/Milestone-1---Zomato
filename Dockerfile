# Railway production — reads PORT in Python (no shell $PORT expansion issues)
FROM python:3.12-slim-bookworm

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY src ./src

# Railway injects PORT at runtime; run_server.py binds to os.environ["PORT"]
CMD ["python", "-m", "src.backend.phase6.run_server"]
