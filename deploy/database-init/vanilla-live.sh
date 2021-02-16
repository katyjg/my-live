#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE USER vanilla WITH PASSWORD 'CDAvxbkLnCQqb6bE0RCguPEpe2FOPN';
    CREATE DATABASE vanilla;
    GRANT ALL PRIVILEGES ON DATABASE vanilla TO vanilla;
EOSQL
