<script lang="ts">
    import type { PageProps } from "./$types";
    import AddSecurityDialog from "$lib/partials/AddSecurityDialog.svelte";

    let { data }: PageProps = $props();
    console.log("Page data:", data);
    
    let inProgress = $state(false);
    let openDialog = $state(false);

    async function handleAdd(securityId: string) {
        openDialog = true;
        if (!securityId) return;
        inProgress = true;
        console.log("Add security:", securityId);
        try {
            let result = await fetch(`/api/backend/${securityId}?info=overview`).then(res => res.json());
            console.log(result);

        } catch(err: any) {
            console.error(err);
        }
        openDialog = false;
        inProgress = false;
    }
</script>

<div class="h-screen w-full px-16 py-8">
    <h1 class="text-lg font-semibold">Watchlist</h1>
    <div class="flex justify-end">
        <AddSecurityDialog handleSave={handleAdd} hasFailed={false} inProgress={inProgress} isOpen={openDialog}/>
    </div>
    <table>
        <thead>
            <tr>
                <th class="text-left">Symbol</th>
                <th class="text-left">Name</th>
                <th class="text-left">Sector</th>
                <th class="text-left">Price</th>
                <th class="text-left">Estimated Lower Bound</th>
                <th class="text-left">Estimated Upper Bound</th>
            </tr>
        </thead>
        <tbody>
            {#each data.securities as security}
                <tr>
                    <td>{security.symbol}</td>
                    <td>{security.name}</td>
                    <td>{security.sector}</td>
                    <td>{security.price ?? "NA"}</td>
                    <td>{security.analysis?.lower ?? "NA"}</td>
                    <td>{security.analysis?.upper ?? "NA"}</td>
                </tr>
            {/each}
        </tbody>
    </table>
</div>