import type { RequestHandler } from './$types';
import { error } from '@sveltejs/kit';
import { securities } from '$lib/functions/mongo';
import type { Security } from '$lib/types/schema';

export const POST: RequestHandler = async ({ request }) => {
    const body: {
        id: string;
        name: string;
        sector: string;
        currency: string;
    } = await request.json();
    try {
        let newSecurity: Security = {
            symbol: body.id,
            name: body.name,
            sector: body.sector,
            exchange_currency: body.currency,
            price: {
                price: 0,
                date: ""
            },
            financials: {
                currency: "",
                date: "",
                financials: []
            },
            analysis: {
                average_income: 0,
                de_ratio: 0,
                cagr: 0,
                bvps: 0,
                upper: 0,
                lower: 0,
                target: 0,
                nominal_upper: 0,
                nominal_lower: 0,
                nominal_target: 0,
            },
            assumptions: {
                growth_rate: 0,
                years: 12,
                safety_margin: 0.3
            }
        };
        await securities.insertOne(newSecurity).catch((err) => {
            error(500, err);
        });
        return new Response("Ok");
    } catch (err: any) {
        error(500, err);
    }
};