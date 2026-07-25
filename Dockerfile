# Используем официальный Python-образ
FROM python:3.10-slim AS builder

# Устанавливаем системные зависимости для dnstwist (whois, etc.)
RUN apt-get update && apt-get install -y \
    whois \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем и устанавливаем Python-зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY src/ /app/src/
COPY config.yaml /app/
COPY README.md /app/

# Устанавливаем переменные окружения
ENV PYTHONPATH=/app
ENV NETLAS_API_KEY=""

# Точка входа
ENTRYPOINT ["python", "-m", "phisher"]
CMD ["--help"]