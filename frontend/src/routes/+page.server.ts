import type { PageServerLoad, Actions } from './$types';
import db from '$db/mongo';

export const load: PageServerLoad = async () => {
    let cursor = db.collection('favourites').find();
    let favourites = await cursor.toArray();
	return {
		favourites: favourites
	};
};