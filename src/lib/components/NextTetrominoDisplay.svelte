<script lang="ts">
	import _ from 'lodash';
	import Tile from './Tile.svelte';
	import * as Card from '$lib/components/ui/card';

	const tetromino_id_strings = ['I', 'O', 'T', 'J', 'L', 'S', 'Z', 'E'];
	// create a random board for testing if not provided one
	export let board: string[][] = _.times(4, () =>
		_.times(4, () => _.sample(tetromino_id_strings)!)
	);
</script>

<Card.Root class="min-w-full">
	<Card.Header>Upcomming Tetromino</Card.Header>
	<Card.Content>
		<div id="display-grid">
			{#each board as row}
				{#each row as id}
					<Tile tetromino_id={id} />
				{/each}
			{/each}
		</div>
	</Card.Content>
</Card.Root>

<style lang="scss">
	#display-grid {
		display: grid;
		column-gap: 0;
		row-gap: 0;
		grid-template-columns: repeat(4, calc(90vh / 20));
		grid-template-rows: repeat(4, calc(90vh / 20));
		background-color: #1f1f1f;
	}
</style>
