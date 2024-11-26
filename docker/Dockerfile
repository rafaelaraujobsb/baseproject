FROM python:3.12.7-bookworm

ENV UV_PROJECT_ENVIRONMENT="/usr/local/"

RUN apt update -y && \
    apt install -y make clang python3-dev libpq-dev && \
    pip install --upgrade pip

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY src /app/src
COPY Makefile pyproject.toml uv.lock gunicorn.conf.py /app/

RUN make install-prod

CMD ["make", "run"]