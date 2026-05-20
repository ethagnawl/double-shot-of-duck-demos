-- client.sql

INSTALL quack FROM core_nightly;
LOAD quack;

ATTACH 'quack:localhost' AS remote_db (TOKEN 'Y0L0');

select * from remote_db.quackers;
