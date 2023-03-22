import base64

from fastapi import HTTPException, Request
from jsonrpcserver import Error
from jsonrpcserver.response import Response, ErrorResponse
from starlette import status


def compare_token(recieved_token: str, correct_token: str):
    if recieved_token == correct_token:
        return True
    return False


def authorize(request: Request):
    """
    :param request
    :return:
    """
    header_token = request.headers.get("authorization", '')
    if not header_token:
        return {
            "error": {
                "code": -32504,
                "message": "authorization parameter is missing!"
            },
            "id": request.get("id")
        }
    header_token = header_token.split(' ')[1]
    correct_token = get_token()
    if not compare_token(header_token, correct_token):
        return {
            "error": {
                "code": -32504,
                "message": "Incorrect token!"
            },
            "id": request.get("id")
        }

    return None

#
# def get_token_x():
#     message = b"PAYME_SETTINGS['MERCHANT_USERNAME']:PAYME_SETTINGS['MERCHANT_PASSWORD']"
#     token_bytes = base64.b64encode(message)
#     return token_bytes


def get_token():
    message = b"PAYME_SETTINGS['MERCHANT_USERNAME']:PAYME_SETTINGS['MERCHANT_PASSWORD']"
    token_bytes = base64.b64encode(message)
    token_str = token_bytes.decode('ascii')
    return token_str