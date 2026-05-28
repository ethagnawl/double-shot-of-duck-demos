FORCE INSTALL quack FROM core_nightly;
LOAD quack;

INSTALL vss;
LOAD vss;

CREATE TABLE IF NOT EXISTS frames (
    id UUID PRIMARY KEY,
    camera_id VARCHAR NOT NULL,
    captured_at TIMESTAMPTZ NOT NULL,
    embedding FLOAT[512] NOT NULL,
    frame_path VARCHAR NOT NULL,
    frame_uri VARCHAR NOT NULL,
    routed_at TIMESTAMPTZ,
);

-- HACK!
SET hnsw_enable_experimental_persistence = true;
CREATE INDEX IF NOT EXISTS frames_embed_idx ON frames USING HNSW (embedding) WITH (metric = 'cosine');

CALL quack_serve('quack:localhost', token = 'super_secret');
