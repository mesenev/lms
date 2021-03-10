#!/bin/bash

set -e
set -u

function create_user_and_database() {
	echo "  Creating database '$1' for user '$POSTGRES_USER'"
	psql -v ON_ERROR_STOP=1 -U $POSTGRES_USER -c "CREATE DATABASE $1 WITH OWNER $POSTGRES_USER;"
}

if [ "$POSTGRES_MULTIPLE_DATABASES" ]; then
	echo "Multiple database creation requested: $POSTGRES_MULTIPLE_DATABASES"
	for db in $(echo "$POSTGRES_MULTIPLE_DATABASES" | tr ',' ' '); do
		create_user_and_database "$db"
	done
	echo "Multiple databases created"
fi
