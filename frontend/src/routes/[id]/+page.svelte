<script lang="ts">
    import type { PageProps } from "./$types";
    import { invalidateAll } from "$app/navigation";
    import SecurityPage from "$lib/partials/SecurityPage.svelte";
    import type { Financial, Security } from "$db/schema";
    import { generateAnalysis } from "$lib/calculations";

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
        for (let key in result.balance_sheet) {
            if (!result.financial_statement.financials.hasOwnProperty(key)) {
                console.error("No financials for date:", key);
                continue;
            }
            let item = {
                date: key,
                balance_sheet: {
                    assets: result.balance_sheet[key].assets,
                    liabilities: result.balance_sheet[key].liabilities,
                    book_value: result.balance_sheet[key].book_value,
                },
                income_statement: {
                    income: result.financial_statement.financials[key].income,
                    shares: result.financial_statement.financials[key].shares,
                },
            };
            console.debug(item);
            newFinancials.push(item);
        }
        for (let financial of security.financials.financials) {
            if (!newFinancials.map((f) => f.date).includes(financial.date)) {
                newFinancials.push(financial);
            }
        }
        // sort financials by date
        newFinancials.sort((a, b) => {
            return (
                new Date(b.date).getSeconds() - new Date(a.date).getSeconds()
            );
        });

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
