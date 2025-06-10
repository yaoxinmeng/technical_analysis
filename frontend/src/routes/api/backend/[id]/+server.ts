import type { RequestHandler } from './$types';
import { error } from '@sveltejs/kit';
import { getSecurityOverview, getSecurityPrice, getSecurityFinancials } from '$lib/backend.server';

export const GET: RequestHandler = async ({ url, params }) => {
    const info = url.searchParams.get('info');

    if (!info) {
        error(400, 'Missing info param');
    }
    try {
        let result = {};
        switch (info) {
            case 'overview':
                result = await getSecurityOverview(params.id);
                break;
            case 'price':
                result = await getSecurityPrice(params.id);
                break;
            case 'financials':
                result = await getSecurityFinancials(params.id);
                break;
            default:
                throw new Error('Invalid info param');
        }
        return new Response(JSON.stringify(result));
    } catch (err: any) {
        error(500, err);
    }
};