import { json } from '@sveltejs/kit';

let score: number;

export async function POST({ request }) {
	try {
		const data = await request.json();
		score = data.score;
		return json({
			status: 'success',
			message: 'score received successfully'
		});
	} catch (error) {
		console.error('Error processing request:', error);
		return json(
			{
				status: 'error',
				message: 'Failed to process the request'
			},
			{ status: 400 }
		);
	}
}

export function GET() {
	return json({ score: score });
}
