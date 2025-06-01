<script lang="ts">
    import type { PageProps } from './$types';

	let { data }: PageProps = $props();
    console.log('Page data:', data);
</script>

<div class="h-screen w-full px-16 py-8">
    <h1 class="text-lg font-semibold">Watchlist</h1>
    <div class="flex justify-end">
        <button class="bg-blue-300 rounded-full p-4 cursor-pointer" on:click>Add New +</button>
    </div>
</div>