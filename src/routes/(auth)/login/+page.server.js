// This server load runs during SSR. Because we set prerender = true, this
// code must be safe to run at build-time (no per-request private tokens).
export async function load({ url }) {
  // Example: return some static metadata for the login page
  return {
    title: 'Sign in'
  };
}