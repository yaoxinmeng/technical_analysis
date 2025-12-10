import type { RequestHandler } from './$types';
import { error } from '@sveltejs/kit';
import { generatePrediction } from '$lib/functions/backend.server';

export const POST: RequestHandler = async ({ request }) => {
    const data = await request.json();

    try {
        let result = await generatePrediction(data);
        return new Response(JSON.stringify(result));
    } catch (err: any) {
        error(500, err);
    }
};