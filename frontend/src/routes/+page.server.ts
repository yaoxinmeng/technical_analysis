import type { PageServerLoad } from './$types';
import { securities } from '$db/mongo';

export const load: PageServerLoad = async () => {
    let cursor = securities.find();
    let documents = await cursor.toArray();
	return {
		securities: documents
	};
};