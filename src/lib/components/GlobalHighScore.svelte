<script lang="ts">
	import * as Table from '$lib/components/ui/table/index.js';

	const modelHistory = [
		{
			episode_id: '0',
			author: 'Player One',
			modelID: 'AS123VAE',
			algorithm: 'PPO',
			score: 100
		},
		{
			episode_id: '1',
			author: 'Player One',
			modelID: 'AS123VAE',
			algorithm: 'PPO',
			score: 100
		},
		{
			episode_id: '2',
			author: 'Player One',
			modelID: 'AS123VAE',
			algorithm: 'PPO',
			score: 100
		},
		{
			episode_id: '3',
			author: 'Player One',
			modelID: 'AS123VAE',
			algorithm: 'PPO',
			score: 100
		},
		{
			episode_id: '4',
			author: 'Player One',
			modelID: 'AS123VAE',
			algorithm: 'PPO',
			score: 100
		},
		{
			episode_id: '5',
			author: 'Player One',
			modelID: 'AS123VAE',
			algorithm: 'PPO',
			score: 100
		},
		{
			episode_id: '6',
			author: 'Player One',
			modelID: 'AS123VAE',
			algorithm: 'PPO',
			score: 100
		}
	];
</script>

<Table.Root>
	<Table.Caption>Personal Model Performance History</Table.Caption>
	<Table.Header>
		<Table.Row>
			<Table.Head class="w-[100px]">Episode ID</Table.Head>
			<Table.Head>Author</Table.Head>
			<Table.Head>Model ID</Table.Head>
			<Table.Head>Algorithm</Table.Head>
			<Table.Head class="text-right">Score</Table.Head>
		</Table.Row>
	</Table.Header>
	<Table.Body>
		{#each modelHistory as history, i (i)}
			<Table.Row>
				<Table.Cell class="font-medium">{history.episode_id}</Table.Cell>
				<Table.Cell>{history.author}</Table.Cell>
				<Table.Cell>{history.modelID}</Table.Cell>
				<Table.Cell>{history.algorithm}</Table.Cell>
				<Table.Cell class="text-right">{history.score}</Table.Cell>
			</Table.Row>
		{/each}
	</Table.Body>
</Table.Root>
