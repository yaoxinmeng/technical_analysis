<script lang="ts">
    import type { PageProps } from "./$types";
    import AddSecurityDialog from "$lib/partials/AddSecurityDialog.svelte";

    let { data }: PageProps = $props();
    console.log("Page data:", data);
    
    let inProgress = $state(false);
    let openDialog = $state(false);

    async function handleAdd(securityId: string) {
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
        <AddSecurityDialog handleSave={handleAdd} isOpen={openDialog} hasFailed={false} inProgress={inProgress}/>
    </div>
</div>