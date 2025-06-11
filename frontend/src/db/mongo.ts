import {MongoClient} from 'mongodb';
import { env } from '$env/dynamic/private'; 

const client = new MongoClient(`mongodb://${env.MONGO_USERNAME}:${env.MONGO_PASSWORD}@${env.MONGO_HOST}:${env.MONGO_PORT}`)

export function start_mongo() {
	console.log('Starting mongo...');
	return client.connect();
}

export default client.db("finance");

export const securities = client.db("finance").collection('securities');