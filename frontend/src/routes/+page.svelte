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
    <h1 class="text-3xl font-semibold">Watchlist</h1>
    <div class="flex justify-end">
        <AddSecurityDialog handleSave={handleAdd} hasFailed={false} inProgress={inProgress} isOpen={openDialog}/>
    </div>
    <div class="relative flex rounded-xl bg-clip-border mt-8">
        <table class="w-full text-left table-auto">
            <thead>
                <tr>
                    <th class="p-4 border-b border-gray-300 bg-gray-200">Symbol</th>
                    <th class="p-4 border-b border-gray-300 bg-gray-200">Name</th>
                    <th class="p-4 border-b border-gray-300 bg-gray-200">Sector</th>
                    <th class="p-4 border-b border-gray-300 bg-gray-200">Price</th>
                    <th class="p-4 border-b border-gray-300 bg-gray-200">Estimated Lower Bound</th>
                    <th class="p-4 border-b border-gray-300 bg-gray-200">Estimated Upper Bound</th>
                </tr>
            </thead>
            <tbody>
                {#if data.securities.length === 0}
                    <tr>
                        <td colspan="6" class="text-center p-8 bg-gray-50">No securities found.</td>
                    </tr>
                {:else}
                    {#each data.securities as security}
                        <tr>
                            <td class="p-4 border-b border-gray-300 bg-gray-50">{security.symbol}</td>
                            <td class="p-4 border-b border-gray-300 bg-gray-50">{security.name}</td>
                            <td class="p-4 border-b border-gray-300 bg-gray-50">{security.sector}</td>
                            <td class="p-4 border-b border-gray-300 bg-gray-50">{security.price.price ?? "NA"}</td>
                            <td class="p-4 border-b border-gray-300 bg-gray-50">{security.analysis?.lower ?? "NA"}</td>
                            <td class="p-4 border-b border-gray-300 bg-gray-50">{security.analysis?.upper ?? "NA"}</td>
                        </tr>
                    {/each}
                {/if}
            </tbody>
        </table>
    </div>
</div>