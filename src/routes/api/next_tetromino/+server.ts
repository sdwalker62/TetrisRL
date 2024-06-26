import { json } from '@sveltejs/kit';

let repr: string[][];

export async function POST({ request }) {
	try {
		const data = await request.json();
		repr = data.representation;
		return json({
			status: 'success',
			message: 'representation received successfully'
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
	return json({ representation: repr });
}
