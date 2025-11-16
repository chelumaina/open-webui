// Server-side dummy data (SSR). Replace with DB/API later.
// src/routes/+page.ts
import { error } from '@sveltejs/kit';
export async function load({ fetch }) {
  let content = '';
  return { content };
}