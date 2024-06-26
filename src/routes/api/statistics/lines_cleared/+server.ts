import { json } from '@sveltejs/kit';

let linesCleared: number;

export async function POST({ request }) {
	try {
		const data = await request.json();
		linesCleared = data.linesCleared;
		return json({
			status: 'success',
			message: 'lines cleared received successfully'
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
	return json({ linesCleared: linesCleared });
}
