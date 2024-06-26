import { json } from '@sveltejs/kit';

let level: number;

export async function POST({ request }) {
	try {
		const data = await request.json();
		level = data.level;
		return json({
			status: 'success',
			message: 'level received successfully'
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
	return json({ level: level });
}
