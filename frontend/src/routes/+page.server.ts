import type { PageServerLoad } from './$types';
import { securities } from '$db/mongo';
import type { Security } from '$db/schema';

export const load: PageServerLoad = async () => {
    let cursor = securities.find();
    let documents = await cursor.toArray();
	let parsed = documents.map((doc) => {
		return {
			symbol: doc.symbol,
			name: doc.name,
			sector: doc.sector,
			exchange_currency: doc.exchange_currency,
			price: doc.price,
			financials: doc.financials,
			analysis: doc.analysis
		} as Security;
	});
	return {
		securities: parsed
	};
};