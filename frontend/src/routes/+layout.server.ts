import type { LayoutServerLoad } from './$types';
import { securities, exchangeRates } from '$lib/functions/mongo';
import type { Security, ExchangeRate } from '$lib/types/schema';
import { getExchangeRate } from '$lib/functions/backend.server';

export const load: LayoutServerLoad = async () => {
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

	// retrieve relevant exchange rates from db
	let exchangeRateCursor = exchangeRates.find();
	let exchangeRateDocuments = await exchangeRateCursor.toArray();
	let exchangeRatesParsed = exchangeRateDocuments.map((doc) => {
		return {
			from: doc.from,
			to: doc.to,
			rate: doc.rate,
			date: doc.date
		} as ExchangeRate;
	});

	// if exchange rate is not in db, fetch it from the API
	let rates: { [key: string]: number } = {};
	for (let exchange of exchanges) {
		// check if exchange rate is already in db
		let existingRate = exchangeRatesParsed.find(
			(rate) => rate.from === exchange[0] && rate.to === exchange[1]
		);
		if (existingRate) {
			rates[`${exchange[0]}-${exchange[1]}`] = existingRate.rate;
			continue;
		}
		try {
			rates[`${exchange[0]}-${exchange[1]}`] = await getExchangeRate(exchange[0], exchange[1]);
			exchangeRates.insertOne({
				from: exchange[0],
				to: exchange[1],
				rate: rates[`${exchange[0]}-${exchange[1]}`],
				date: new Date().toISOString().split("T")[0]
			});
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