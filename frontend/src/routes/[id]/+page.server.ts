import type { PageServerLoad } from './$types';
import { securities } from '$lib/functions/mongo';
import type { Security } from '$lib/types/schema';

export const load: PageServerLoad = async ({ params }) => {
    let doc = await securities.findOne({
        symbol: params.id
    });
    if (!doc) {
        throw new Error(`Security with symbol ${params.id} not found`);
    }
    let parsed = {
        symbol: doc.symbol,
        name: doc.name,
        sector: doc.sector,
        exchange_currency: doc.exchange_currency,
        price: doc.price,
        financials: doc.financials,
        analysis: doc.analysis,
        assumptions: doc.assumptions
    } as Security
    return {
        security: parsed
    };
};