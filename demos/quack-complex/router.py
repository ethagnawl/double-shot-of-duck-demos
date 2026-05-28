import duckdb
import json
import sys
import time
import uuid

from loguru import logger

QUACK_TOKEN = "super_secret"
SRC_URI = "quack:localhost:9494"
DUCK_URI = "quack:localhost:9595"
CAT_URI = "quack:localhost:9696"

# Cosine-distance thresholds (0 = identical direction, 2 = opposite).
# These are independent — tune each separately. Lower = stricter match.
DUCK_THRESHOLD = 0.25
CAT_THRESHOLD = 0.25

POLL_INTERVAL = 2.0
BATCH = 200  # max frames pulled per tick

with open("animal-embeddings.json") as f:
    reference_embeddings = json.load(f)
DUCK_REF, CAT_REF = reference_embeddings["duck"], reference_embeddings["cat"]


def select_unrouted(conn):
    select_unrouted = """
SELECT
    id, camera_id, captured_at, frame_uri,
    array_cosine_distance(embedding, $duck_ref::FLOAT[512]) AS duck_dist,
    array_cosine_distance(embedding, $cat_ref::FLOAT[512])  AS cat_dist
FROM src.frames
WHERE routed_at IS NULL
LIMIT $batch
    """
    return conn.execute(
        select_unrouted,
        {"duck_ref": DUCK_REF, "cat_ref": CAT_REF, "batch": BATCH},
    ).fetchall()


def insert_into_target_database(db_type, conn, params):
    insert_target = """
INSERT INTO {tgt}.frames (id, frame_id, camera_id, captured_at, frame_uri)
VALUES ($id, $frame_id, $camera_id, $captured_at, $frame_uri)
    """
    return conn.execute(insert_target.format(tgt=db_type), params)


def connect():
    conn = duckdb.connect()
    conn.execute("INSTALL quack FROM core_nightly; LOAD quack;")
    conn.execute("INSTALL vss; LOAD vss;")
    conn.execute(f"ATTACH '{SRC_URI}'  AS src  (TOKEN '{QUACK_TOKEN}');")
    conn.execute(f"ATTACH '{DUCK_URI}' AS duck (TOKEN '{QUACK_TOKEN}');")
    conn.execute(f"ATTACH '{CAT_URI}'  AS cat  (TOKEN '{QUACK_TOKEN}');")
    logger.info("attached src / duck / cat")
    return conn


# Use stateless query to address Binder Error mentioned in post
def mark_routed(conn, frame_id):
    inner = f"UPDATE frames SET routed_at = now() WHERE id = '{frame_id}'"
    conn.execute(
        "SELECT * FROM quack_query($uri, $q, token := $tok)",
        {"uri": SRC_URI, "q": inner, "tok": QUACK_TOKEN},
    )


def route_once(conn):
    unrouted_rows = select_unrouted(conn)
    for id, camera_id, captured_at, frame_uri, duck_dist, cat_dist in unrouted_rows: # noqa
        params = {
            "camera_id": camera_id,
            "captured_at": captured_at,
            "frame_id": id,  # upstream frame id
            "frame_uri": frame_uri,
            "id": str(uuid.uuid4()),
        }

        logger.info(f"cat_dist: {cat_dist}")
        logger.info(f"duck_dist: {duck_dist}")

        if duck_dist is not None and duck_dist < DUCK_THRESHOLD:
            insert_into_target_database("duck", conn, params)
            logger.info(f"{id}# duck (dist={duck_dist:.3f})")

        if cat_dist is not None and cat_dist < CAT_THRESHOLD:
            insert_into_target_database("cat", conn, params)
            logger.info(f"{id}# cat (dist={cat_dist:.3f})")

        # Mark handled regardless of whether or not match was found.
        mark_routed(conn, id)

    return len(unrouted_rows)


def main():
    conn = connect()
    logger.info("polling for un-routed frames ...")
    while True:
        n = route_once(conn)
        if n:
            logger.info(f"processed {n} frame(s)")
        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    sys.exit(main())
