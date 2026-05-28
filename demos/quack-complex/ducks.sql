INSTALL quack FROM core_nightly;
LOAD quack;

INSTALL vss;
LOAD vss;

CREATE TABLE IF NOT EXISTS frames (
    id UUID PRIMARY KEY,
    frame_id UUID NOT NULL,
    camera_id VARCHAR NOT NULL,
    captured_at TIMESTAMPTZ NOT NULL,
    frame_uri VARCHAR,
);

CALL quack_serve('quack:localhost:9595', token = 'super_secret');
