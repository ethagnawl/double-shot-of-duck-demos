-- PANE 1: server. Owns the file + lock, serves it over Quack.
-- Run with:  duckdb quack_server.duckdb -f quack_server.sql -no-stdin
-- (or paste into:  duckdb quack_server.duckdb  and keep the shell open)

INSTALL quack FROM core_nightly;
LOAD quack;

CALL quack_serve('quack:localhost', token = 'super_secret');

CREATE TABLE t (id INTEGER PRIMARY KEY, val INTEGER);
INSERT INTO t VALUES (1, 100);

-- Keep this pane/shell alive while the clients run.
-- After the clients finish, check the result here:
--   SELECT * FROM t;