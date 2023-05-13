import os

from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.status import HTTP_403_FORBIDDEN

api_key_header = HTTPBearer()


async def get_api_key(api_key_header: HTTPAuthorizationCredentials = Security(api_key_header)):
    print(api_key_header)
    if api_key_header.credentials == os.getenv("API_KEY"):
        return api_key_header
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate API KEY"
        )
