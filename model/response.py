from pydantic import BaseModel, validator


class Battery(BaseModel):
    health: str
    percentage: int
    plugged: str
    status: str
    temperature: float
    current: int

    @validator('temperature')
    def result_check(cls, v):
        return round(v, 2)
