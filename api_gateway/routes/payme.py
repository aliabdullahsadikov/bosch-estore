from typing import Union

from fastapi import APIRouter, Request, Response, HTTPException, Depends
# from jsonrpcserver import Result, Success, method, async_dispatch as dispatch
from starlette import status
from starlette.responses import JSONResponse

from services.payment.payme.utils.authorize import authorize

payme_routes = APIRouter()

#
# @method
# async def CheckPerformTransaction():
#     i = "i"
#     return i
#
#
# @method(name="CheckTransaction")
# def CheckTransaction() -> Result:
#     i = "i"
#     return Success("I got it!")


@payme_routes.post("/payme")
async def compute_payme_operations(request: Request):

    #  check auth
    check_auth = authorize(request)
    if check_auth:
        return check_auth

    #
    request_body = await request.json()
    # response = await serve(request_body)
    # return request_body

#
# class Composer:
#     def __init__(self, request: Request):
#         self._request = request
#
#     async def call(self):
#         if not self._request["method"]:
#             return "method parameter is empty"
#
#         if self._request["method"] not in paycom_methods():
#             return "Method not found"
#
#         method = self._request["method"]
#         return await self._dispatch(method)
#
#     async def _dispatch(self, method):
#         return await method()





def paycom_methods():
    return [
        "CheckPerformTransaction",
        "CreateTransaction",
        "PerformTransaction",
        "CancelTransaction",
        "CheckTransaction",
        "GetStatement"
    ]