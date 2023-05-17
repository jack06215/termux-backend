import os
import uuid
from uuid import uuid4

import requests
from dotenv import load_dotenv
from fastapi import BackgroundTasks, Depends, FastAPI, Response, status

import termux as tapi
from auth.api_key import get_api_key
from model.form import (LaunchAppRequest, NotificationRequest,
                        SmartHomeActionRequest, Text2SpeachRequest)
from model.response import Battery, Clipboard, Location
from pydantic_faker import generate_fake_data
from switchbot_sign import create_headers
from termux.android import execute

load_dotenv(f"./secrets/.env", override=True)

TERMUX = "termux-api"
JOINAPP = "join-api"
SWITCHBOT = "switchbot-api"

ACTION = "actions"
STATUS = "status"

SWITCHBOT_ENDPOINT = os.environ.get("SWITCHBOT_ENDPOINT_ENDPOINT")

app = FastAPI(
    title="Termux API Service",
    version="0.0.1",
    description="Termux API wrapper to interact with my Android phone",
    openapi_tags=[
        {
            "name": STATUS.capitalize(),
            "description": "Device and sensors status",
        },
        {
            "name": ACTION.capitalize(),
            "description": "Interact with device",
        },
    ]
)


@app.get(f"/{TERMUX}/battery", response_model=Battery, tags=[STATUS.capitalize()])
async def get_battery(api_key: str = Depends(get_api_key)):
    # res = generate_fake_data(Battery)
    rtn, res, err = tapi.API.battery()
    return Battery(**res)


@app.get(f"/{TERMUX}/location", response_model=Location, tags=[STATUS.capitalize()])
async def get_location(api_key: str = Depends(get_api_key)):
    rtn, res, err = tapi.API.location(provider="network")
    return Location(**res)


@app.get(f"/{TERMUX}/clipboard", response_model=Clipboard, tags=[STATUS.capitalize()])
async def get_clipboard(api_key: str = Depends(get_api_key)):
    rtn, res, err = tapi.Clipboard.getclipboard()
    return Clipboard(content=res)


@app.post(f"/{TERMUX}/text2speach", tags=[ACTION.capitalize()])
async def speak_tts(params: Text2SpeachRequest, background_tasks: BackgroundTasks, api_key: str = Depends(get_api_key)):
    background_tasks.add_task(
        tapi.TTS.tts_speak, params.content, language=params.country)
    return params


@app.post(f"/{TERMUX}/send-notification", tags=[ACTION.capitalize()])
async def send_notification(params: NotificationRequest, api_key: str = Depends(get_api_key)):
    rtn, res, err = tapi.Notification.notify(
        title=params.title, content=params.message, nid=params.id)
    return Response(status_code=status.HTTP_200_OK)


@app.post(f"/{TERMUX}/launch-app", tags=[ACTION.capitalize()])
async def launch_youtube(params: LaunchAppRequest, api_key: str = Depends(get_api_key)):
    rtn, res, err = execute(["bash", "./launch-app.sh", params.appName])
    return Response(status_code=status.HTTP_200_OK)


@app.post(f"/{JOINAPP}/send-notification", tags=[JOINAPP.capitalize()])
async def sh_turn_on(params: SmartHomeActionRequest, api_key: str = Depends(get_api_key)):
    api_key = os.environ.get("JOIN_APP_HTCM10_API_KEY")
    device_id = os.environ.get("JOIN_APP_HTCM10_DEVICE_ID")
    url = f"https://joinjoaomgcd.appspot.com/_ah/api/messaging/v1/sendPush?apikey={api_key}&deviceId={device_id}&title={params.get_command()}&text=Termux Backend"
    _ = requests.request("GET", url)
    return Response(status_code=status.HTTP_200_OK)


@app.get(f"/{SWITCHBOT}/devices")
async def sh_get_devices(api_key: str = Depends(get_api_key)):
    headers = create_headers(
        os.environ.get("SWITCHBOT_CLIENT_TOKEN"),
        os.environ.get("SWITCHBOT_CLIENT_SECRET")
    )

    response = requests.request(
        "GET", f"{SWITCHBOT_ENDPOINT}/v1.1/devices", headers=headers)

    return response.json()
