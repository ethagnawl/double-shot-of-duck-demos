INSTALL quack FROM core_nightly;
LOAD quack;

CREATE TABLE IF NOT EXISTS quackers (
    id INTEGER PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
);

insert into quackers (id, name) values (0, 'hello');

CALL quack_serve('quack:localhost', token = 'Y0L0');
