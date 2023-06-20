#!/bin/bash

set -e
set -u

# load environment variables from .env file
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source "$DIR/../.env"

create_database() {
	psql -v ON_ERROR_STOP=1 -U "$POSTGRES_MASTER" <<-EOSQL
        CREATE USER $POSTGRES_USER WITH PASSWORD '$POSTGRES_PASSWORD';
        ALTER USER $POSTGRES_USER WITH SUPERUSER;
	CREATE DATABASE $POSTGRES_DB;
        ALTER DATABASE $POSTGRES_DB OWNER TO $POSTGRES_USER;
EOSQL
}

grant_permissions() {
	psql -v ON_ERROR_STOP=1 -U "$POSTGRES_MASTER" <<-EOSQL
	GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DB TO $POSTGRES_USER;
EOSQL
}

create_table() {
	psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB" <<-EOSQL
        CREATE TABLE books (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            author VARCHAR(255) NOT NULL,
            description TEXT NOT NULL
        );
EOSQL
}

connect_database() {
	psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"
}

create_database
grant_permissions
create_table
connect_database