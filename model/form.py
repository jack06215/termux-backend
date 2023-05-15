from pydantic import BaseModel, Field

APP_NAME_LIST = {
    "pokemongo": "pokémon-go",
}

TTS_LANGUAGE_CODE = {
    "Japan": "ja_JP",
    "Taiwan": "zh_TW",
    "Australia": "en_AU",
}

class Text2SpeachRequest(BaseModel):
    country: str
    content: str
    
    def __init__(self, **data):
        super().__init__(**data)
        try:
            self.country = TTS_LANGUAGE_CODE[self.country]
        except:
            pass

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

class SmartHomeActionRequest(BaseModel):
    location: str
    device: str
    action: str
    id: int = 1
    
    def get_command(self):
        return f"{self.location.upper()}.{self.device.capitalize()}.{self.action.capitalize()}"
