import {MongoClient} from 'mongodb';
import { MONGO_HOST, MONGO_PORT, MONGO_USERNAME, MONGO_PASSWORD } from '$env/static/private'; 

const client = new MongoClient(`mongodb://${MONGO_USERNAME}:${MONGO_PASSWORD}@${MONGO_HOST}:${MONGO_PORT}`)

export function start_mongo() {
	console.log('Starting mongo...');
	return client.connect();
}

export default client.db("finance");

export const securities = client.db("finance").collection('securities');