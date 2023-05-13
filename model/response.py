from pydantic import BaseModel, Field, validator


class Battery(BaseModel):
    health: str
    percentage: int = Field(ge=0, le=100)
    plugged: str
    status: str
    temperature: float
    current: int

    class Config:
        schema_extra = {
            "example": {
                "health": "GOOD",
                "percentage": 100,
                "plugged": "PLUGGED",
                "status": "CHARGING",
                "temperature": 32.2,
                "current": 320,
            }
        }

    @validator('temperature')
    def result_check(cls, v):
        return round(v, 2)
