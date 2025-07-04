<script lang="ts">
    import { writable } from "svelte/store";
    import { createDialog, melt } from "@melt-ui/svelte";
    import { fade, scale } from "svelte/transition";
    import Loading from "$lib/components/Loading.svelte";

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
        escapeBehavior: "ignore",
        open: openStore,
    });

    $effect(() => {
        $openStore = isOpen;
    });
</script>

<button
    class="inline-flex items-center bg-blue-200 rounded-full px-4 py-2 cursor-pointer disabled:cursor-not-allowed disabled:bg-gray-300"
    disabled={inProgress}
    use:melt={$trigger}
>
    Add New +
    {#if inProgress}
        <Loading />
    {/if}
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
            <h2 use:melt={$title} class="text-lg font-medium text-black">
                Add Security
            </h2>
            <div class="flex flex-row items-center gap-4 mt-4">
                <label class="w-[90px] text-right text-black" for="name"
                    >Security ID</label
                >
                <input
                    class="inline-flex w-full flex-1 items-center justify-center
                                rounded-sm border border-solid px-3 py-2 leading-none text-black"
                    id="name"
                    placeholder="Enter security ID..."
                    bind:value={securityId}
                    onkeydown={(e) =>
                        e.key === "Enter" && handleSave(securityId)}
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
                        <Loading />
                    {/if}
                </button>
            </div>
        </div>
    </div>
{/if}
