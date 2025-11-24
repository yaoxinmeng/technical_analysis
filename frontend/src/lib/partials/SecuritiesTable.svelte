<script lang="ts">
    import Loading from "$lib/components/LoadingIcon.svelte";
    import type { Security } from "$db/schema";
    import { convertPrice } from "$lib/utils/calculations";

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

    let sortBy = $state({col: "id", ascending: true});
    let fetchProgresses = $state(securities.map(() => inProgress));

    function mapSecurities(securities: Security[]) {
        return securities.map((s, idx) => {
            let convertedUpper = convertPrice(s.analysis.upper, rates, s.financials.currency, s.exchange_currency);
            let convertedLower = convertPrice(s.analysis.lower, rates, s.financials.currency, s.exchange_currency);
            let score = null;
            if (s.analysis.upper > 0 && s.analysis.lower > 0 && s.price.price > 0) {
                score = 1 - (s.price.price - convertedLower) / (convertedUpper - convertedLower);
            }
            return {
                idx: idx,
                symbol: s.symbol,
                name: s.name,
                sector: s.sector,
                price: s.price.date.length === 0 ? null : s.price.price,
                priceDate: s.price.date.length === 0 ? null : s.price.date,
                exchangeCurrency: s.exchange_currency,
                financialsCurrency: s.financials.currency,
                financialsDate: s.financials.date.length === 0 ? null : s.financials.date,
                lower: s.analysis.lower,
                convertedLower: s.financials.currency !== s.exchange_currency ? convertedLower : null,
                upper: s.analysis.upper,
                convertedUpper: s.financials.currency !== s.exchange_currency ? convertedUpper : null,
                score: score
        }});
    }

    // create array to store table data
    let tableData = $derived(mapSecurities(securities));

    async function onFetch(symbol: string) {
        let idx = tableData.filter((s) => s.symbol === symbol)[0].idx;
        fetchProgresses[idx] = true;
        await handleFetchPrice(symbol);
        fetchProgresses[idx] = false;
    }

    function sort(col: string, ascending: boolean) {
        // Modifier to sorting function for ascending or descending
		let sortModifier = (ascending) ? 1 : -1;
		
		let sort = (a: any, b: any) => 
			(a[col] < b[col]) 
			? -1 * sortModifier 
			: (a[col] > b[col]) 
			? 1 * sortModifier 
			: 0;
		
		return tableData.toSorted(sort);
    }

    function updateSortBy(col: string) {
        if (sortBy.col == col) {
			sortBy.ascending = !sortBy.ascending
		} else {
			sortBy.col = col
			sortBy.ascending = true
		}
    }

    let sortedTableDate = $derived(sort(sortBy.col, sortBy.ascending));
    $inspect(tableData);
    $inspect(sortedTableDate);
</script>

