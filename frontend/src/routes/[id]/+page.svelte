<script lang="ts">
    import type { PageProps } from "./$types";
    import { invalidateAll } from "$app/navigation";
    import SecurityPage from "$lib/partials/SecurityPage.svelte";
    import type { Financial, Security } from "$db/schema";
    import { generateAnalysis, updateExistingFinancials } from "$lib/utils/calculations";
    import { updateSecurity } from "$lib/api";

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
            date: new Date().toISOString().split("T")[0], // format date as YYYY-MM-DD
            currency: result.financial_statement.financials_currency,
            financials: newFinancials,
        };
    }

    async function saveSecurity(security: Security) {
        // update the security in the database
        await updateSecurity(security);
        // refresh the page to show the updated price
        await invalidateAll();
    }
</script>

<SecurityPage
    security={data.security}
    rates={data.rates}
    {fetchFinancials}
    {saveSecurity}
    {generateAnalysis}
/>
