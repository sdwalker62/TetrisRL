import { json } from '@sveltejs/kit';

let boardState: string[][];

export async function POST({ request }) {
	try {
		const data = await request.json();
		boardState = data.board_state;
		return json({
			status: 'success',
			message: 'Board state received successfully'
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
	return json({ boardState: boardState });
}
