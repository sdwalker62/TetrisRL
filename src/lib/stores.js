import { writable } from 'svelte/store';

export const boardState = writable(null);
export const score = writable(0);
export const linesCleared = writable(0);
export const level = writable(0);
export const nextTetromino = writable(null);
export const mode = writable('');
