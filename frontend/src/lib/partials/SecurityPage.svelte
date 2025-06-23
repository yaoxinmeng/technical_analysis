<script lang="ts">
    import Loading from "$lib/components/Loading.svelte";
    import type { Security, Financial, Assumptions, Analysis } from "$db/schema";

    interface Props {
        initialSecurity: Security;
        fetchFinancials: () => Promise<Security>;
        saveSecurity: (security: Security) => Promise<void>;
        generateAnalysis: (financials: Financial[], assumptions: Assumptions) => Analysis;
    }

    let {
        initialSecurity,
        fetchFinancials,
        saveSecurity,
        generateAnalysis
    }: Props = $props();
    
    let security = $state(initialSecurity);
    let inProgress = $state(false);
    let growthPercent = $state(security.assumptions.growth_rate * 100);
    let safetyMarginPercent = $state(security.assumptions.safety_margin * 100);

    let canSave = $derived(
        JSON.stringify(security) !== JSON.stringify(initialSecurity),
    );

    async function handleFetch() {
        inProgress = true;
        try {
            security = await fetchFinancials();
        } catch (error) {
            console.error("Error fetching financials:", error);
        }
        inProgress = false;
    }

    function parseNumber(value: string | undefined): number {
        if (value === undefined || value.trim() === "") {
            return 0;
        }
        return Number.parseFloat(value.replace(/,/g, ""));
    }

    $effect(() => {
        security.assumptions.growth_rate = growthPercent / 100;
    });
    
    $effect(() => {
        security.assumptions.safety_margin = safetyMarginPercent / 100;
    });

    $effect(() => {
        security.analysis = generateAnalysis(security.financials.financials, security.assumptions);
    });
</script>

