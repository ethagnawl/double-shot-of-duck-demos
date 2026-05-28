-- client.sql
INSTALL quack FROM core_nightly;
LOAD quack;
ATTACH 'quack:localhost' AS remote_db (TOKEN 'super_secret');
select * from remote_db.quackers;
