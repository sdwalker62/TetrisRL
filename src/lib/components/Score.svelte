<script lang="ts">
	import * as Card from '$lib/components/ui/card';

	export let score: number = 0;
	export let level: number = 0;
	export let lines: number = 0;

	function padAndColorize(num: number): string {
		const paddedVal = num.toString().padStart(10, '0');
		const splitVal = paddedVal.split('');
		const firstNonZeroIndex = splitVal.findIndex((char) => char !== '0');
		if (num !== 0) {
			let newArr = splitVal.map((char, index) => {
				if (index < firstNonZeroIndex) {
					return `<span class="zero">${char}</span>`;
				} else {
					return `<span class="non-zero">${char}</span>`;
				}
			});
			return newArr.join('');
		} else {
			return `<span class="zero">${paddedVal}</span>`;
		}
	}
</script>

<Card.Root class="min-w-full">
	<Card.Header>Statistics</Card.Header>
	<Card.Description class="text-center">Current episode statistics</Card.Description>
	<Card.Content>
		<h1 class="text-xl">Score</h1>
		<p class="stat-text">{@html padAndColorize(score)}</p>
		<h2>Level</h2>
		<p class="stat-text-2">{@html padAndColorize(level)}</p>
		<h2>Lines</h2>
		<p class="stat-text-2">{@html padAndColorize(lines)}</p>
	</Card.Content>
</Card.Root>

<style lang="scss">
	:global(.zero) {
		color: darken(#eeeeee, 80%);
	}

	:global(.non-zero) {
		color: #eeeeee;
	}

	.stat-text,
	.stat-text-2 {
		color: darken(#eeeeee, 80%);
	}

	// h1, h2 {
	//     color: #eeeeee;
	//     font-family: "Inter", sans-serif;
	//     font-optical-sizing: auto;
	//     font-weight: medium;
	//     font-style: normal;
	//     font-variation-settings:
	//         "slnt" 0;
	// }

	// h1 {
	//     font-style: 800;
	//     font-size: 2rem;
	// }

	// h2 {
	//     font-style: 400;
	//     font-size: 1rem;

	// }

	.stat-text,
	.stat-text-2 {
		font-family: 'Roboto Mono', monospace;
		font-optical-sizing: auto;
		font-style: normal;
		font-weight: 400;
		padding: 10px;
		min-width: 200px;
		border-radius: 7px;
		background: #141414;
	}

	.stat-text {
		font-size: 2rem;
	}

	.stat-text-2 {
		font-size: 1rem;
	}
</style>
