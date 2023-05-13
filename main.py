from fastapi import FastAPI, Depends
from fastapi import Response, status
from fastapi.security.api_key import APIKey
from model.response import Battery
from model.form import LaunchAppRequest, NotificationRequest
from termux.android import execute
import auth
import termux as tapi

from dotenv import load_dotenv
load_dotenv(f"./secrets/.env", override=True)

ACTION = "actions"
STATUS = "status"

tags_metadata = [
    {
        "name": STATUS.capitalize(),
        "description": "Device and sensors status",
    },
    {
        "name": ACTION.capitalize(),
        "description": "Interact with device",
    },
]

app = FastAPI(
    title="Termux API Service",
    version="0.0.1",
    description="Termux API wrapper to interact with my Android phone",
    openapi_tags=tags_metadata
)


@app.get(f"/{STATUS}/battery", tags=[STATUS.capitalize()])
async def root(api_key: APIKey = Depends(auth.get_api_key)):
    rtn, res, err = tapi.API.battery()
    # data = {
    #     "health": "good",
    #     "percentage": 100,
    #     "plugged": "uy",
    #     "status": "asdfas",
    #     "temperature": 22.22,
    #     "current": 100
    # }
    return Battery(**res)


@app.post(f"/{ACTION}/send-notification", tags=[ACTION.capitalize()])
async def notify(params: NotificationRequest, api_key: APIKey = Depends(auth.get_api_key)):
    rtn, res, err = tapi.Notification.notify(
        title=params.title, content=params.message, nid=params.id)
    print(res)
    return Response(status_code=status.HTTP_200_OK)


@app.post(f"/{ACTION}/launch-app", tags=[ACTION.capitalize()])
async def launch_youtube(params: LaunchAppRequest, api_key: APIKey = Depends(auth.get_api_key)):
    rtn, res, err = execute(["bash", "./launch-app.sh", params.appName])
    print(res)
    return Response(status_code=status.HTTP_200_OK)
