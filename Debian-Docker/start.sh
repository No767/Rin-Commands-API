#!/bin/bash

if [[ -v POSTGRES_USER ]]; then
    echo "Postgres_Username=${POSTGRES_USER}" >> /Rin-Commands-API/.env
else
    echo "Missing Postgres_Username env var! POSTGRES_USER environment variable is not set."
    exit 1;
fi

if [[ -v POSTGRES_PASSWORD ]]; then
    echo "Postgres_Password=${POSTGRES_PASSWORD}" >> /Rin-Commands-API/.env
else
    echo "Missing Postgres_Password env var! POSTGRES_PASSWORD environment variable is not set."
    exit 1;
fi

if [[ -v POSTGRES_IP ]]; then
    echo "Postgres_Server_IP=${POSTGRES_IP}" >> /Rin-Commands-API/.env
else
    echo "Missing Postgres_Server_IP env var! POSTGRES_IP environment variable is not set."
    exit 1;
fi

if [[ -v POSTGRES_DATABASE ]]; then
    echo "Postgres_Database=${POSTGRES_DATABASE}" >> /Rin-Commands-API/.env
else
    echo "Missing Postgres_Database env var! POSTGRES_DATABASE environment variable is not set."
    exit 1;
fi

if [[ -v POSTGRES_PORT ]]; then
    echo "Postgres_Server_Port=${POSTGRES_PORT}" >> /Rin-Commands-API/.env
else
    echo "Missing Postgres_Server_Port env var! POSTGRES_PORT environment variable is not set."
    exit 1;
fi

if [[ -v REDIS_IP ]]; then
    echo "Redis_Server_IP=${REDIS_IP}" >> /Rin-Commands-API/.env
else
    echo "Missing Redis_Server_IP env var! REDIS_IP environment variable is not set."
    exit 1;
fi

if [[ -v REDIS_PORT ]]; then
    echo "Redis_Port=${REDIS_PORT}" >> /Rin-Commands-API/.env
else
    echo "Missing Redis_Port env var! REDIS_PORT environment variable is not set."
    exit 1;
fi

exec gunicorn api:app --workers 8 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000