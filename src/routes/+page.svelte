<script lang="ts">
	import Board from '$lib/components/Board.svelte';
	import Score from '$lib/components/Score.svelte';
	import NextTetrominoDisplay from '$lib/components/NextTetrominoDisplay.svelte';
	import GameMode from '$lib/components/GameMode.svelte';
	import { onMount } from 'svelte';
	import { Separator } from '$lib/components/ui/separator';
	import Sun from 'svelte-radix/Sun.svelte';
	import Moon from 'svelte-radix/Moon.svelte';
	import { toggleMode } from 'mode-watcher';
	import { Button } from '$lib/components/ui/button/index.js';
	import * as Menubar from '$lib/components/ui/menubar';
	import * as Tabs from '$lib/components/ui/tabs/index.js';
	import PersonalHighScore from '$lib/components/PersonalHighScore.svelte';
	import GlobalHighScore from '$lib/components/GlobalHighScore.svelte';
	import { boardState, linesCleared, score, level, nextTetromino, mode } from '$lib/stores';
	import _ from 'lodash';

	class StreamReader {
		attribute: string;
		storeValue: any;
		url: string;
		isArray: boolean;
		aborter: AbortController;

		constructor(attribute: string, storeValue: any, url: string, isArray = false) {
			this.attribute = attribute;
			this.storeValue = storeValue;
			this.url = url;
			this.isArray = isArray;
			this.aborter = new AbortController();
		}

		async readStream() {
			let previousChunk = null;
			while (true) {
				try {
					const response = await fetch(this.url, this.aborter);
					// @ts-ignore
					for await (const chunk of response.body!) {
						const decodedChunkString = new TextDecoder().decode(chunk);
						let decodedChunk = JSON.parse(decodedChunkString);
						// Check if chunk contains non-null data, skip otherwise
						if (Object.keys(decodedChunk).includes(this.attribute)) {
							// Initialize previousChunk with first chunk
							const attributeValue = decodedChunk[this.attribute];
							if (!previousChunk) {
								previousChunk = decodedChunk;
								this.storeValue.set(attributeValue);
							}
							const prevValue = previousChunk[this.attribute];
							if (this.isArray) {
								// Check if arrays are equal
								if (!_.isEqual(attributeValue, prevValue)) {
									this.storeValue.set(attributeValue);
									previousChunk = decodedChunk;
								}
							} else {
								// Check if values are equal
								if (attributeValue !== prevValue) {
									this.storeValue.set(attributeValue);
									previousChunk = decodedChunk;
								}
							}
						}
					}
				} catch (e) {
					if (e instanceof TypeError) {
						console.error(e);
						console.error('TypeError: Browser may not support async iteration');
					} else {
						console.error(`Error in async iterator: ${e}.`);
					}
				}
			}
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

		const boardStreamer = new StreamReader('boardState', boardState, '/api/render/', true);
		const nextTetrominoStream = new StreamReader(
			'representation',
			nextTetromino,
			'/api/next_tetromino/',
			true
		);
		const modeStreamer = new StreamReader('mode', mode, '/api/mode/');
		const scoreStreamer = new StreamReader('score', score, '/api/statistics/score/');
		const linesClearedStreamer = new StreamReader(
			'linesCleared',
			linesCleared,
			'/api/statistics/lines_cleared/'
		);
		const levelStreamer = new StreamReader('level', level, '/api/statistics/level/');

		boardStreamer.readStream();
		nextTetrominoStream.readStream();
		modeStreamer.readStream();
		scoreStreamer.readStream();
		linesClearedStreamer.readStream();
		levelStreamer.readStream();

		return () => {
			document.removeEventListener('keydown', handleKeyPress);
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
		{#key $score}
			<Score score={$score} level={$level} lines={$linesCleared} />
		{/key}
		{#key $nextTetromino}
			{#if $nextTetromino}
				<NextTetrominoDisplay board={$nextTetromino} />
			{/if}
		{/key}
		{#key $mode}
			<GameMode gameMode={$mode} />
		{/key}
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
