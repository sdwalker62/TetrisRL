<script lang="ts">
    import Board from "$lib/components/Board.svelte";
	import Score from "$lib/components/Score.svelte";
    import NextTetrominoDisplay from "$lib/components/NextTetrominoDisplay.svelte";
	import GameMode from "$lib/components/GameMode.svelte";
    import type { PageData } from './$types';
    export let data: PageData;

    console.log(data);
</script>

<main>
    <enhanced:img id="tetris-logo" src="$lib/assets/imgs/tetris-logo.png" alt="Tetris Logo" />
    <div id="game">
        <div id="sidebar">
            <Score />
            <NextTetrominoDisplay />
            <GameMode />
        </div>
        <Board />
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