<div class="h-screen w-full mx-8 my-8 md:px-16">
    <div class="flex justify-between">
        <h1 class="text-3xl font-bold">
            {security.symbol}
            <span class="ml-3 font-semibold">{security.name}</span>
        </h1>
        <button
            class="flex bg-blue-200 px-4 py-2 rounded-full cursor-pointer disabled:cursor-not-allowed disabled:bg-gray-300"
            disabled={!canSave}
            onclick={() => saveSecurity(security)}
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
                        bind:value={growthPercent}
                    />
                </div>
                <div class="flex flex-col gap-1">
                    <label for="horizon">Estimated Horizon (years)</label>
                    <input
                        id="horizon"
                        type="number"
                        class="bg-white py-2 px-4 rounded-full"
                        bind:value={security.assumptions.years}
                    />
                </div>
                <div class="flex flex-col gap-1">
                    <label for="horizon">Safety Margin (%)</label>
                    <input
                        id="horizon"
                        type="number"
                        class="bg-white py-2 px-4 rounded-full"
                        bind:value={safetyMarginPercent}
                    />
                </div>
            </div>
            <div class="flex-1 bg-gray-100 rounded-xl p-6">
                <h2 class="text-2xl">Analysis</h2>
                <div class="flex flex-col gap-4 mt-4">
                    <h3 class="font-semibold">Technical Analysis</h3>
                    <div class="grid grid-cols-2 gap-4 md:grid-cols-4">
                        <div class="flex flex-col gap-1 min-w-20">
                            <p class="text-sm">
                                Average Income{security.financials.currency
                                    ? ` (${security.financials.currency})`
                                    : ""}
                            </p>
                            <p
                                class="bg-green-200 py-2 px-4 rounded-full text-base"
                            >
                                {Math.round(security.analysis.average_income)}
                            </p>
                        </div>
                        <div class="flex flex-col gap-1 min-w-20">
                            <p class="text-sm">D/E Ratio</p>
                            <p
                                class="bg-green-200 py-2 px-4 rounded-full text-base"
                            >
                                {(security.analysis.de_ratio * 100).toFixed(2)} %
                            </p>
                        </div>
                        <div class="flex flex-col gap-1 min-w-20">
                            <p class="text-sm">BVPS</p>
                            <p
                                class="bg-green-200 py-2 px-4 rounded-full text-base"
                            >
                                {security.analysis.bvps.toFixed(2)}
                            </p>
                        </div>
                        <div class="flex flex-col gap-1 min-w-20">
                            <p class="text-sm">CAGR</p>
                            <p
                                class="bg-green-200 py-2 px-4 rounded-full text-base"
                            >
                                {(security.analysis.cagr * 100).toFixed(2)} %
                            </p>
                        </div>
                    </div>
                    <h3 class="font-semibold">Estimated Bounds</h3>
                    <div class="grid grid-cols-2 gap-4 md:grid-cols-4">
                        <div class="flex flex-col gap-1 min-w-20">
                            <p class="text-sm">Lower Bound</p>
                            <p
                                class="bg-green-200 py-2 px-4 rounded-full text-base"
                            >
                                {security.analysis.lower.toFixed(2)}
                            </p>
                        </div>
                        <div class="flex flex-col gap-1 min-w-20">
                            <p class="text-sm">Target</p>
                            <p
                                class="bg-green-200 py-2 px-4 rounded-full text-base"
                            >
                                {security.analysis.target.toFixed(2)}
                            </p>
                        </div>
                        <div class="flex flex-col gap-1 min-w-20">
                            <p class="text-sm">Upper Bound</p>
                            <p
                                class="bg-green-200 py-2 px-4 rounded-full text-base"
                            >
                                {security.analysis.upper.toFixed(2)}
                            </p>
                        </div>
                    </div>
                    <h3 class="font-semibold">Nominal Bounds</h3>
                    <div class="grid grid-cols-2 gap-4 md:grid-cols-4">
                        <div class="flex flex-col gap-1 min-w-20">
                            <p class="text-sm">Lower Bound</p>
                            <p
                                class="bg-green-200 py-2 px-4 rounded-full text-base"
                            >
                                {security.analysis.nominal_lower.toFixed(2)}
                            </p>
                        </div>
                        <div class="flex flex-col gap-1 min-w-20">
                            <p class="text-sm">Target</p>
                            <p
                                class="bg-green-200 py-2 px-4 rounded-full text-base"
                            >
                                {security.analysis.nominal_target.toFixed(2)}
                            </p>
                        </div>
                        <div class="flex flex-col gap-1 min-w-20">
                            <p class="text-sm">Upper Bound</p>
                            <p
                                class="bg-green-200 py-2 px-4 rounded-full text-base"
                            >
                                {security.analysis.nominal_upper.toFixed(2)}
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
                            class="p-4 border-b border-r text-center border-gray-300 bg-gray-200"
                            >Balance Sheet</th
                        >
                        <th rowspan="2" class="p-4 border-b border-r border-gray-300 bg-gray-200">Actions</th>
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
                        <th class="p-4 border-b border-r border-gray-300 bg-gray-200"
                            >Book Value</th
                        >
                    </tr>
                </thead>
                <tbody>
                    {#if security.financials.financials.length === 0}
                        <tr>
                            <td colspan="7" class="text-center p-8 bg-gray-50"
                                >No financial record found.</td
                            >
                        </tr>
                    {:else}
                        {#each security.financials.financials as financial, idx}
                            <tr>
                                <td class="p-4 border-b border-r border-gray-300 bg-gray-50">
                                    <input 
                                        type="text" 
                                        class="p-1 rounded-lg"
                                        value={financial.date} 
                                        onchange={(e) => {
                                            financial.date = (<HTMLInputElement>e.target).value;
                                        }}
                                    />
                                </td>
                                <td class="p-4 border-b border-gray-300 bg-gray-50">
                                    <input 
                                        type="text" 
                                        class="p-1 rounded-lg"
                                        value={financial.income_statement.income.toLocaleString()} 
                                        onchange={(e) => {
                                            financial.income_statement.income = parseNumber((<HTMLInputElement>e.target).value)
                                            security.analysis = generateAnalysis(security.financials.financials, security.assumptions)
                                        }}
                                    />
                                </td>
                                <td class="p-4 border-b border-r border-gray-300 bg-gray-50">
                                    <input 
                                        type="text" 
                                        value={financial.income_statement.shares.toLocaleString()} 
                                        onchange={(e) => {
                                            financial.income_statement.shares = parseNumber((<HTMLInputElement>e.target).value)
                                            security.analysis = generateAnalysis(security.financials.financials, security.assumptions)
                                        }}
                                    />
                                </td>
                                <td class="p-4 border-b border-gray-300 bg-gray-50">
                                    {financial.balance_sheet.assets.toLocaleString()}
                                </td>
                                <td class="p-4 border-b border-gray-300 bg-gray-50">
                                    {financial.balance_sheet.liabilities.toLocaleString()}
                                </td>
                                <td class="p-4 border-b border-r border-gray-300 bg-gray-50">
                                    {financial.balance_sheet.book_value.toLocaleString()}
                                </td>
                                <td class="p-4 border-b border-gray-300 bg-gray-50">
                                    <button class="bg-red-400 px-4 py-2 rounded-full cursor-pointer" onclick={() => {
                                        security.financials.financials=[
                                            ...security.financials.financials.slice(0, idx),
                                            ...security.financials.financials.slice(idx + 1)
                                        ];}}>
                                        Delete
                                    </button>
                                </td>
                            </tr>
                        {/each}
                    {/if}
                </tbody>
            </table>
            <div class="flex justify-end">
                <button 
                    class="flex bg-blue-200 px-4 py-2 rounded-full cursor-pointer disabled:bg-gray-300 disabled:cursor-not-allowed"
                    onclick={() => {
                        security.financials.financials.push({
                            date: new Date().toLocaleDateString('en-UK'), // format date as DD/MM/YYYY
                            income_statement: {
                                income: 0,
                                shares: 0
                            },
                            balance_sheet: {
                                assets: 0,
                                liabilities: 0,
                                book_value: 0
                            }
                        });
                    }}
                >Add Row</button>
            </div>
        </div>
    </div>
</div>
