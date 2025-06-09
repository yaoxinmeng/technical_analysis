export type Security = {
    symbol: string
    name: string
    sector: string
    exchange_currency: string
    price: {
        price: number
        date: string
    }
    financials: {
        currency: string
        date: string
        financials: {
            date: string
            balance_sheet: {
                assets: number
                liabilities: number
                book_value: number
            },
            income_statement: {
                income: number
                shares: number
            }
        }[]
    }
    analysis: {
        average_income: number
        pe_ratio: number
        de_ratio: number
        bvps: number
        cagr: number
        upper: number
        lower: number
        target: number
        nominal_upper: number
        nominal_lower: number
        nominal_target: number
        assumptions: {
            growth_rate: number
            years: number
        }
    }
}