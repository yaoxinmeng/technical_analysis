<script lang="ts">
    import Loading from "$lib/components/LoadingIcon.svelte";
    import type { Security } from "$db/schema";

    interface Props {
        handleDelete: (id: string) => Promise<void>;
        handleFetchPrice: (id: string) => Promise<void>;
        securities: Security[];
        inProgress: boolean;
        rates: { [key: string]: number };
    }

    let {
        handleDelete,
        handleFetchPrice,
        securities,
        inProgress,
        rates,
    }: Props = $props();
    let fetchProgress = $state(securities.map((s) => false));

    async function handleFetch(symbol: string, idx: number) {
        fetchProgress[idx] = true;
        await handleFetchPrice(symbol);
        fetchProgress[idx] = false;
    }

    $effect(() => {
        fetchProgress = securities.map((s) => inProgress);
    });
</script>

<div class="relative flex rounded-xl bg-clip-border py-8">
    <table class="w-full text-left table-auto">
        <thead>
            <tr>
                <th class="p-4 border-b border-gray-300 bg-gray-200">Symbol</th>
                <th class="p-4 border-b border-gray-300 bg-gray-200">Name</th>
                <th class="p-4 border-b border-gray-300 bg-gray-200">Sector</th>
                <th class="p-4 border-b border-gray-300 bg-gray-200">Price</th>
                <th class="p-4 border-b border-gray-300 bg-gray-200"
                    >Estimated Lower Bound</th
                >
                <th class="p-4 border-b border-gray-300 bg-gray-200"
                    >Estimated Upper Bound</th
                >
                <th class="p-4 border-b border-gray-300 bg-gray-200">Actions</th
                >
            </tr>
        </thead>
        <tbody>
            {#if securities.length === 0}
                <tr>
                    <td colspan="7" class="text-center p-8 bg-gray-50"
                        >No securities found.</td
                    >
                </tr>
            {:else}
                {#each securities as security, idx}
                    <tr>
                        <td class="p-4 border-b border-gray-300 bg-gray-50"
                            >{security.symbol}</td
                        >
                        <td class="p-4 border-b border-gray-300 bg-gray-50"
                            >{security.name}</td
                        >
                        <td class="p-4 border-b border-gray-300 bg-gray-50"
                            >{security.sector}</td
                        >
                        <td class="p-4 border-b border-gray-300 bg-gray-50">
                            <div class="flex flex-row">
                                <div class="row-span-2 gap-2 min-w-40">
                                    <p>
                                        {security.price.date.length === 0
                                            ? "NA"
                                            : `${security.price.price} ${security.exchange_currency}`}
                                    </p>
                                    <p class="text-xs text-gray-500">
                                        Last Fetched: {security.price.date
                                            .length == 0
                                            ? "NA"
                                            : security.price.date}
                                    </p>
                                </div>
                                <button
                                    class="flex bg-blue-200 px-4 py-2 rounded-full cursor-pointer disabled:bg-gray-300 disabled:cursor-not-allowed"
                                    disabled={fetchProgress[idx]}
                                    onclick={() =>
                                        handleFetch(security.symbol, idx)}
                                >
                                    <p>Fetch</p>
                                    {#if fetchProgress[idx]}
                                        <Loading />
                                    {/if}
                                </button>
                            </div>
                        </td>
                        <td class="p-4 border-b border-gray-300 bg-gray-50">
                            <p>
                                {#if security.financials.date.length === 0}
                                    NA
                                {:else}
                                    {#if security.analysis.lower === null}
                                        NULL
                                    {:else}
                                        {`${security.analysis.lower.toFixed(2)} ${security.financials.currency}`}
                                        {#if security.financials.currency !== security.exchange_currency}
                                            <span class="mx-1">
                                                ({(
                                                    security.analysis.lower *
                                                    rates[
                                                        `${security.financials.currency}-${security.exchange_currency}`
                                                    ]
                                                ).toFixed(2)}
                                                {security.exchange_currency})
                                            </span>
                                        {/if}
                                    {/if}
                                {/if}
                            </p>
                            <p class="text-xs text-gray-500">
                                Last Updated: {security.financials.date
                                    .length == 0
                                    ? "NA"
                                    : security.financials.date}
                            </p>
                        </td>
                        <td class="p-4 border-b border-gray-300 bg-gray-50">
                            <p>
                                {#if security.financials.date.length === 0}
                                    NA
                                {:else}
                                    {#if security.analysis.upper === null}
                                        NULL
                                    {:else}
                                        {`${security.analysis.upper.toFixed(2)} ${security.financials.currency}`}
                                        {#if security.financials.currency !== security.exchange_currency}
                                            <span class="mx-1">
                                                ({(
                                                    security.analysis.upper *
                                                    rates[
                                                        `${security.financials.currency}-${security.exchange_currency}`
                                                    ]
                                                ).toFixed(2)}
                                                {security.exchange_currency})
                                            </span>
                                        {/if}
                                    {/if}
                                {/if}
                            </p>
                            <p class="text-xs text-gray-500">
                                Last Updated: {security.financials.date
                                    .length == 0
                                    ? "NA"
                                    : security.financials.date}
                            </p>
                        </td>
                        <td class="p-4 border-b border-gray-300 bg-gray-50">
                            <div class="flex items-center gap-2">
                                <a
                                    class="bg-blue-200 px-4 py-2 rounded-full cursor-pointer"
                                    href={`/${security.symbol}`}>View/Update</a
                                >
                                <button
                                    class="bg-red-400 px-4 py-2 rounded-full cursor-pointer"
                                    onclick={() =>
                                        handleDelete(security.symbol)}
                                    >Delete</button
                                >
                            </div>
                        </td>
                    </tr>
                {/each}
            {/if}
        </tbody>
    </table>
</div>
