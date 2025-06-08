<script lang="ts">
    import type { PageProps } from "./$types";

    let { data }: PageProps = $props();
    console.log("Page data:", data);
</script>

<div class="h-screen w-full px-16 py-8">
    <div class="flex items-center gap-6">
        <h1 class="text-3xl font-bold">{data.security.symbol}</h1>
        <h1 class="text-3xl font-semibold">{data.security.name}</h1>
    </div>
</div>