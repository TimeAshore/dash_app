#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	SET TIMEZONE='Asia/shanghai';
	CREATE DATABASE socamas_dev OWNER postgres;
	GRANT ALL PRIVILEGES ON DATABASE socamas_dev TO postgres;
	\c socamas_dev;
	CREATE EXTENSION "uuid-ossp";
	CREATE EXTENSION pgcrypto;
    SET TIMEZONE='Asia/shanghai';
	CREATE DATABASE socamas_test OWNER postgres;
	GRANT ALL PRIVILEGES ON DATABASE socamas_test TO postgres;
	\c socamas_test;
	CREATE EXTENSION "uuid-ossp";
	CREATE EXTENSION pgcrypto;

EOSQL
