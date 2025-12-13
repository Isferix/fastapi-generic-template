# Define build-time argument
ARG env=dev

FROM python:3.12.12-alpine3.23 AS base

ARG env
ENV ENV_MODE=$env

# Debugging info during build
RUN echo "Building with env=$env"

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the application into the container

WORKDIR /server
COPY . .

# Usa una carpeta de venv específica
RUN uv sync --frozen --no-cache

EXPOSE 8000

# ---------- STAGE: dev-deploy ----------
FROM base AS dev-deploy
CMD ["uv", "run", "uvicorn", "src.main:server", "--host", "0.0.0.0", "--reload"] 

# ---------- STAGE: test-deploy ----------
FROM base AS test-deploy
CMD ["uv", "run", "uvicorn", "src.main:server", "--host", "0.0.0.0", "--reload"] 

# ---------- STAGE: prod-deploy ----------
FROM base AS prod-deploy
CMD ["uv", "run", "uvicorn", "src.main:server", "--host", "0.0.0.0", "--forwarded-allow-ips", "*"]

# ---------- STAGE: final ----------
FROM ${env}-deploy AS final-deploy