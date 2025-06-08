import { BACKEND_URL } from '$env/static/private';

export async function getSecurityOverview(id: string) {
    const res = await fetch(`${BACKEND_URL}/finance/overview/${id}`);
    if (!res.ok) {
        throw new Error(`Failed to fetch security overview: ${res.statusText}`);
    }
    return await res.json();
}

export async function getSecurityPrice(id: string): Promise<number> {
    const res = await fetch(`${BACKEND_URL}/finance/price/${id}`);
    if (!res.ok) {
        throw new Error(`Failed to fetch security price: ${res.statusText}`);
    }
    return res.json();
}