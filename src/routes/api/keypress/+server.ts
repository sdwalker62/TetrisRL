import { json } from '@sveltejs/kit';
import axios from 'axios';

export async function POST({ request }) {
	const data = await request.json();
	const url = 'http://127.0.0.1:8000/tetris/keypress';
	try {
		const response = await axios.post(url, data, {
			headers: {
				'Content-Type': 'application/json'
			}
		});
		return json(response.data);
	} catch (error) {
		console.error('Error:', error);
		throw error;
	}
}
