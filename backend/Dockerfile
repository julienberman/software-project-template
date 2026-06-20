FROM python:3.11-slim

RUN pip install --no-cache-dir uv

WORKDIR /backend

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project

COPY . .

ENV HOST=0.0.0.0
ENV PORT=8000

CMD uv run uvicorn app.main:app --host ${HOST} --port ${PORT}

