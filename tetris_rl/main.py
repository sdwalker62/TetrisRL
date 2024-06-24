import gymnasium

if __name__ == "__main__":
    env = gymnasium.make("env:Tetris-v0", render_mode="web_viewer")
    env.reset()
    while True:
        action = 0
        playfield = env.step(action)
