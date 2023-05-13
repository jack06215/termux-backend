from pydantic import BaseModel, Field

APP_NAME_LIST = {
    "pokemongo": "pokémon-go",
}


class NotificationRequest(BaseModel):
    title: str
    id: int = 1
    message: str = None


class LaunchAppRequest(BaseModel):
    appName: str = Field(alias="app_name")

    def __init__(self, **data):
        super().__init__(**data)
        try:
            self.appName = APP_NAME_LIST[self.appName]
        except:
            pass
