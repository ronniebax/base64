import base64
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi.logger import logger as fastapi_logger
import logging
from fastapi import HTTPException, status, Security
from fastapi.security import APIKeyHeader
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

API_KEY = os.environ.get('KEY')
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)

# Enabling logging in docker container
gunicorn_error_logger = logging.getLogger("gunicorn.error")
gunicorn_logger = logging.getLogger("gunicorn")
uvicorn_access_logger = logging.getLogger("uvicorn.access")
uvicorn_access_logger.handlers = gunicorn_error_logger.handlers
fastapi_logger.handlers = gunicorn_error_logger.handlers
if __name__ != "__main__":
    fastapi_logger.setLevel(gunicorn_logger.level)
else:
    fastapi_logger.setLevel(logging.DEBUG)


class base64Request(BaseModel):
    input: str


class base64Response(BaseModel):
    status: int
    result: str


# setting the api key
def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )


def make_base64(data):
    data = str(data)
    return base64.b64encode(data.encode()).decode()


@app.post('/base64')
def base64_api(data:base64Request, api_key: str = Security(get_api_key)):
    try:
        return {
            "status": 200,
            "result": make_base64(data.input)
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={'reason': str(e)})