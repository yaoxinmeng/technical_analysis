import type { PageServerLoad } from './$types';
import { securities } from '$db/mongo';
import type { Security } from '$db/schema';
import { getExchangeRate } from '$lib/backend.server';

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
			analysis: doc.analysis,
			assumptions: doc.assumptions
		} as Security;
	});

	// for each document, determine if an exchange rate is required
	let exchanges = parsed.filter(
		(doc) => doc.financials.currency && doc.exchange_currency !== doc.financials.currency
	).map(
		(doc) => [doc.financials.currency, doc.exchange_currency]
	);

	// retrieve relevant exchange rates
	let rates: { [key: string]: number } = {};
	for (let exchange of exchanges) {
		try {
			let rate = await getExchangeRate(exchange[0], exchange[1]);
			rates[`${exchange[0]}-${exchange[1]}`] = rate;
		} catch (err) {
			console.error(err);
			rates[`${exchange[0]}-${exchange[1]}`] = 0;
		}
	}
	return {
		securities: parsed,
		rates: rates
	};
};