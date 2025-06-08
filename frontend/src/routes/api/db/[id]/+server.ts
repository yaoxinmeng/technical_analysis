import type { RequestHandler } from './$types';
import { error } from '@sveltejs/kit';
import { securities } from '$db/mongo';
import type { Security } from '$db/schema';

export const PUT: RequestHandler = async ({ request, params }) => {
    const body: Security = await request.json();
    const symbol = params.id;
    try {
        await securities.findOneAndUpdate(
            {
                symbol: symbol
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

export const DELETE: RequestHandler = async ({ params }) => {
    const symbol = params.id;
    try {
        await securities.findOneAndDelete({
            symbol: symbol
        }).catch((err) => {
            error(500, err);
        }); 
        return new Response("Ok");
    }
    catch (err: any) {
        error(500, err);
    }
}
