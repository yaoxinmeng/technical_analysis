import type { LayoutServerLoad } from './$types';
import { securities } from '$db/mongo';
import type { Security } from '$db/schema';

export const load: LayoutServerLoad = async ({ params }) => {
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