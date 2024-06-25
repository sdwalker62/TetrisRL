<script lang="ts">
	import _ from 'lodash';
	import Tile from './Tile.svelte';

	const tetromino_id_strings = ['I', 'O', 'T', 'J', 'L', 'S', 'Z', 'E'];
	// create a random board for testing if not provided one
	export let board: string[][] = _.times(20, () => _.times(10, () => 'E'));
</script>

<main>
	{#each board as row}
		{#each row as id}
			<Tile tetromino_id={id} />
		{/each}
	{/each}
</main>

<style lang="scss">
	main {
		display: grid;
		column-gap: 0;
		row-gap: 0;
		grid-template-columns: repeat(10, calc(90vh / 20));
		grid-template-rows: repeat(20, calc(90vh / 20));
		padding: 10px;
		border-radius: 7px;
		border: 3px solid darken(#eeeeee, 20%);
		margin: 0 0 0 20px;
		height: fit-content;
	}
</style>
