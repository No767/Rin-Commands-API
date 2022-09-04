####################################################################################################
## Builder image
####################################################################################################
FROM python:3.10.6-slim-bullseye AS builder
ENV DEBIAN_FRONTEND=noninteractive 
RUN apt update \
    && apt install -y --no-install-recommends \
    build-essential \
    curl \
    ca-certificates \
    git

# Ad Poetry Locally
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN python -m pip install --upgrade pip setuptools
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="${PATH}:/root/.local/bin"

WORKDIR /Rin-Commands-API

COPY /pyproject.toml /Rin-Commands-API/
COPY /poetry.lock /Rin-Commands-API/

# Create dependency wheels
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes \
    && pip wheel --wheel-dir=/Rin-Commands-API/wheels -r requirements.txt

####################################################################################################
## Final image
####################################################################################################
FROM python:3.10.6-slim-bullseye
RUN apt update \
    && apt install -y --no-install-recommends \
    tini \
    ca-certificates \
    bash \
    git

WORKDIR /Rin-Commands-API
COPY /src/api.py /Rin-Commands-API/
COPY /src/api_utils/ /Rin-Commands-API/api_utils/
COPY /Debian-Docker/start.sh /Rin-Commands-API/start.sh

COPY --from=builder /Rin-Commands-API/wheels /Rin-Commands-API/wheels
COPY --from=builder /Rin-Commands-API/requirements.txt /Rin-Commands-API/requirements.txt

# Add an unprivileged user and set directory permissions
RUN adduser --disabled-password --gecos "" rin \
    && chown -R rin:rin /Rin-Commands-API \
    && chmod +x /Rin-Commands-API/start.sh

USER rin

# Set up path so pip won't complain again
ENV PATH="${PATH}:/home/rin/.local/bin"
ENV PYTHONDONTWRITEBYTECODE 1

RUN pip install --user --no-index --find-links=/Rin-Commands-API/wheels -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["/usr/bin/tini", "--"]

CMD ["/Rin-Commands-API/start.sh"]

STOPSIGNAL SIGTERM

# Image metadata
LABEL org.opencontainers.image.title="Rin-Commands-API"
LABEL org.opencontainers.image.description="An API for fetching commands and their info for Rin"
LABEL org.opencontainers.image.licenses="GPL-3.0"
LABEL org.opencontainers.image.source="https://github.com/No767/Rin-Commands-API"