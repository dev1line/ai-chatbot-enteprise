FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PRISMA_HOME_DIR=/tmp/prisma

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    libatomic1 \
    openssl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt

COPY prisma ./prisma
RUN prisma generate --schema=prisma/schema.prisma

COPY . .

EXPOSE 8000
CMD ["./scripts/entrypoint.sh"]
