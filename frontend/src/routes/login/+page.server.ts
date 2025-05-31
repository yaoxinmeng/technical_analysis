import { fail, redirect } from '@sveltejs/kit';
import type { Actions } from './$types';
import { generateToken } from "$lib/auth";

export const actions = {
	default: async ({ cookies, request }) => {
		const data = await request.formData();
        const username = data.get('username');
        const password = data.get('password');

        if (typeof username !== 'string' || typeof password !== 'string') {
            console.error('Invalid input types for username or password');
            return fail(400, { message: 'Invalid username or password' });
        }

        let token = generateToken(username, password);

        cookies.set('session', token, {
            // send cookie for every page
            path: '/',
            // server side only cookie so you can't use `document.cookie`
            httpOnly: true,
            // only requests from same site can send cookies
            // https://developer.mozilla.org/en-US/docs/Glossary/CSRF
            sameSite: 'strict',
            // set cookie to expire after a month
            maxAge: 60 * 60 * 24 * 30,
        });

        // redirect the user
        redirect(302, '/');
	}
} satisfies Actions;