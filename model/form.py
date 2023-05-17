import json

from pydantic import BaseModel, Field

APP_NAME_LIST = {
    "pokemongo": "pokémon-go",
}

TTS_LANGUAGE_CODE = {
    "Japan": "ja_JP",
    "Taiwan": "zh_TW",
    "Australia": "en_AU",
}

SWITCHBOT_AC_DEVICE = {
    "FUK.Akasaka": "01-202305161536-51343289",
}

SWITCHBOT_SWITCH_DEVICE = {
    "FUK.Akasaka": "ECF5617EF399",
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


class SetAirConditionRequest(BaseModel):
    device: str = ""
    temperature: int
    mode: str = "2"
    fanSpeed: str = "2"
    powerState: int = Field(ge=0, le=1)

    def __init__(self, **data):
        super().__init__(**data)
        try:
            self.device = SWITCHBOT_AC_DEVICE[self.device]
        except:
            pass

    def get_command(self):
        mode_cmd = "on" if self.powerState == 1 else "off"
        payload = json.dumps({
            "command": "setAll",
            "parameter": f"{self.temperature},{self.mode.lower()},{self.fanSpeed.lower()},{mode_cmd}",
            "commandType": "command"
        })

        return payload


class SetSwitchDeviceRequest(BaseModel):
    device: str = ""
    powerState: int = Field(ge=0, le=1)

    def __init__(self, **data):
        super().__init__(**data)
        try:
            self.device = SWITCHBOT_SWITCH_DEVICE[self.device]
        except:
            pass

    def get_command(self):
        cmd = "turnOn" if self.powerState == 1 else "turnOff"
        payload = json.dumps({
            "command": cmd,
            "commandType": "command"
        })

        return payload
