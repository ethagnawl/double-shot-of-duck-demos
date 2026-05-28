-- PANE 2: client 1. Inserts id=1 first. Run line-by-line in:  duckdb

INSTALL quack FROM core_nightly;
LOAD quack;
CREATE SECRET (TYPE quack, TOKEN 'super_secret');
ATTACH 'quack:localhost' AS remote;

BEGIN TRANSACTION;
INSERT INTO remote.t VALUES (77, 200);

-- >>> STOP HERE. Switch to pane 3, run client 2's BEGIN + INSERT. <<<
-- Then come back and commit (client 1 wins the key):

COMMIT;
