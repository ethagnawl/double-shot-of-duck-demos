import duckdb

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from loguru import logger # noqa
from pathlib import Path

app = FastAPI()

QUACK_TOKEN = "super_secret"


def get_animals(animal):
    if animal == "ducks":
        port = "9595"
    elif animal == "cats":
        port = "9696"
    else:
        raise Exception("No such animal")

    conn = duckdb.connect()
    conn.execute("INSTALL quack FROM core_nightly; LOAD quack;")
    conn.execute(
        f"ATTACH 'quack:localhost:{port}' AS remote_db (TOKEN '{QUACK_TOKEN}');"  # noqa
    )
    frames = conn.sql(f"select captured_at, camera_id, frame_uri from remote_db.frames")  # noqa
    animals = frames.fetchall()
    return animals



BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")

@app.get("/animals/{animal}", response_class=HTMLResponse)
async def main(request: Request, animal: str):
    animals = get_animals(animal)
    return templates.TemplateResponse(
        request=request, name="animal.html", context={
            "type": animal,
            "animals": animals
        }
    )
