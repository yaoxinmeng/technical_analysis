<script lang="ts">
    import type { PageProps } from "./$types";
    import AddSecurityDialog from "$lib/partials/AddSecurityDialog.svelte";
    import SecuritiesTable from "$lib/partials/SecuritiesTable.svelte";
    import { invalidateAll } from "$app/navigation";
    import type { Security } from "$db/schema";

    let { data }: PageProps = $props();
    console.log("Page data:", data);
    
    let inProgress = $state(false);
    let openDialog = $state(false);
    let hasFailed = $state(false);

    async function handleAdd(securityId: string) {
        if (!securityId) return;
        openDialog = true;
        inProgress = true;
        console.log("Add security:", securityId);
        try {
            // fetch results from the backend API
            let res = await fetch(`/api/backend/${securityId}?info=overview`);
            if (!res.ok) {
                throw new Error(`Failed to fetch security data: ${res.statusText}`);
            }
            let result = await res.json();
            console.log(result);
            // save the security to the watchlist
            res = await fetch(`/api/db`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ 
                    id: securityId,
                    name: result.name,
                    sector: result.sector,
                    exchange_currency: result.currency
                 })
            });
            if (!res.ok) {
                throw new Error(`Failed to save security: ${res.statusText}`);
            }
            openDialog = false;
            inProgress = false;
            // refresh the page to show the new security
            await invalidateAll();
        } catch(err: any) {
            console.error(err);
            hasFailed = true;
            inProgress = false;
        }
    }

    async function handleDelete(securityId: string) {
        if (!securityId) return;
        console.log("Delete security:", securityId);
        try {
            // delete the security from the watchlist
            let res = await fetch(`/api/db/${securityId}`, {
                method: "DELETE"
            });
            if (!res.ok) {
                throw new Error(`Failed to delete security: ${res.statusText}`);
            }
            // refresh the page to show the updated watchlist
            await invalidateAll();
        } catch(err: any) {
            console.error(err);
        }
    }

    async function handleFetchPrice(securityId: string) {
        if (!securityId) return;
        console.log("Fetch price for security:", securityId);
        try {
            // fetch the latest price for the security
            let res = await fetch(`/api/backend/${securityId}?info=price`);
            if (!res.ok) {
                throw new Error(`Failed to fetch price data: ${res.statusText}`);
            }
            let result = await res.json();
            console.log(result);
            // get current security
            let security = data.securities.find((s: Security) => s.symbol === securityId);
            if (!security) {
                throw new Error(`Security with ID ${securityId} not found`);
            }
            security.price.price = result;
            security.price.date = new Date().toISOString().split('T')[0]; // format date as YYYY-MM-DD
            // update the security's price in the database
            res = await fetch(`/api/db/${securityId}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(security)
            });
            if (!res.ok) {
                throw new Error(`Failed to update price: ${res.statusText}`);
            }
            // refresh the page to show the updated price
            await invalidateAll();
        } catch(err: any) {
            console.error(err);
        }
    }
</script>

<div class="h-screen w-full px-16 py-8">
    <h1 class="text-3xl font-semibold">Watchlist</h1>
    <div class="flex justify-end">
        <AddSecurityDialog handleSave={handleAdd} {hasFailed} {inProgress} isOpen={openDialog}/>
    </div>
    <SecuritiesTable handleDelete={handleDelete} handleFetchPrice={handleFetchPrice} securities={data.securities}/>
</div>