from pydantic import BaseModel, Field, validator


class Location(BaseModel):
    latitude: float
    longitude: float
    altitude: float
    accuracy: float
    verticalAccuracy: float = Field(alias="vertical_accuracy")
    bearing: float
    speed: float
    elapsedMs: int
    provider: str

    class Config:
        schema_extra = {
            "example": {
                "latitude": 31.0,
                "longitude": 130.0,
                "altitude": 0.0,
                "accuracy": 19.0,
                "vertical_accuracy": 19.0,
                "bearing": 0.0,
                "speed": 0.0,
                "elapsedMs": 39,
                "provider": "network",
            }
        }


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
