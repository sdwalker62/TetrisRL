<script lang="ts">
    import Board from "$lib/components/Board.svelte";
	import Score from "$lib/components/Score.svelte";
    import NextTetrominoDisplay from "$lib/components/NextTetrominoDisplay.svelte";
	import GameMode from "$lib/components/GameMode.svelte";
    import { onMount } from 'svelte';
    import type { PageData } from './$types';

    let board_state: string[][];
    let next_tetromino_state: string[][];
    let score: number = 0;
    let level: number = 0;
    let lines: number = 0;
    let game_mode: string;

    const FPS = 60;
    // const INTERVAL = 1000 / FPS;
    const INTERVAL = 1500;

    onMount(() => {
        const interval = setInterval(async () => {
            const board_response = await fetch('http://localhost:8000/tetris/board');
            const board_data = await board_response.json();
            board_state = board_data.board_state;

            const next_tetromino_response = await fetch('http://localhost:8000/tetris/next_tetromino');
            const next_tetromino_data = await next_tetromino_response.json();
            next_tetromino_state = next_tetromino_data.next_tetromino;

            const stats_response = await fetch('http://localhost:8000/tetris/statistics');
            const stats_data = await stats_response.json();
            score = stats_data.score;
            level = stats_data.level;
            lines = stats_data.lines;

            const game_mode_response = await fetch('http://localhost:8000/tetris/game_mode');
            const game_mode_data = await game_mode_response.json();
            game_mode = game_mode_data.game_mode;
        } , INTERVAL);
        return () => clearInterval(interval);
    });
</script>

<main>
    <enhanced:img id="tetris-logo" src="$lib/assets/imgs/tetris-logo.png" alt="Tetris Logo" />
    <div id="game">
        <div id="sidebar">
            <Score score={score} level={level} lines={lines}/>
            {#key next_tetromino_state}
                <NextTetrominoDisplay board={next_tetromino_state}/>
            {/key}
            <GameMode gameMode = {game_mode}/>
        </div>
        {#key board_state}
            <Board board={board_state}/>
        {/key}
    </div>
    
</main>


<style>
    main {
        display: flex;
        flex-direction: column;
        gap: 0px;
        height: 100vh;
        width: 100vw;
        background: var(--bg-color);
        padding: 0px;
        align-items: center;
    }

    #game {
        display: flex;
        flex-direction: row;
        
    }

    #sidebar {
        display: flex;
        flex-direction: column;
        gap: 0px;
    }

    #tetris-logo {
        height: 10vh;
        width: var(--size);
        padding: 20px;
        justify-self: flex-start;
    }

</style>