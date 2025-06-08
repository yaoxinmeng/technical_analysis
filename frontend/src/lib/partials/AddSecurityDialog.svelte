<script lang="ts">
    import { writable } from "svelte/store";
    import { createDialog, melt } from "@melt-ui/svelte";
    import { fade, scale } from 'svelte/transition';

    interface Props {
		handleSave: (id: string) => void;
        isOpen: boolean;
        hasFailed: boolean;
        inProgress: boolean;
	}

    let { handleSave, isOpen, hasFailed, inProgress }: Props = $props();

    const openStore = writable(isOpen);
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
        escapeBehavior: 'ignore',
        open: openStore,
    });

    $effect(() => {
        $openStore = isOpen;
    })
</script>

<button
    class="bg-blue-200 rounded-full px-4 py-2 cursor-pointer"
    use:melt={$trigger}
>
    Add New +
</button>

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
                start: 0.96,
            }}
        >
            <h2 use:melt={$title} class="text-lg font-medium text-black">Add Security</h2>
            <div class="flex flex-row items-center gap-4 mt-4">
                <label class="w-[90px] text-right text-black" for="name">Security ID</label>
                <input
                    class="inline-flex w-full flex-1 items-center justify-center
                                rounded-sm border border-solid px-3 py-2 leading-none text-black"
                    id="name"
                    placeholder="Enter security ID..."
                    bind:value={securityId}
                />
            </div>
            <div class="my-4">
                {#if hasFailed}
                    <p class="text-red-500">Failed to add security.</p>
                {/if}
            </div>
            <div class="mt-6 flex justify-end gap-4">
                <button
                use:melt={$close}
                class="inline-flex items-center justify-center rounded-full
                            bg-zinc-100 px-4 py-2 font-medium cursor-pointer disabled:cursor-not-allowed"
                disabled={inProgress}
                >
                Cancel
                </button>
                <button
                class="inline-flex items-center justify-center rounded-full
                            bg-blue-200 px-4 py-2 font-medium cursor-pointer disabled:cursor-not-allowed disabled:bg-gray-300"
                disabled={inProgress}
                onclick={() => handleSave(securityId)}
                >
                Save
                {#if inProgress}
                <svg class="ml-3 size-5 animate-spin text-white" viewBox="0 0 24 24" fill="none">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                {/if}
                </button>
            </div>
        </div>
    </div>
{/if}
