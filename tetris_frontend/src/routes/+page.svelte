<script lang="ts">
    import Board from "$lib/components/Board.svelte";
	import Score from "$lib/components/Score.svelte";
</script>

<main>
    <enhanced:img id="tetris-logo" src="$lib/assets/imgs/tetris-logo.png" alt="Tetris Logo" />
    <div id="game">
        <Score />
        <Board />
    </div>
    
</main>


<style>
    main {
        display: flex;
        flex-direction: column;
        height: 100vh;
        width: 100vw;
        background: var(--bg-color);
        padding: 20px;
        align-items: center;
    }

    #game {
        display: flex;
        flex-direction: row;
        
    }

    #tetris-logo {
        height: 10vh;
        width: var(--size);
        padding: 10px;
        justify-self: flex-start;
    }

</style>