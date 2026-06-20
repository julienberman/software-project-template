FROM python:3.11-slim

RUN pip install --no-cache-dir uv

WORKDIR /backend

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project

COPY . .

# Run app at $HOSTNAME and $PORT, which are set in the backend service in Railway
# If these are not set, revert to defaults 
CMD uv run uvicorn app.main:app --host ${HOSTNAME-0.0.0.0} --port ${PORT-8000}


