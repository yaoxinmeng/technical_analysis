<script lang="ts">
    import type {Security} from "$db/schema";

    interface Props {
		handleDelete: (id: string) => void;
        handleFetchPrice: (id: string) => void;
        securities: Security[];
	}

    let { handleDelete, handleFetchPrice, securities }: Props = $props();
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
                {#each securities as security}
                    <tr>
                        <td class="p-4 border-b border-gray-300 bg-gray-50">{security.symbol}</td>
                        <td class="p-4 border-b border-gray-300 bg-gray-50">{security.name}</td>
                        <td class="p-4 border-b border-gray-300 bg-gray-50">{security.sector}</td>
                        <td class="p-4 border-b border-gray-300 bg-gray-50">
                            <div class="flex justify-between items-center">
                                <div class="flex flex-col gap-2">
                                    <p>{security.price.date.length == 0 ? "NA" : `${security.price.price} ${security.exchange_currency}`}</p>
                                    <p class="text-xs text-gray-500">Last Fetched: {security.price.date.length == 0 ? "NA" : security.price.date}</p>
                                </div>
                                <button class="bg-blue-200 px-4 py-2 rounded-full cursor-pointer" onclick={() => handleFetchPrice(security.symbol)}>Refresh</button>
                            </div>
                        </td>
                        <td class="p-4 border-b border-gray-300 bg-gray-50">{security.analysis?.lower ?? "NA"}</td>
                        <td class="p-4 border-b border-gray-300 bg-gray-50">{security.analysis?.upper ?? "NA"}</td>
                        <td class="p-4 border-b border-gray-300 bg-gray-50">
                            <div class="flex items-center gap-2">
                                <a class="bg-blue-200 px-4 py-2 rounded-full cursor-pointer" href={`/${security.symbol}`}>View</a>
                                <button class="bg-red-400 px-4 py-2 rounded-full cursor-pointer" onclick={() => handleDelete(security.symbol)}>Delete</button>
                            </div>
                        </td>
                    </tr>
                {/each}
            {/if}
        </tbody>
    </table>
</div>