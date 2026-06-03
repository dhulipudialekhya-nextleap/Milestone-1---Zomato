# Railway production image — slim API (mock data; no pandas/HF at runtime)
FROM python:3.12-slim-bookworm

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY src ./src

EXPOSE 8000

CMD ["sh", "-c", "python -m uvicorn src.backend.phase6.server:app --host 0.0.0.0 --port ${PORT:-8000}"]
