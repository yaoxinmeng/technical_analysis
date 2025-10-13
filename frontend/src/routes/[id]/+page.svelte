<script lang="ts">
    import type { PageProps } from "./$types";
    import { invalidateAll } from "$app/navigation";
    import SecurityPage from "$lib/partials/SecurityPage.svelte";
    import type { Financial, Security } from "$db/schema";
    import { generateAnalysis, updateExistingFinancials } from "$lib/utils/calculations";

    let { data }: PageProps = $props();
    let security = $state(data.security);
    let inProgress = $state(false);

    async function fetchFinancials() {
        inProgress = true;
        console.log("Fetch financials for security:", security.symbol);
        // fetch the latest financials for the security
        let res = await fetch(
            `/api/backend/${security.symbol}?info=financials`,
        );
        if (!res.ok) {
            console.error(`Failed to fetch financials: ${res.statusText}`);
            throw new Error(
                `Failed to fetch financials: ${res.statusText}`,
            );
        }
        const result = await res.json();
        console.debug(result);
        if (result.balance_sheet === undefined || result.financial_statement === undefined) {
            console.error(`Failed to fetch financials`);
            throw new Error(
                `Failed to fetch financials due to missing data`,
            );
        }
        // parse updated financials
        let newFinancials: Financial[] = [];
        for (let key in result.financial_statement.financials) {
            let balance_sheet = result.balance_sheet[key] ? result.balance_sheet[key] : {
                assets: -1,
                liabilities: -1,
                book_value: -1,
            };
            let item = {
                date: key,
                balance_sheet: balance_sheet,
                income_statement: {
                    income: result.financial_statement.financials[key].income,
                    shares: result.financial_statement.financials[key].shares,
                },
            };
            console.debug(item);
            newFinancials.push(item);
        }
        newFinancials = updateExistingFinancials(
            security.financials.financials,
            newFinancials,
        );

        // return updated security
        return {
            ...security,
            financials: {
                date: new Date().toISOString().split("T")[0], // format date as YYYY-MM-DD
                currency: result.financial_statement.financials_currency,
                financials: newFinancials,
            },
            analysis: generateAnalysis(newFinancials, security.assumptions),
        };
    }

    async function saveSecurity(security: Security) {
        // update the security's price in the database
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
        // refresh the page to show the updated price
        await invalidateAll();
    }
</script>

<SecurityPage
    initialSecurity={data.security}
    {fetchFinancials}
    {saveSecurity}
    {generateAnalysis}
/>
