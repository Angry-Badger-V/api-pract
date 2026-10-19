-- Disconnect active connections
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE datname = 'nc_plus_one'
  AND pid <> pg_backend_pid();

-- Drop database if it exists
DROP DATABASE IF EXISTS nc_plus_one;

-- Recreate database
CREATE DATABASE nc_plus_one;
