import gymnasium

gymnasium.register(
    id="Tetris-v0",
    entry_point="tetris_rl.env.tetris_env:TetrisEnv",
)
