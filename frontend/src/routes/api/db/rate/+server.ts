import type { RequestHandler } from './$types';
import { error } from '@sveltejs/kit';
import { exchangeRates } from '$db/mongo';
import type { ExchangeRate } from '$db/schema';

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