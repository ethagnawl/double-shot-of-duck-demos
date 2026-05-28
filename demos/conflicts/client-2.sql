-- PANE 3: client 2. Tries the same key, loses, then retries. Run in:  duckdb

INSTALL quack FROM core_nightly;
LOAD quack;
CREATE SECRET (TYPE quack, TOKEN 'super_secret');
ATTACH 'quack:localhost' AS remote;

BEGIN TRANSACTION;

-- Run AFTER client 1's INSERT, BEFORE client 1 commits.
-- Expected: a conflict / duplicate-key (PRIMARY KEY) rejection.
INSERT INTO remote.t VALUES (1, 300);

-- On rejection:
ROLLBACK;

-- After client 1 commits, retry with a non-colliding key to show progress:
BEGIN TRANSACTION;
INSERT INTO remote.t VALUES (22, 300);
COMMIT;
