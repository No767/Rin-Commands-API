####################################################################################################
## Builder image
####################################################################################################
FROM python:3.10.7-alpine3.16 AS builder

# Note that some libaries require Linux Kernel C Headers
RUN apk add --no-cache \
    ca-certificates \
    build-base \
    curl \
    linux-headers

# Add Poetry locally
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
FROM python:3.10.7-alpine3.16

RUN apk add --no-cache \
    ca-certificates \
    tini \
    bash

WORKDIR /Rin-Commands-API
COPY /src/api.py /Rin-Commands-API/
COPY /src/api_utils/ /Rin-Commands-API/api_utils/
COPY /Alpine-Docker/start.sh /Rin-Commands-API/start.sh

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

ENTRYPOINT ["/sbin/tini", "--"]

CMD ["/Rin-Commands-API/start.sh"]

STOPSIGNAL SIGTERM

# Image metadata
LABEL org.opencontainers.image.title="Rin-Commands-API"
LABEL org.opencontainers.image.description="An API for fetching commands and their info for Rin"
LABEL org.opencontainers.image.licenses="GPL-3.0"
LABEL org.opencontainers.image.source="https://github.com/No767/Rin-Commands-API"