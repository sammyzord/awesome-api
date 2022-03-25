FROM python:3.8-slim as base

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

WORKDIR /app

FROM base as builder

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry export -o requirements.txt

RUN python -m venv /venv

RUN /venv/bin/pip install --no-cache-dir -r requirements.txt

FROM base as production 

COPY --from=builder /venv /venv

COPY ./src ./src

ENV PATH=/venv/bin:$PATH

CMD uvicorn src.main:app --host 0.0.0.0 --port 8000
