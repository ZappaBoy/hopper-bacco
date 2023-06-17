import requests
from fastapi import HTTPException
from requests.adapters import HTTPAdapter
from starlette import status
from urllib3 import Retry


def bad_request(detail: str = 'Wrong params') -> HTTPException:
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


def get_requests_session():
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retries)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session
