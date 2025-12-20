<script lang="ts">
    import type { PageProps } from "./$types";
    import AddSecurityDialog from "$lib/partials/AddSecurityDialog.svelte";
    import SecuritiesTable from "$lib/partials/SecuritiesTable.svelte";
    import LoadingOverlay from "$lib/components/LoadingOverlay.svelte";
    import ExchangeRatesDropdown from "$lib/partials/ExchangeRatesDropdown.svelte";
    import { exportCsv } from "$lib/functions/utils/csvUtils";
    import { saveSecurityOverview, updateSecurity, deleteSecurity, fetchSecurityOverview, fetchSecurityPrice } from "$lib/functions/api";
    import { invalidateAll } from "$app/navigation";
    import type { Security } from "$lib/types/schema";

    let { data }: PageProps = $props();

    let inProgress = $state(false);
    let openDialog = $state(false);
    let hasFailed = $state(false);

    async function handleAdd(securityId: string) {
        if (!securityId) {
            throw new Error("Security ID is required");
        }
        if (data.securities.map((s) => s.symbol).includes(securityId)) {
            throw new Error("Security already exists");
        }
        openDialog = true;
        inProgress = true;
        console.log("Add security:", securityId);
        try {
            // fetch results from the backend API
            let result = await fetchSecurityOverview(securityId);
            console.log(result);
            // save the security to the watchlist
            await saveSecurityOverview(securityId, result.name, result.sector, result.exchange_currency);
            // fetch prices for the new security
            await handleFetchPrice(securityId);
            openDialog = false;
            inProgress = false;
            hasFailed = false;
            // refresh the page to show the new security
            await invalidateAll();
        } catch (err: any) {
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
            await deleteSecurity(securityId);
            // refresh the page to show the updated watchlist
            await invalidateAll();
        } catch (err: any) {
            console.error(err);
        }
    }

    async function fetchAndUpdatePrice(security: Security) {
        // fetch the latest price for the security
        security.price.price = await fetchSecurityPrice(security.symbol);
        security.price.date = new Date().toISOString().split("T")[0]; // format date as YYYY-MM-DD
        // update the security's price in the database
        await updateSecurity(security);
    }

    async function handleFetchPrice(securityId: string) {
        if (!securityId) return;
        console.log("Fetch price for security:", securityId);
        try {
            // get current security
            let security = data.securities.find((s) => s.symbol === securityId);
            if (!security) {
                throw new Error(`Security with ID ${securityId} not found`);
            }
            await fetchAndUpdatePrice(security);
            // refresh the page to show the updated price
            await invalidateAll();
        } catch (err: any) {
            console.error(err);
        }
    }

    async function handleFetchAll() {
        inProgress = true;
        for (const security of data.securities) {
            try {
                await fetchAndUpdatePrice(security);
            } catch (err: any) {
                console.error(err);
            }
        }
        inProgress = false;
        // refresh the page to show the updated price
        await invalidateAll();
    }

    async function handleFetchRates() {
        inProgress = true;
        for (const rate in data.rates) {
            let curr1 = rate.split("-")[0];
            let curr2 = rate.split("-")[1];
            try {
                // fetch exchange rates for the currency pair
                let res = await fetch(`/api/backend/rates?curr1=${curr1}&curr2=${curr2}`);
                if (!res.ok) {
                    throw new Error(`Failed to fetch exchange rates: ${res.statusText}`);
                }
                let rates = await res.json();
                // update the rates in the database
                res = await fetch(`/api/db/rates`, {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        from: curr1,
                        to: curr2,
                        date: new Date().toISOString().split("T")[0], // format date as YYYY-MM-DD
                        rate: rates,
                    }),
                });
            } catch (err: any) {
                console.error(err);
            }
        }
        inProgress = false;
        // refresh the page to show the updated price
        await invalidateAll();
    }
</script>

{#if inProgress}
    <LoadingOverlay />
{/if}
<div class="h-screen w-full px-16 py-8">
    <h1 class="text-3xl font-semibold">Watchlist</h1>
    <ExchangeRatesDropdown rates={data.rates} />
    <div class="flex justify-end gap-4">
        <button
            class="bg-blue-200 rounded-full px-4 py-2 cursor-pointer"
            onclick={handleFetchRates}
        >
            Update Exchange Rates
        </button>
        <button
            class="bg-blue-200 rounded-full px-4 py-2 cursor-pointer"
            onclick={handleFetchAll}
        >
            Fetch All
        </button>
        <AddSecurityDialog
            handleSave={handleAdd}
            {hasFailed}
            {inProgress}
            isOpen={openDialog}
        />
        <button
            class="bg-orange-200 rounded-full px-4 py-2 cursor-pointer"
            onclick={() => (exportCsv(data.securities))}
        >
            Export CSV
        </button>
    </div>
    <SecuritiesTable
        {handleDelete}
        {handleFetchPrice}
        securities={data.securities}
        rates={data.rates}
        {inProgress}
    />
</div>
