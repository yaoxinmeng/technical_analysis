import { type Handle, redirect } from '@sveltejs/kit';
import { start_mongo } from "$db/mongo";
import { verifyToken } from '$lib/auth';

// Start MongoDB connection
start_mongo().then(() => {
	console.log('Mongo started');
}).catch(e => {console.error(e)})

// This hook checks if the user is authenticated before allowing access to protected routes
export const handle: Handle = async ({ event, resolve }) => {
	// skip auth for login page
	if (event.url.pathname.startsWith('/login')) {
		const response = await resolve(event);
		return response;
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