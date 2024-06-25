import gymnasium
import requests


def manual_action_parser(key: str) -> int:
    r"""Map the keypress event to the corresponding gym action

    ArrowLeft -> 0   (left)
    ArrowRight -> 1  (right)
    ArrowDown -> 2,  (soft-drop)
    ' ' -> 3         (hard-drop)
    ArrowUp -> 4,    (clockwise rotation)
    z -> 5           (counter-clockwise rotation)
    """
    match key:
        case "ArrowLeft":
            return 0
        case "ArrowRight":
            return 1
        case "ArrowDown":
            return 2
        case " ":
            return 3
        case "ArrowUp":
            return 4
        case "z":
            return 5
        case _:
            return 2


if __name__ == "__main__":
    env = gymnasium.make("env:Tetris-v0", render_mode="web_viewer")
    env.reset()
    mode = "human"
    continue_game = True
    while continue_game:
        if mode == "human":
            action_data = requests.get("http://localhost:8000/tetris/action")
            key = action_data.json()["action"]
            action = manual_action_parser(key)
            playfield = env.step(action)
        elif mode == "random":
            action = env.action_space.sample()
            playfield = env.step(action)
