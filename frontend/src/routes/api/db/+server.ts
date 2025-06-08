import type { RequestHandler } from './$types';
import { error } from '@sveltejs/kit';
import { securities } from '$db/mongo';
import type { Security } from '$db/schema';

export const POST: RequestHandler = async ({ request }) => {
    const body = await request.json();
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
                currency: body.currency,
                date: "",
                balance_sheet: [],
                income_statement: []
            },
            analysis: {
                average_income: 0,
                pe_ratio: 0,
                de_ratio: 0,
                book_value_per_share: 0,
                upper: 0,
                lower: 0,
                target: 0,
                nominal_upper: 0,
                nominal_lower: 0,
                nominal_target: 0
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