#!/bin/bash

set -e
set -u

# load environment variables from .env file
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source "$DIR/../.env"

delete_table() {
    psql -v ON_ERROR_STOP=1 -U "$POSTGRES_MASTER" -d "$POSTGRES_DB" <<-EOSQL
        DROP TABLE $POSTGRES_TABLE;
EOSQL
}

delete_user() {
    psql -v ON_ERROR_STOP=1 -U "$POSTGRES_MASTER" -d "$POSTGRES_DB" <<-EOSQL
        REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA public FROM $POSTGRES_USER;
        REVOKE USAGE ON SCHEMA public FROM $POSTGRES_USER;
        DROP USER $POSTGRES_USER;
EOSQL
}

delete_database() {
    psql -v ON_ERROR_STOP=1 -U "$POSTGRES_MASTER" <<-EOSQL
        DROP DATABASE IF EXISTS $POSTGRES_DB;
EOSQL
}

delete_table
delete_user
delete_database
