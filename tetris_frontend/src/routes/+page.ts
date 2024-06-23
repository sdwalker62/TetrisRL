import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch, setHeaders }) => {
	const url = `http://localhost:8000/tetris/board`;
	const response = await fetch(url);

	// cache the page for the same length of time
	// as the underlying data
	setHeaders({
		age: response.headers.get('age'),
		'cache-control': response.headers.get('cache-control')
	});

	console.log(response);
	return response.json();
};
