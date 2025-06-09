<script lang="ts">
    import type { PageProps } from "./$types";
    import SecurityPage from "$lib/partials/SecurityPage.svelte";

    let { data }: PageProps = $props();
    console.log("Page data:", data);
    let security = $state(data.security);
    let inProgress = $state(false);

    async function fetchFinancials() {
        inProgress = true;
        console.log("Fetch financials for security:", security.symbol);
        let res = await fetch(
            `/api/backend/${security.symbol}?info=financials`,
        );
        if (!res.ok) {
            console.error(`Failed to fetch financials: ${res.statusText}`);
            inProgress = false;
            return;
        }
        const result = await res.json();
        console.log(result);
        inProgress = false;
    }

    async function saveSecurity() {}
</script>

<SecurityPage {security} {fetchFinancials} {saveSecurity} />
