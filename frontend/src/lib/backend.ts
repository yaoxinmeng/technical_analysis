import { BACKEND_URL } from '$env/static/private';

export async function getSecurityOverview(id: string) {
    return fetch(`${BACKEND_URL}/finance/overview/${id}`).then(res => res.json());
}

export async function getSecurityPrice(id: string) {
    return fetch(`${BACKEND_URL}/finance/price/${id}`).then(res => res.json());
}