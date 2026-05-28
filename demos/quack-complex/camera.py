import duckdb
import sys
import torch
import uuid

from datetime import datetime
from PIL import Image
from transformers import CLIPProcessor, CLIPModel

MODEL_ID = "openai/clip-vit-base-patch32"
QUACK_TOKEN = "super_secret"


def insert_data(
    camera_id, frame_id, captured_at, embedding, frame_path, frame_uri
):  # noqa
    conn = duckdb.connect()
    conn.execute("INSTALL quack FROM core_nightly; LOAD quack;")
    conn.execute(
        f"ATTACH 'quack:localhost' AS remote_db (TOKEN '{QUACK_TOKEN}');"  # noqa
    )
    insert = conn.sql(
        f"INSERT INTO remote_db.frames (id, camera_id, captured_at, embedding, frame_path, frame_uri) values ('{frame_id}', '{camera_id}', '{captured_at}', {embedding}, '{frame_path}', '{frame_uri}')"  # noqa
    )
    return insert


def main(camera_id, frame_path, uri):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = CLIPModel.from_pretrained(MODEL_ID).to(device).eval()
    processor = CLIPProcessor.from_pretrained(MODEL_ID, use_fast=True)
    image = Image.open(frame_path).convert("RGB")

    with torch.no_grad():
        img_inputs = processor(images=image, return_tensors="pt").to(device)
        img_feats = model.get_image_features(**img_inputs)
        img_feats = img_feats / img_feats.norm(dim=-1, keepdim=True)

    embedding = img_feats.squeeze(0).cpu().tolist()
    captured_at = str(datetime.now())
    frame_id = str(uuid.uuid4())
    insert_data(camera_id, frame_id, captured_at, embedding, frame_path, uri)


if __name__ == "__main__":
    """
    usage:
    uv run main.py \
        backyard-1 \
        ~/Downloads/house-cat.jpg \
        https://double-shot-of-duck-demos.s3.us-east-1.amazonaws.com/cats/pexels-helen1-30002405.jpg
    """

    camera_id = sys.argv[1]
    frame_path = sys.argv[2]
    uri = sys.argv[3]
    sys.exit(main(camera_id=camera_id, frame_path=frame_path, uri=uri))
