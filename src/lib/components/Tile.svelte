<script lang="ts">
	import { onMount } from 'svelte';

	export let tetromino_id: string;
	let tile: HTMLDivElement;

	onMount(() => {
		tile.classList.add(tetromino_id);
	});
</script>

<div bind:this={tile} class="tile" class:tetromino_id />

<style lang="scss">
	.tile {
		height: calc(90vh / 20);
		width: calc(90vh / 20);
	}

	:global(.tile.I) {
		background: #00f0f0;
		box-shadow:
			5px 5px lighten(#00f0f0, 20%) inset,
			-5px -5px darken(#00f0f0, 20%) inset;
	}

	:global(.tile.O) {
		background: #f0f000;
		box-shadow:
			5px 5px lighten(#f0f000, 20%) inset,
			-5px -5px darken(#f0f000, 20%) inset;
	}

	:global(.tile.T) {
		background: #a000f0;
		box-shadow:
			5px 5px lighten(#a000f0, 20%) inset,
			-5px -5px darken(#a000f0, 20%) inset;
	}

	:global(.tile.J) {
		background: #0000f0;
		box-shadow:
			5px 5px lighten(#0000f0, 20%) inset,
			-5px -5px darken(#0000f0, 20%) inset;
	}

	:global(.tile.L) {
		background: #f0a000;
		box-shadow:
			5px 5px lighten(#f0a000, 20%) inset,
			-5px -5px darken(#f0a000, 20%) inset;
	}

	:global(.tile.S) {
		background: #00f000;
		box-shadow:
			5px 5px lighten(#00f000, 20%) inset,
			-5px -5px darken(#00f000, 20%) inset;
	}

	:global(.tile.Z) {
		background: #f00000;
		box-shadow:
			5px 5px lighten(#f00000, 20%) inset,
			-5px -5px darken(#f00000, 20%) inset;
	}

	:global(.tile.E) {
		background: #1f1f1f;
	}
</style>
