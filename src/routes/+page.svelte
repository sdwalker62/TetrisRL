<script lang="ts">
	import Board from '$lib/components/Board.svelte';
	import Score from '$lib/components/Score.svelte';
	import NextTetrominoDisplay from '$lib/components/NextTetrominoDisplay.svelte';
	import GameMode from '$lib/components/GameMode.svelte';
	import { onMount } from 'svelte';
	import type { PageData } from './$types';
	import { Separator } from '$lib/components/ui/separator';
	import Sun from 'svelte-radix/Sun.svelte';
	import Moon from 'svelte-radix/Moon.svelte';
	import { toggleMode } from 'mode-watcher';
	import { Button } from '$lib/components/ui/button/index.js';
	import * as Menubar from '$lib/components/ui/menubar';
	import * as Tabs from '$lib/components/ui/tabs/index.js';
	import PersonalHighScore from '$lib/components/PersonalHighScore.svelte';
	import GlobalHighScore from '$lib/components/GlobalHighScore.svelte';
	import { boardState } from '$lib/stores';

	let board_state: string[][];
	let next_tetromino_state: string[][];
	let score: number = 0;
	let level: number = 0;
	let lines: number = 0;
	let game_mode: string;

	const FPS = 60;
	const INTERVAL = 1000 / FPS;
	// const INTERVAL = 500;

	async function fetchBoardState() {
		try {
			const response = await fetch('/api/render', {
				method: 'GET',
				headers: {
					'Content-Type': 'application/json'
				}
			});
			const data = await response.json();
			boardState.set(data.boardState);
		} catch (error) {
			console.error('Error fetching board state:', error);
		}
	}

	async function handleKeyPress(event: KeyboardEvent) {
		const data = {
			key: event.key,
			timestamp: new Date().toISOString()
		};

		try {
			const response = await fetch('/api/keypress', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(data)
			});

			if (!response.ok) {
				throw new Error('Collector middleware failed to log keypress event.');
			}

			const result = await response.json();
		} catch (error) {
			console.error('Error:', error);
		}
	}

	onMount(() => {
		document.addEventListener('keydown', handleKeyPress);
		const interval = setInterval(async () => {
			// const board_response = await fetch('http://localhost:8000/tetris/board');
			// const board_data = await board_response.json();
			fetchBoardState();

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
		}, INTERVAL);
		return () => {
			document.removeEventListener('keydown', handleKeyPress);
			clearInterval(interval);
		};
	});
</script>

<main>
	<div class="flex flex-col items-center gap-1 p-1">
		<Menubar.Root class="self-start">
			<Menubar.Menu>
				<Button on:click={toggleMode} variant="outline" size="icon">
					<Sun
						class="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0"
					/>
					<Moon
						class="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100"
					/>
					<span class="sr-only">Toggle theme</span>
				</Button>
			</Menubar.Menu>
		</Menubar.Root>
		<enhanced:img
			id="tetris-logo"
			src="$lib/assets/imgs/tetris-logo.png"
			alt="Tetris Logo"
			class="p-4"
		/>
		<Score {score} {level} {lines} />
		{#key next_tetromino_state}
			<NextTetrominoDisplay board={next_tetromino_state} />
		{/key}
		<GameMode gameMode={game_mode} />
	</div>
	<Separator class=" h-screen" orientation={'vertical'} />
	<div id="tabs" class="flex w-full flex-col items-center justify-items-center p-1">
		<Tabs.Root value="game" class="w-full">
			<Tabs.List>
				<Tabs.Trigger value="game">Game</Tabs.Trigger>
				<Tabs.Trigger value="model-stats">Model Statistics</Tabs.Trigger>
				<Tabs.Trigger value="personal-high-score">Personal High Score</Tabs.Trigger>
				<Tabs.Trigger value="global-high-score">Global High Score</Tabs.Trigger>
			</Tabs.List>
			<Tabs.Content value="game">
				<div class="flex w-full flex-col place-items-center p-4">
					{#key $boardState}
						{#if $boardState}
							<Board board={$boardState} />
						{/if}
					{/key}
				</div>
			</Tabs.Content>
			<Tabs.Content value="model-stats">TBD</Tabs.Content>
			<Tabs.Content value="personal-high-score"><PersonalHighScore /></Tabs.Content>
			<Tabs.Content value="global-high-score"><GlobalHighScore /></Tabs.Content>
		</Tabs.Root>
	</div>
</main>

<style>
	main {
		display: flex;
		flex-direction: row;
		height: 100vh;
		width: 100vw;
		background: var(--bg-color);
	}

	#tabs {
		display: flex;
		flex-direction: column;
		align-items: center;
		width: 100%;
	}

	#tetris-logo {
		height: 15vh;
		width: var(--size);
		justify-self: flex-start;
	}
</style>
