#!/bin/bash

set -e
set -u

# Create custom database
create_database() {
	psql -v ON_ERROR_STOP=1 -U "$POSTGRES_MASTER" <<-EOSQL
        CREATE USER $WORKSHOP_POSTGRES_USER WITH PASSWORD '$WORKSHOP_POSTGRES_PASSWORD';
        ALTER USER $WORKSHOP_POSTGRES_USER WITH SUPERUSER;
	CREATE DATABASE $WORKSHOP_POSTGRES_DB;
        ALTER DATABASE $WORKSHOP_POSTGRES_DB OWNER TO $WORKSHOP_POSTGRES_USER;
EOSQL
}

grant_permissions() {
	psql -v ON_ERROR_STOP=1 -U "$POSTGRES_MASTER" <<-EOSQL
	GRANT ALL PRIVILEGES ON DATABASE $WORKSHOP_POSTGRES_DB TO $WORKSHOP_POSTGRES_USER;
EOSQL
}

create_table() {
	psql -v ON_ERROR_STOP=1 -U "$WORKSHOP_POSTGRES_USER" -d "$WORKSHOP_POSTGRES_DB" <<-EOSQL
        CREATE TABLE books (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            author VARCHAR(255) NOT NULL,
            description TEXT NOT NULL
        );
EOSQL
}

connect_database() {
	psql -U "$WORKSHOP_POSTGRES_USER" -d "$WORKSHOP_POSTGRES_DB"
}

create_database
grant_permissions
create_table
connect_database