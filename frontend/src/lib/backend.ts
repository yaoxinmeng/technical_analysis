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

export async function getSecurityFinancials(id: string) {
    const res = await fetch(`${BACKEND_URL}/finance/financials/${id}`);
    if (!res.ok) {
        throw new Error(`Failed to fetch security financials: ${res.statusText}`);
    }
    return await res.json();
}


export async function getExchangeRate(curr1: string, curr2: string) {
    const res = await fetch(`${BACKEND_URL}/exchange/${curr1}/${curr2}`);
    if (!res.ok) {
        throw new Error(`Failed to fetch exchange rate: ${res.statusText}`);
    }
    return await res.json();
}