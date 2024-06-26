import { json } from '@sveltejs/kit';

let mode: string;

export async function POST({ request }) {
	try {
		const data = await request.json();
		mode = data.mode;
		return json({
			status: 'success',
			message: 'mode received successfully'
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
	return json({ mode: mode });
}
