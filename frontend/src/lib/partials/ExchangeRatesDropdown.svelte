<script lang="ts">
    import { writable } from "svelte/store";
    import { createCollapsible, melt } from "@melt-ui/svelte";
    import { slide } from "svelte/transition";
    import ChevronDown from "$lib/icons/ChevronDown.svelte";
    import Close from "$lib/icons/Close.svelte";

    interface Props {
        rates: { [key: string]: number };
    }

    let { rates }: Props = $props();

    const openStore = writable(false);

    const {
        elements: { root, content, trigger },
        states: { open },
    } = createCollapsible({
        forceVisible: true,
    });

    $effect(() => {
        $openStore = false;
    });
</script>

<div
  use:melt={$root}
  class="relative my-6 w-[18rem] sm:w-[25rem]"
>
  <div class="flex items-center justify-between">
    <span class="text-sm font-semibold text-magnum-900">
      View Exchange Rates
    </span>
    <button
      use:melt={$trigger}
      class="relative h-6 w-6 place-items-center rounded-md bg-white text-sm hover:opacity-50 cursor-pointer"
      aria-label="Toggle"
    >
      <div class="abs-center">
        {#if $open}
          <Close />
        {:else}
          <ChevronDown />
        {/if}
      </div>
    </button>
  </div>

  <div
  >
    {#if $open}
      <div use:melt={$content} transition:slide>
        <div class="flex flex-col gap-1 mt-2">
            {#each Object.keys(rates) as rate}
                <div class="rounded-lg bg-gray-100 p-3">
                    <span class="text-base text-black">{rate}: {rates[rate]}</span>
                </div>
            {/each}
        </div>
      </div>
    {/if}
  </div>
</div>