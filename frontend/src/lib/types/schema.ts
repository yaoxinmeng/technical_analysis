export type Security = {
    symbol: string
    name: string
    sector: string
    exchange_currency: string
    price: {
        price: number
        date: string
    }
    financials: FinancialsOverview
    analysis: Analysis
    assumptions: Assumptions
}

export type FinancialsOverview = {
    currency: string
    date: string
    financials: Financial[]
}

export type Financial = {
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
}

export type Analysis = {
    average_income: number
    de_ratio: number
    bvps: number
    cagr: number
    upper: number
    lower: number
    target: number
    nominal_upper: number
    nominal_lower: number
    nominal_target: number
}

export type Assumptions = {
    growth_rate: number
    years: number
    safety_margin: number
}

export type ExchangeRate = {
    from: string
    to: string
    rate: number
    date: string
}

export type SecurityOverview = {
    name: string
    sector: string
    exchange_currency: string
}