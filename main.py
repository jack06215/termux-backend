from dotenv import load_dotenv
from fastapi import BackgroundTasks, Depends, FastAPI, Response, status

import termux as tapi
from auth.api_key import get_api_key
from model.form import (LaunchAppRequest, NotificationRequest,
                        Text2SpeachRequest)
from model.response import Battery, Clipboard, Location
from pydantic_faker import generate_fake_data
from termux.android import execute

load_dotenv(f"./secrets/.env", override=True)


ACTION = "actions"
STATUS = "status"

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


@app.get(f"/{STATUS}/battery", response_model=Battery, tags=[STATUS.capitalize()])
async def get_battery(api_key: str = Depends(get_api_key)):
    # res = generate_fake_data(Battery)
    rtn, res, err = tapi.API.battery()
    return Battery(**res)


@app.get(f"/{STATUS}/location", response_model=Location, tags=[STATUS.capitalize()])
async def get_location(api_key: str = Depends(get_api_key)):
    # res = generate_fake_data(Location)
    rtn, res, err = tapi.API.location(provider="network")
    return Location(**res)


@app.get(f"/{STATUS}/clipboard", response_model=Clipboard, tags=[STATUS.capitalize()])
async def get_clipboard(api_key: str = Depends(get_api_key)):
    # res = generate_fake_data(Location)
    rtn, res, err = tapi.Clipboard.getclipboard()
    return Clipboard(content=res)


@app.post(f"/{ACTION}/text2speach", tags=[ACTION.capitalize()])
async def speak_tts(params: Text2SpeachRequest, background_tasks: BackgroundTasks, api_key: str = Depends(get_api_key)):
    background_tasks.add_task(
        tapi.TTS.tts_speak, params.content, language=params.country)
    return Response(status_code=status.HTTP_200_OK)


@app.post(f"/{ACTION}/send-notification", tags=[ACTION.capitalize()])
async def send_notification(params: NotificationRequest, api_key: str = Depends(get_api_key)):
    rtn, res, err = tapi.Notification.notify(
        title=params.title, content=params.message, nid=params.id)
    print(res)
    return Response(status_code=status.HTTP_200_OK)


@app.post(f"/{ACTION}/launch-app", tags=[ACTION.capitalize()])
async def launch_youtube(params: LaunchAppRequest, api_key: str = Depends(get_api_key)):
    rtn, res, err = execute(["bash", "./launch-app.sh", params.appName])
    print(res)
    return Response(status_code=status.HTTP_200_OK)
