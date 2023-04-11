from typing import Union

from fastapi import APIRouter, Request, Response, HTTPException, Depends
# from jsonrpcserver import Result, Success, method, async_dispatch as dispatch
from starlette import status
from starlette.responses import JSONResponse

from services.order.models.transaction import Transaction
from services.payment.payme.methods.check_perform_transaction import CheckPerformTransaction
from services.payment.payme.methods.create_transaction import CreateTransaction
from services.payment.payme.schemas.check_perform_transaction import CheckPerformTransactionParamsSchema
from services.payment.payme.utils.authorize import authorize
from services.payment.payme.utils.errors import errors

from services.payment.payme.methods.check_transaction import CheckTransaction

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
    """
    auth_error = authorize(request)
    if auth_error:
        return auth_error
    """

    #  dispatch method
    request_body = await request.json()
    response = await call_method(request_body, request_body["method"], request_body["params"])
    return response


async def call_method(request, method, params: dict) -> dict:
    if method == "CheckPerformTransaction":
        response = await CheckPerformTransaction(request, CheckPerformTransactionParamsSchema(**params)).call()
    elif method == "CreateTransaction":
        response = await CreateTransaction(params).call()
    elif method == "CheckTransaction":
        response = await CheckTransaction(params).call()
    else:
        response = "Undefined method"
    return response






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