<script lang="ts">
    import type { PageProps } from "./$types";
    import { createDialog, melt } from "@melt-ui/svelte";
    import { fade, scale } from 'svelte/transition';

    let { data }: PageProps = $props();
    console.log("Page data:", data);
    
    let securityId = $state("");

    const {
        elements: {
            trigger,
            portalled,
            overlay,
            content,
            title,
            description,
            close,
        },
        states: { open },
    } = createDialog({
        forceVisible: true,
        closeOnOutsideClick: false,
        escapeBehavior: 'ignore'
    });

    async function handleAdd() {
        if (!securityId) return;
        console.log("Add security:", securityId);
        let result = await fetch(`/api/backend/${securityId}?info=overview`).then(res => res.json());
        console.log(result);
        $open = false;
    }
</script>

<div class="h-screen w-full px-16 py-8">
    <h1 class="text-lg font-semibold">Watchlist</h1>
    <div class="flex justify-end">
        <button
            class="bg-blue-300 rounded-full p-4 cursor-pointer"
            use:melt={$trigger}
        >
            Add New +
        </button>
    </div>
</div>

{#if $open}
    <div use:melt={$portalled}>
        <div 
            use:melt={$overlay}
            class="fixed inset-0 z-50 bg-black/50"
            transition:fade={{ duration: 150 }}
        ></div>
        <div 
            use:melt={$content}
            class="fixed left-1/2 top-1/2 z-50 max-h-[85vh] w-[90vw]
                max-w-[450px] -translate-x-1/2 -translate-y-1/2 rounded-xl bg-white
                p-6 shadow-lg"
            transition:scale={{
                duration: 150,
                y: 8,
                start: 0.96,
            }}
        >
            <h2 use:melt={$title} class="m-0 text-lg font-medium text-black">Add Security</h2>
            <label class="w-[90px] text-right text-black" for="name">Security ID</label>
            <input
                class="inline-flex h-8 w-full flex-1 items-center justify-center
                            rounded-sm border border-solid px-3 leading-none text-black"
                id="name"
                placeholder="Enter security ID..."
                bind:value={securityId}
            />
            <div class="mt-6 flex justify-end gap-4">
                <button
                use:melt={$close}
                class="inline-flex h-8 items-center justify-center rounded-sm
                            bg-zinc-100 px-4 font-medium leading-none text-zinc-600 cursor-pointer"
                >
                Cancel
                </button>
                <button
                class="inline-flex h-8 items-center justify-center rounded-sm
                            bg-magnum-100 px-4 font-medium leading-none text-magnum-900 cursor-pointer"
                onclick={handleAdd}
                >
                Save
                </button>
            </div>
        </div>
    </div>
{/if}
