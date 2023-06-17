FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10-slim as python-base
ENV PYTHONUNBUFFERED=true
WORKDIR /app

FROM python-base as poetry
ENV POETRY_HOME /opt/poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT true
ENV PATH "$POETRY_HOME/bin:$PATH"
RUN pip install poetry
COPY . .
RUN poetry install --no-interaction --no-ansi -vvv --without dev

FROM python-base as runtime
ENV PATH="/app/.venv/bin:$PATH"
COPY --from=poetry /app/hopper-bacco .
COPY --from=poetry /app/.venv .venv
RUN apt-get update &&\
    apt-get install -y --no-install-recommends curl &&\
    apt-get clean && rm -rf /var/lib/apt/lists/*

EXPOSE 80

ENTRYPOINT ["/bin/bash", "entrypoint.sh"]
