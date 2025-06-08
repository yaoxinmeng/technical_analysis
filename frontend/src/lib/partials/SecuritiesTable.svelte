<script lang="ts">
    import type {Security} from "$db/schema";

    interface Props {
		handleDelete: (id: string) => Promise<void>;
        handleFetchPrice: (id: string) => Promise<void>;
        securities: Security[];
	}

    let { handleDelete, handleFetchPrice, securities }: Props = $props();
    let fetchProgress = $state(securities.map(s => false))

    async function handleFetch(symbol: string, idx: number) {
        fetchProgress[idx] = true;
        await handleFetchPrice(symbol);
        fetchProgress[idx] = false;
    }
</script>

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
                <th class="p-4 border-b border-gray-300 bg-gray-200">Actions</th>
            </tr>
        </thead>
        <tbody>
            {#if securities.length === 0}
                <tr>
                    <td colspan="7" class="text-center p-8 bg-gray-50">No securities found.</td>
                </tr>
            {:else}
                {#each securities as security, idx}
                    <tr>
                        <td class="p-4 border-b border-gray-300 bg-gray-50">{security.symbol}</td>
                        <td class="p-4 border-b border-gray-300 bg-gray-50">{security.name}</td>
                        <td class="p-4 border-b border-gray-300 bg-gray-50">{security.sector}</td>
                        <td class="p-4 border-b border-gray-300 bg-gray-50">
                            <div class="grid grid-flow-col grid-cols-2 justify-items-start">
                                <div class="row-span-2 gap-2">
                                    <p>{security.price.date.length === 0 ? "NA" : `${security.price.price} ${security.exchange_currency}`}</p>
                                    <p class="text-xs text-gray-500">Last Fetched: {security.price.date.length == 0 ? "NA" : security.price.date}</p>
                                </div>
                                <button 
                                    class="flex bg-blue-200 px-4 py-2 rounded-full cursor-pointer disabled:bg-gray-300 disabled:cursor-not-allowed"
                                    disabled={fetchProgress[idx]}
                                    onclick={() => handleFetch(security.symbol, idx)}
                                >
                                    <p>Refresh</p>
                                    {#if fetchProgress[idx]}
                                        <svg class="ml-3 size-5 animate-spin text-white" viewBox="0 0 24 24" fill="none">
                                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                        </svg>
                                    {/if}
                                </button>
                            </div>
                        </td>
                        <td class="p-4 border-b border-gray-300 bg-gray-50">
                            <p>{security.financials.date.length === 0 ? "NA": `${security.analysis.lower} ${security.financials.currency}`}</p>
                            <p class="text-xs text-gray-500">Last Updated: {security.financials.date.length == 0 ? "NA" : security.financials.date}</p>
                        </td>
                        <td class="p-4 border-b border-gray-300 bg-gray-50">
                            <p>{security.financials.date.length === 0 ? "NA": `${security.analysis.upper} ${security.financials.currency}`}</p>
                            <p class="text-xs text-gray-500">Last Updated: {security.financials.date.length == 0 ? "NA" : security.financials.date}</p>
                        </td>
                        <td class="p-4 border-b border-gray-300 bg-gray-50">
                            <div class="flex items-center gap-2">
                                <a class="bg-blue-200 px-4 py-2 rounded-full cursor-pointer" href={`/${security.symbol}`}>View/Update</a>
                                <button class="bg-red-400 px-4 py-2 rounded-full cursor-pointer" onclick={() => handleDelete(security.symbol)}>Delete</button>
                            </div>
                        </td>
                    </tr>
                {/each}
            {/if}
        </tbody>
    </table>
</div>