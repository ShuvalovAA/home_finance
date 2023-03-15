-- CREATE EXTENSION dblink;
-- DO
-- $body$
-- BEGIN
--   IF NOT EXISTS(SELECT 1 FROM pg_catalog.pg_user WHERE usename = 'postgres') THEN
--     CREATE ROLE postgres WITH LOGIN CREATEDB PASSWORD 'postgres';
--   END IF;
-- END
-- $body$;

-- DO
-- $body$
-- BEGIN
--   IF NOT EXISTS(SELECT 1 FROM pg_database WHERE datname = 'home_f') THEN
--     PERFORM dblink_exec('dbname=' || current_database(), 'CREATE DATABASE home_f OWNER postgres');
--   END IF;
-- END
-- $body$;
CREATE DATABASE home_f;