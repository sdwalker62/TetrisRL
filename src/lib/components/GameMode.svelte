<script lang="ts">
	export let gameMode: string = 'ai';
	import { Joystick, Bot } from 'lucide-svelte';
	import * as Card from '$lib/components/ui/card';
	import { Description } from 'formsnap';
</script>

<Card.Root class="min-w-full">
	<Card.Header>Current Mode</Card.Header>
	<Card.Description class="text-center">Brain behind the game</Card.Description>
	<Card.Content class="flex flex-col items-center">
		<p class="game-mode-text">{gameMode}</p>
		{#if gameMode === 'human'}
			<Joystick color="#eeeeee" size="72" />
		{:else}
			<Bot color="#eeeeee" size="72" />
		{/if}
	</Card.Content>
</Card.Root>

<style lang="scss">
	.game-mode-text {
		font-family: 'Roboto Mono', monospace;
		font-optical-sizing: auto;
		font-style: normal;
		font-weight: 400;
		padding: 10px;
		min-width: 200px;
		color: #eeeeee;
		text-align: center;
		font-size: 2rem;
	}
</style>
