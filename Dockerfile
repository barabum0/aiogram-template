FROM python:3.12-slim AS poetry
LABEL authors="Roman Poltorabatko"
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN pip install poetry

FROM poetry AS environment
WORKDIR /usr/src/app
COPY ./pyproject.toml /usr/src/app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

FROM environment AS code
WORKDIR /usr/src/app
COPY . /usr/src/app

RUN poetry install

ENTRYPOINT ["poetry", "run", "app"]
