from pydantic import BaseModel

class PredictRequestBody(BaseModel):
    prices: list[float]