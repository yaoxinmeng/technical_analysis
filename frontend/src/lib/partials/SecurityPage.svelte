<script lang="ts">
    import Loading from "$lib/components/Loading.svelte";
    import type { Security } from "$db/schema";

    interface Props {
        security: Security;
        fetchFinancials: () => Promise<void>;
        saveSecurity: () => Promise<void>;
    }

    let { security, fetchFinancials, saveSecurity }: Props = $props();
    let inProgress = $state(false);

    async function handleFetch() {
        inProgress = true;
        await fetchFinancials();
        inProgress = false;
    }
</script>

<div class="h-screen w-full mx-8 my-8 md:px-16">
    <div class="flex justify-between">
        <h1 class="text-3xl font-bold">
            {security.symbol}
            <span class="ml-3 font-semibold">{security.name}</span>
        </h1>
        <button
            class="flex bg-blue-200 px-4 py-2 rounded-full cursor-pointer"
            onclick={saveSecurity}
        >
            Save
        </button>
    </div>
    <div class="flex flex-col mt-8 gap-4">
        <div class="flex flex-row gap-4">
            <div class="flex flex-col gap-4 bg-gray-100 rounded-xl p-6">
                <h2 class="text-2xl">Assumptions</h2>
                <div class="flex flex-col gap-1">
                    <label for="growth">Estimated Annual Growth (%)</label>
                    <input
                        id="growth"
                        type="number"
                        class="bg-white py-2 px-4 rounded-full"
                        bind:value={security.analysis.assumptions.growth_rate}
                    />
                </div>
                <div class="flex flex-col gap-1">
                    <label for="horizon">Estimated Horizon (years)</label>
                    <input
                        id="horizon"
                        type="number"
                        class="bg-white py-2 px-4 rounded-full"
                        bind:value={security.analysis.assumptions.years}
                    />
                </div>
            </div>
            <div class="flex-1 bg-gray-100 rounded-xl p-6">
                <h2 class="text-2xl">Analysis</h2>
                <div class="flex flex-col gap-4 mt-4">
                    <h3 class="font-semibold">Technical Analysis</h3>
                    <div class="grid grid-cols-2 gap-4 md:grid-cols-5">
                        <div class="flex flex-col gap-1 min-w-20">
                            <p class="text-sm text-nowrap">
                                Average Income{security.financials.currency
                                    ? ` (${security.financials.currency})`
                                    : ""}
                            </p>
                            <p
                                class="bg-green-200 py-2 px-4 rounded-full text-base"
                            >
                                {security.analysis.average_income}
                            </p>
                        </div>
                        <div class="flex flex-col gap-1 min-w-20">
                            <p class="text-sm">P/E Ratio</p>
                            <p
                                class="bg-green-200 py-2 px-4 rounded-full text-base"
                            >
                                {security.analysis.pe_ratio * 100} %
                            </p>
                        </div>
                        <div class="flex flex-col gap-1 min-w-20">
                            <p class="text-sm">D/E Ratio</p>
                            <p
                                class="bg-green-200 py-2 px-4 rounded-full text-base"
                            >
                                {security.analysis.de_ratio * 100} %
                            </p>
                        </div>
                        <div class="flex flex-col gap-1 min-w-20">
                            <p class="text-sm">BVPS</p>
                            <p
                                class="bg-green-200 py-2 px-4 rounded-full text-base"
                            >
                                {security.analysis.bvps}
                            </p>
                        </div>
                        <div class="flex flex-col gap-1 min-w-20">
                            <p class="text-sm">CAGR</p>
                            <p
                                class="bg-green-200 py-2 px-4 rounded-full text-base"
                            >
                                {security.analysis.cagr * 100} %
                            </p>
                        </div>
                    </div>
                    <h3 class="font-semibold">Estimated Bounds</h3>
                    <div class="grid grid-cols-2 gap-4 md:grid-cols-5">
                        <div class="flex flex-col gap-1 min-w-20">
                            <p class="text-sm">Lower Bound</p>
                            <p
                                class="bg-green-200 py-2 px-4 rounded-full text-base"
                            >
                                {security.analysis.lower}
                            </p>
                        </div>
                        <div class="flex flex-col gap-1 min-w-20">
                            <p class="text-sm">Target</p>
                            <p
                                class="bg-green-200 py-2 px-4 rounded-full text-base"
                            >
                                {security.analysis.target}
                            </p>
                        </div>
                        <div class="flex flex-col gap-1 min-w-20">
                            <p class="text-sm">Upper Bound</p>
                            <p
                                class="bg-green-200 py-2 px-4 rounded-full text-base"
                            >
                                {security.analysis.upper}
                            </p>
                        </div>
                    </div>
                    <h3 class="font-semibold">Nominal Bounds</h3>
                    <div class="grid grid-cols-2 gap-4 md:grid-cols-5">
                        <div class="flex flex-col gap-1 min-w-20">
                            <p class="text-sm">Lower Bound</p>
                            <p
                                class="bg-green-200 py-2 px-4 rounded-full text-base"
                            >
                                {security.analysis.nominal_lower}
                            </p>
                        </div>
                        <div class="flex flex-col gap-1 min-w-20">
                            <p class="text-sm">Target</p>
                            <p
                                class="bg-green-200 py-2 px-4 rounded-full text-base"
                            >
                                {security.analysis.nominal_target}
                            </p>
                        </div>
                        <div class="flex flex-col gap-1 min-w-20">
                            <p class="text-sm">Upper Bound</p>
                            <p
                                class="bg-green-200 py-2 px-4 rounded-full text-base"
                            >
                                {security.analysis.nominal_upper}
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="flex flex-col bg-gray-100 rounded-xl p-6 w-full gap-6">
            <div class="flex flex-row justify-between">
                <h2 class="text-2xl">Financials</h2>
                <button
                    class="flex bg-blue-200 px-4 py-2 rounded-full cursor-pointer disabled:bg-gray-300 disabled:cursor-not-allowed"
                    disabled={inProgress}
                    onclick={handleFetch}
                >
                    <p>Fetch</p>
                    {#if inProgress}
                        <Loading />
                    {/if}
                </button>
            </div>
            <table class="w-full text-left table-auto">
                <thead>
                    <tr>
                        <th
                            rowspan="2"
                            class="p-4 border-b border-r border-gray-300 bg-gray-200"
                            >Date</th
                        >
                        <th
                            colspan="2"
                            class="p-4 border-b border-r text-center border-gray-300 bg-gray-200"
                            >Income Statement</th
                        >
                        <th
                            colspan="3"
                            class="p-4 border-b text-center border-gray-300 bg-gray-200"
                            >Balance Sheet</th
                        >
                    </tr>
                    <tr>
                        <th class="p-4 border-b border-gray-300 bg-gray-200"
                            >Income</th
                        >
                        <th
                            class="p-4 border-b border-r border-gray-300 bg-gray-200"
                            >Common Shares</th
                        >
                        <th class="p-4 border-b border-gray-300 bg-gray-200"
                            >Assets</th
                        >
                        <th class="p-4 border-b border-gray-300 bg-gray-200"
                            >Liabilities</th
                        >
                        <th class="p-4 border-b border-gray-300 bg-gray-200"
                            >Book Value</th
                        >
                    </tr>
                </thead>
                <tbody>
                    {#if security.financials.financials.length === 0}
                        <tr>
                            <td colspan="6" class="text-center p-8 bg-gray-50"
                                >No financial record found.</td
                            >
                        </tr>
                    {:else}
                        {#each security.financials.financials as financial, idx}
                            <tr></tr>
                        {/each}
                    {/if}
                </tbody>
            </table>
        </div>
    </div>
</div>
