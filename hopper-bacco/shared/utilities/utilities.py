from fastapi import HTTPException
from starlette import status


def bad_request(detail: str = 'Wrong params') -> HTTPException:
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
