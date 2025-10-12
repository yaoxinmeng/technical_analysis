import type { Analysis, Financial, Assumptions } from "$db/schema";

const INTEREST_RATE = 0.0328;

export function generateAnalysis(financials: Financial[], assumptions: Assumptions): Analysis {
    const incomes = financials.map((f) => f.income_statement.income);
    const latestBalance = financials[0].balance_sheet;
    const latestShares = financials[0].income_statement.shares;

    // calculate inflation-adjusted average income using up to 10 years of historic data
    let averageIncome = calculateInflationAdjustedAverage(incomes.slice(0, Math.min(incomes.length, 10)));
    let nominalTarget = averageIncome * assumptions.years / latestShares;
    let target = calculateGpSum(averageIncome, 1 + assumptions.growth_rate, assumptions.years) / latestShares;
    return {
        average_income: averageIncome,
        de_ratio: latestBalance.liabilities / latestBalance.assets,
        bvps: latestBalance.book_value / latestShares,
        cagr: (incomes[0] / incomes[incomes.length - 1]) ** (1 / (incomes.length - 1)) - 1,
        upper: target * (1 + assumptions.safety_margin),
        lower: target * (1 - assumptions.safety_margin),
        target: target,
        nominal_upper: nominalTarget * (1 + assumptions.safety_margin),
        nominal_lower: nominalTarget * (1 - assumptions.safety_margin),
        nominal_target: nominalTarget,
    }
}

/**
 * Calculates the average of an array of numbers.
 * @param {number[]} incomes - an array of numbers
 * @returns {number} the average of the array
 */
function calculateInflationAdjustedAverage(incomes: number[]) {
    if (incomes.length === 0) return 0;
    let sum = 0;
    for (let i = 0; i < incomes.length; i++) {
        sum += incomes[i] * (1 + INTEREST_RATE) ** i;
    }
    return sum / incomes.length;
}

/**
 * Calculates the sum of a geometric progression.
 * @param {number} a - initial value
 * @param {number} r - common ratio
 * @param {number} n - number of terms
 * @returns {number} the sum of the geometric progression
 */
function calculateGpSum(a: number, r: number, n: number) {
    if (r === 1) return a * n;
    return a * (r ** n - 1) / (r - 1);
}

/**
 * Updates existing financials with new ones, prioritizing existing ones (unless it is TTM)
 * @param existing existing financials
 * @param newFinancials 
 * @returns 
 */
export function updateExistingFinancials(existing: Financial[], newFinancials: Financial[]): Financial[] {
    for (let i = 0; i < newFinancials.length; i++) {
        let index = existing.findIndex(
            (f) => f.date === newFinancials[i].date,
        );
        // if date is not present in existing, add it from new financials
        if (index !== -1) {
            existing.push(newFinancials[i]);
            continue;
        } 
        // the date is TTM, we replace the existing one
        if (newFinancials[i].date === "TTM") {
            existing[index] = newFinancials[i];
            continue;
        }
        // if any of the existing data has a value of 0, we replace it with new data
        if (
            existing[index].income_statement.income === 0 || 
            existing[index].income_statement.shares === 0 ||
            existing[index].balance_sheet.assets === 0 ||
            existing[index].balance_sheet.liabilities === 0 ||
            existing[index].balance_sheet.book_value === 0 
        ) {
            existing[index] = newFinancials[i];
        }
    }
    // sort financials by date
    newFinancials.sort((a, b) => {
        if (a.date === "TTM") return -1;
        if (b.date === "TTM") return 1;
        return (
            new Date(b.date).getSeconds() - new Date(a.date).getSeconds()
        );
    });
    // since balance sheet might not have TTM, we need to handle that case
    // we use the balance sheet data from the latest date available
    if(newFinancials[0].balance_sheet.assets === -1) {
        newFinancials[0].balance_sheet = newFinancials[1].balance_sheet;
    }

    return newFinancials;
}