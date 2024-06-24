import random
import tomllib
from pathlib import Path

import click
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

origins = ["http://localhost", "http://localhost:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TETROMINO_IDS = ["I", "O", "T", "S", "Z", "J", "L"]
N_COLS = 10
N_ROWS = 20


def generate_random_board() -> list[list[str]]:
    return [
        [random.choice(TETROMINO_IDS) for _ in range(N_COLS)] for _ in range(N_ROWS)
    ]


def generate_random_next_tetromino() -> str:
    return [[random.choice(TETROMINO_IDS) for _ in range(4)] for _ in range(4)]


@app.get("/tetris/board")
def get_board():
    random_board = generate_random_board()
    json_data = jsonable_encoder(random_board)
    return JSONResponse(content={"board_state": json_data})


@app.get("/tetris/next_tetromino")
def get_next_tetromino():
    next_tetromino = generate_random_next_tetromino()
    json_data = jsonable_encoder(next_tetromino)
    return JSONResponse(content={"next_tetromino": json_data})


@app.get("/tetris/statistics")
def get_statistics():
    score = random.randint(0, 10_000)
    level = random.randint(0, 100)
    lines = random.randint(0, 1_000)
    json_data = jsonable_encoder({"score": score, "level": level, "lines": lines})
    return JSONResponse(content=json_data)


@app.get("/tetris/game_mode")
def get_game_mode():
    game_mode = random.choice(["ai", "human"])
    return JSONResponse(content={"game_mode": game_mode})


@click.command()
@click.option("--mode", default="bot", help="Mode of the game")
@click.option("--cfg", help="Configuration file path for algorithm")
def main(mode: str, cfg: str):
    if mode == "bot":
        assert cfg is not None, "Please provide a configuration file for the bot"
        assert Path(cfg).exists(), f"Cannot find config file at {cfg}"
        with open(cfg, "rb") as f:
            config = tomllib.load(f)
        print(config)


if __name__ == "__main__":
    main()
    # uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
