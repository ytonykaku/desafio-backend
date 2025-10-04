FROM python:3.10-slim as builder

WORKDIR /app

RUN apt-get update && apt-get install -y git && pip install poetry

RUN poetry config virtualenvs.in-project true

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root

FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y git

COPY --from=builder /app/.venv ./.venv

ENV PATH="/app/.venv/bin:$PATH"

COPY . .

EXPOSE 5000

CMD ["python", "run.py"]