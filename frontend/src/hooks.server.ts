import { type Handle, redirect } from '@sveltejs/kit';
import { start_mongo } from "$lib/functions/mongo";
import { verifyToken } from '$lib/functions/auth.server';

// Start MongoDB connection
start_mongo().then(() => {
	console.log('Mongo started');
}).catch(e => { console.error(e) })


// This hook checks if the user is authenticated before allowing access to protected routes
const EXCEPTIONS = ['*'];	// skip auth for all paths for now
export const handle: Handle = async ({ event, resolve }) => {
	// skip auth for paths in exceptions list
	for (const path of EXCEPTIONS) {
		if (path === '*' || event.url.pathname.startsWith(path)) {
			const response = await resolve(event);
			return response;
		}
	}

	// get cookies from browser
	const session = event.cookies.get('session');
	if (!session || !verifyToken(session)) {
		// If no session cookie or invalid session cookie, redirect to login
		return redirect(302, "/login")
	}

	const response = await resolve(event);
	return response;
};