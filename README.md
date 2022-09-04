<div align=center>

# Rin-Commands-API

![Rin](https://raw.githubusercontent.com/No767/Rin/dev/assets/rin-logo.png)

[![Required Python Version](https://img.shields.io/badge/Python-3.10-blue?logo=python&logoColor=white)](https://github.com/No767/Rin-Commands-API/blob/dev/pyproject.toml) [![Docker Build (GHCR, Alpine)](https://github.com/No767/Rin-Commands-API/actions/workflows/docker-build-ghcr-alpine.yml/badge.svg)](https://github.com/No767/Rin-Commands-API/actions/workflows/docker-build-ghcr-alpine.yml) [![Docker Build (GHCR, Debian)](https://github.com/No767/Rin-Commands-API/actions/workflows/docker-build-ghcr-debian.yml/badge.svg)](https://github.com/No767/Rin-Commands-API/actions/workflows/docker-build-ghcr-debian.yml) [![Docker Build (Hub, Alpine)](https://github.com/No767/Rin-Commands-API/actions/workflows/docker-build-hub-alpine.yml/badge.svg)](https://github.com/No767/Rin-Commands-API/actions/workflows/docker-build-hub-alpine.yml) [![Docker Build (Hub, Debian)](https://github.com/No767/Rin-Commands-API/actions/workflows/docker-build-hub-debian.yml/badge.svg)](https://github.com/No767/Rin-Commands-API/actions/workflows/docker-build-hub-debian.yml) ![GitHub](https://img.shields.io/github/license/No767/Rin-Commands-API?label=License&logo=github)

The Commands API for Rin

<div align=left>

# Info 
Within Rin's Site, there exists a page that allows you to see the different commands. The way that it is done is that it fetches from an API. And this is the API it fetches the data from. The API is a private API, which means that it is only really used internally. But this API can be self-hosted by anyone (The API is packaged using Docker and can be used with both the Debian or Alpine base images) This API is built on FastAPI, and uses PostgreSQL and Redis.

# License

GPL-3.0