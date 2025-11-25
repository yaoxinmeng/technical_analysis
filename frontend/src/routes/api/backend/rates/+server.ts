import type { RequestHandler } from './$types';
import { error } from '@sveltejs/kit';
import { getExchangeRate } from '$lib/functions/backend.server';

export const GET: RequestHandler = async ({ url }) => {
    const curr1 = url.searchParams.get('curr1');
    const curr2 = url.searchParams.get('curr2');

    if (!curr1 || !curr2) {
        error(400, 'Missing params');
    }
    try {
        let result = await getExchangeRate(curr1, curr2);
        return new Response(JSON.stringify(result));
    } catch (err: any) {
        error(500, err);
    }
};