r"""This module defines the middleware server that collects episode information
and sends it to the frontend for rendering.
"""

import datetime

import numpy as np
import requests
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

origins = ["http://localhost", "http://localhost:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TETROMINO_IDS = ["E", "I", "O", "T", "S", "Z", "J", "L"]
N_COLS = 10
N_ROWS = 20
TIMEOUT = 10

render_frames = []
action_buffer = []


@app.post("/tetris/next_tetromino")
async def send_next_tetromino(next_tetromino_data: Request):
    r"""Send the next tetromino to the frontend for rendering"""
    next_tetromino = await next_tetromino_data.json()
    arr = np.array(next_tetromino["representation"])
    arr = np.where(arr == 0.0, "E", arr)
    arr = np.where(arr == "1", "I", arr)
    arr = np.where(arr == "2", "J", arr)
    arr = np.where(arr == "3", "L", arr)
    arr = np.where(arr == "4", "O", arr)
    arr = np.where(arr == "5", "S", arr)
    arr = np.where(arr == "6", "T", arr)
    arr = np.where(arr == "7", "Z", arr)
    requests.post(
        "http://localhost:5173/api/next_tetromino",
        json={"representation": arr.tolist()},
        headers={"Content-Type": "application/json"},
        timeout=TIMEOUT,
    )


@app.post("/tetris/frame")
async def add_frame(frame_data: Request):
    r"""Converts the playfield frame to a format the Svelte can use"""
    data = await frame_data.json()

    # convert indices to tetromino ids
    arr = np.array(data["board"])
    arr = np.where(arr == 0.0, "E", arr)
    arr = np.where(arr == "1.0", "I", arr)
    arr = np.where(arr == "2.0", "J", arr)
    arr = np.where(arr == "3.0", "L", arr)
    arr = np.where(arr == "4.0", "O", arr)
    arr = np.where(arr == "5.0", "S", arr)
    arr = np.where(arr == "6.0", "T", arr)
    arr = np.where(arr == "7.0", "Z", arr)
    render_frames.append(arr.tolist())
    headers = {"Content-Type": "application/json"}
    requests.post(
        "http://localhost:5173/api/render",
        json={"board_state": arr.tolist()},
        headers=headers,
        timeout=TIMEOUT,
    )


@app.post("/tetris/mode")
async def add_mode(mode: Request):
    r"""Sends the current play mode to the ui"""
    data = await mode.json()
    requests.post(
        "http://localhost:5173/api/mode",
        json={"mode": data["mode"]},
        headers={"Content-Type": "application/json"},
        timeout=TIMEOUT,
    )


@app.post("/tetris/stats")
async def add_statistics(stats: Request):
    r"""Pushes game statistics updates to be parsed by the stream reader"""
    data = await stats.json()
    score = data["score"]
    level = data["level"]
    lines_cleared = data["lines_cleared"]

    headers = {"Content-Type": "application/json"}

    requests.post(
        "http://localhost:5173/api/statistics/level",
        json={"level": level},
        headers=headers,
        timeout=TIMEOUT,
    )

    requests.post(
        "http://localhost:5173/api/statistics/score",
        json={"score": score},
        headers=headers,
        timeout=TIMEOUT,
    )

    requests.post(
        "http://localhost:5173/api/statistics/lines_cleared",
        json={"linesCleared": lines_cleared},
        headers=headers,
        timeout=TIMEOUT,
    )


class KeypressEvent(BaseModel):
    r"""Datafields for each time a key is pressed"""

    key: str
    timestamp: datetime.datetime


@app.post("/tetris/keypress")
async def receive_keypress(keypress_event: KeypressEvent):
    r"""Gets the key press event from the user"""
    key = keypress_event.key
    timestamp = keypress_event.timestamp
    action_buffer.append((key, timestamp))
    print(f"Registered action: {key} at {timestamp}")
    return JSONResponse(content={"status": "success"})


@app.get("/tetris/action")
async def get_action():
    r"""MIGHT GET REMOVED"""
    if len(action_buffer) == 0:
        return JSONResponse(content={"action": "none"})
    action = action_buffer.pop(0)
    return JSONResponse(content={"action": action[0]})


class ClearActionEvent(BaseModel):
    r"""Clears the current action buffer"""

    should_clear: bool


@app.post("/tetris/clear_action_buffer")
async def clear_action_buffer(data: ClearActionEvent):
    r"""Clears the action buffer between episodes"""
    if data.should_clear:
        action_buffer.clear()
    return JSONResponse(content={"status": "success"})


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
