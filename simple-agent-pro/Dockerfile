# etapa 1 — builder
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# etapa 2 — production
FROM python:3.11-slim AS production
WORKDIR /app

# copia las dependencias instaladas del builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# copia solo lo necesario para correr
COPY src/ ./src/
COPY main.py .
COPY .env .

CMD ["python3", "main.py"]