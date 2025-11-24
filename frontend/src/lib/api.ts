import type { Security } from "$db/schema";

export async function saveSecurityOverview(securityId: string, name: string, sector: string, currency: string) {
    const res = await fetch(`/api/db`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            id: securityId,
            name: name,
            sector: sector,
            currency: currency,
        }),
    });
    if (!res.ok) {
        throw new Error(`Failed to save security: ${res.statusText}`);
    }
}

export async function updateSecurity(security: Security) {
    const res = await fetch(`/api/db/${security.symbol}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(security),
    });
    if (!res.ok) {
        throw new Error(`Failed to update price: ${res.statusText}`);
    }
}