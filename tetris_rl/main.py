r"""Main gym event logic."""

import gymnasium
import requests


def manual_action_parser(key: str) -> int:
    r"""Map the keypress event to the corresponding gym action.

    ArrowLeft -> 0   (left)
    ArrowRight -> 1  (right)
    ArrowDown -> 2,  (soft-drop)
    ' ' -> 3         (hard-drop)
    ArrowUp -> 4,    (clockwise rotation)
    z -> 5           (counter-clockwise rotation)
    """
    try:
        action_id = ["ArrowLeft", "ArrowRight", "ArrowDown", " ", "ArrowUp", "z"].index(
            key,
        )
    except ValueError:
        action_id = -1
    return action_id


if __name__ == "__main__":
    MODE = "human"
    env = gymnasium.make(
        "env:Tetris-v0",
        render_mode="web_viewer",
        manual_play=MODE == "human",
    )
    env.reset()
    CONTINUE_GAME = True
    while CONTINUE_GAME:
        if MODE == "human":
            action_data = requests.get("http://localhost:8000/tetris/action", timeout=100)
            action_key = action_data.json()["action"]
            ACTION = manual_action_parser(action_key)
            playfield = env.step(ACTION)
        elif MODE == "random":
            env = gymnasium.make("env:Tetris-v0", render_mode="web_viewer", mode=MODE)
            env.reset()
            action = env.action_space.sample()
            playfield = env.step(action)
