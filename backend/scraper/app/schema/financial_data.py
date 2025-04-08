from pydantic import BaseModel

class FinancialData(BaseModel):
    share_price: int
    earnings_per_share: float
    dividend_yield: int
    market_cap: int
    debt: int
    net_assets: int
    net_profits: int