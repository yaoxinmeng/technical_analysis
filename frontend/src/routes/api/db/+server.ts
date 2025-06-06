import type { RequestHandler } from './$types';
import { error } from '@sveltejs/kit';
import { securities } from '$db/mongo';

export const POST: RequestHandler = async ({ request }) => {
    const body = await request.json();
    try {
        let newSecurity = {
            symbol: body.id,
            name: body.name,
            sector: body.sector,
            exchange_currency: body.currency,
            financials: {},
            analysis: {}
        };
        await securities.insertOne(newSecurity).catch((err) => {
            error(500, err);
        });
        return new Response("Ok");
    } catch (err: any) {
        error(500, err);
    }
};