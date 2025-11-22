export const prerender = false; // built at build time
export const ssr = false;
export async function load({ params }) {
  // normally only visible to logged-in authors
  const draft = { title: 'WIP', html: '<p>Work in progress</p>' };
  return { draft };
}