<div class="my-8 h-[calc(100%-200px)] overflow-y-auto">
    <table class="w-full text-left table-auto">
        <thead class="sticky top-0 z-10">
            <tr>
                <th class="p-4 border-b border-gray-300 bg-gray-200 hover:bg-gray-300 cursor-pointer" onclick={() => updateSortBy("symbol")}>Symbol</th>
                <th class="p-4 border-b border-gray-300 bg-gray-200 hover:bg-gray-300 cursor-pointer" onclick={() => updateSortBy("name")}>Name</th>
                <th class="p-4 border-b border-gray-300 bg-gray-200 hover:bg-gray-300 cursor-pointer" onclick={() => updateSortBy("sector")}>Sector</th>
                <th class="p-4 border-b border-gray-300 bg-gray-200 hover:bg-gray-300 cursor-pointer" onclick={() => updateSortBy("price")}>Price</th>
                <th class="p-4 border-b border-gray-300 bg-gray-200 hover:bg-gray-300 cursor-pointer" onclick={() => updateSortBy("lower")}
                    >Estimated Lower Bound</th
                >
                <th class="p-4 border-b border-gray-300 bg-gray-200 hover:bg-gray-300 cursor-pointer" onclick={() => updateSortBy("upper")}
                    >Estimated Upper Bound</th
                >
                <th class="p-4 border-b border-gray-300 bg-gray-200 hover:bg-gray-300 cursor-pointer" onclick={() => updateSortBy("score")}>Score</th>
                <th class="p-4 border-b border-gray-300 bg-gray-200">Actions</th
                >
            </tr>
        </thead>
        <tbody class="overflow-y-auto">
            {#if sortedTableDate.length === 0}
                <tr>
                    <td colspan="7" class="text-center p-8 bg-gray-50"
                        >No securities found.</td
                    >
                </tr>
            {:else}
                {#each sortedTableDate as row}
                    <tr>
                        <td class="p-4 border-b border-gray-300 bg-gray-50"
                            >{row.symbol}</td
                        >
                        <td class="p-4 border-b border-gray-300 bg-gray-50"
                            >{row.name}</td
                        >
                        <td class="p-4 border-b border-gray-300 bg-gray-50"
                            >{row.sector}</td
                        >
                        <td class="p-4 border-b border-gray-300 bg-gray-50">
                            <div class="flex flex-row">
                                <div class="row-span-2 gap-2 min-w-40">
                                    <p>
                                        {row.price === null ? "NA" : `${row.price.toFixed(2)} ${row.exchangeCurrency}`}
                                    </p>
                                    <p class="text-xs text-gray-500">
                                        Last Fetched: {row.priceDate === null
                                            ? "NA"
                                            : row.priceDate
                                        }
                                    </p>
                                </div>
                                <button
                                    class="flex bg-blue-200 px-4 py-2 rounded-full cursor-pointer disabled:bg-gray-300 disabled:cursor-not-allowed"
                                    disabled={fetchProgresses[row.idx]}
                                    onclick={() =>
                                        onFetch(row.symbol)}
                                >
                                    <p>Fetch</p>
                                    {#if fetchProgresses[row.idx]}
                                        <Loading />
                                    {/if}
                                </button>
                            </div>
                        </td>
                        <td class="p-4 border-b border-gray-300 bg-gray-50">
                            <p>
                                {#if row.financialsDate === null}
                                    NA
                                {:else}
                                    {#if row.lower === null}
                                        NULL
                                    {:else}
                                        {`${row.lower.toFixed(2)} ${row.financialsCurrency}`}
                                        {#if row.convertedLower !== null}
                                            <span class="mx-1">
                                                ({row.convertedLower.toFixed(2)}
                                                {row.exchangeCurrency})
                                            </span>
                                        {/if}
                                    {/if}
                                {/if}
                            </p>
                            <p class="text-xs text-gray-500">
                                Last Updated: {row.financialsDate === null
                                    ? "NA"
                                    : row.financialsDate}
                            </p>
                        </td>
                        <td class="p-4 border-b border-gray-300 bg-gray-50">
                            <p>
                                {#if row.financialsDate === null}
                                    NA
                                {:else}
                                    {#if row.upper === null}
                                        NULL
                                    {:else}
                                        {`${row.upper.toFixed(2)} ${row.financialsCurrency}`}
                                        {#if row.convertedUpper !== null}
                                            <span class="mx-1">
                                                ({row.convertedUpper.toFixed(2)}
                                                {row.exchangeCurrency})
                                            </span>
                                        {/if}
                                    {/if}
                                {/if}
                            </p>
                            <p class="text-xs text-gray-500">
                                Last Updated: {row.financialsDate === null
                                    ? "NA"
                                    : row.financialsDate}
                            </p>
                        </td>
                        <td class="p-4 border-b border-gray-300 bg-gray-50">
                            <p>
                                {#if row.score === null}
                                        NULL
                                {:else}
                                    {row.score.toFixed(2)}
                                {/if}
                            </p>
                        </td>
                        <td class="p-4 border-b border-gray-300 bg-gray-50">
                            <div class="flex items-center gap-2">
                                <a
                                    class="bg-blue-200 px-4 py-2 rounded-full cursor-pointer"
                                    href={`/${row.symbol}`}>View/Update</a
                                >
                                <button
                                    class="bg-red-400 px-4 py-2 rounded-full cursor-pointer"
                                    onclick={() =>
                                        handleDelete(row.symbol)}
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
