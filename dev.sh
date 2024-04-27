#!/usr/bin/env bash
docker compose --env-file dev.env -f docker-compose.base.yml -f docker-compose.dev.yml up --build mongo redis strapi strapi_mysql
