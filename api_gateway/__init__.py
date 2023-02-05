import os
from contextlib import contextmanager

from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer
# from sqlalchemy.orm import session
from api_gateway.routes.cart import cart_routes
from api_gateway.routes.category import category_routes
from api_gateway.routes.order import order_routes
from api_gateway.routes.product import product_routes
from api_gateway.routes.user import user_routes
from common.config import config
from common.database import SessionLocal

""" Application """
app = FastAPI()
app.mount("/static", StaticFiles(directory=os.path.abspath("common/static")), name="static")


@app.on_event("startup")
async def startup():
    print("hello")
    # await database.connect()


@app.on_event("shutdown")
async def shutdown():
    print("By-By")
    # await database.disconnect()


"""  Including Product Routes  """
app.include_router(product_routes, prefix="/api/v1", tags=["Product Routes"])


"""  Including User Routes  """
app.include_router(user_routes, prefix="/api/v1", tags=["User Routes"])


"""  Including Category Routes  """
app.include_router(category_routes, prefix="/api/v1", tags=["Category Routes"])


"""  Including Cart Routes  """
app.include_router(cart_routes, prefix="/api/v1", tags=["Cart Routes"])


"""  Including Cart Routes  """
app.include_router(order_routes, prefix="/api/v1", tags=["Order Routes"])


""" LOGGING """


# def send_alert(text):
#     bot = telebot.TeleBot('2136464490:AAFCCAsoM9I4lSkTDWaI0muO0aYTDiz0IgQ')
#     bot.send_message(chat_id='-1001748390698', text=f"@m_mirfayziyev \n <code> {text} </code>", parse_mode='html')
#
#     return {"detail": "Sent to the channel"}

#
# @app.exception_handler(Exception)
# async def debug_exception_handler(request: Request, exc: Exception):
#     import traceback
#     text = traceback.format_exception(type(exc), value=exc, tb=exc.__traceback__)
#     message = "❌ User Service Exception ❌ \n MESSAGE: "
#     send_alert(message + ''.join(text))
#
#     return Response(
#         content="".join(
#             traceback.format_exception(
#                 etype=type(exc), value=exc, tb=exc.__traceback__
#             )
#         )
#     )

