import type { RequestHandler } from './$types';
import { error } from '@sveltejs/kit';
import { exchangeRates } from '$lib/functions/mongo';
import type { ExchangeRate } from '$lib/types/schema';

export const PUT: RequestHandler = async ({ request }) => {
    const body: ExchangeRate = await request.json();
    try {
        await exchangeRates.findOneAndUpdate(
            {
                from: body.from,
                to: body.to
            }, 
            {
                $set: body
            }, 
            {
                upsert: false
            }
        ).catch((err) => {
            error(500, err);
        })
        return new Response("Ok");
    } catch (err: any) {
        error(500, err);
    }
};