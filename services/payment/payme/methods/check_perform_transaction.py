from services.order.models.order import Order, ORDER_STATUS
from services.payment import BasePayment
from services.payment.payme.schemas.check_perform_transaction import CheckPerformTransactionParamsSchema
from services.payment.payme.schemas.error_schema import ErrorResponse, Error
from services.payment.payme.schemas.success_schema import SuccessResponse
from services.payment.payme.utils.errors import errors


class CheckPerformTransaction(BasePayment):
    def __init__(self, request, params: CheckPerformTransactionParamsSchema):
        self._request = request
        self._params = params
        super(CheckPerformTransaction, self).__init__()

    def call(self):
        order: Order = self.get_order(self._params.account["order"])
        if not order:
            return ErrorResponse(
                error=Error(
                    code=errors["not_found"],
                    message={
                        "uz": "Buyurtma topilmadi",
                        "ru": "Заказ не найдено"
                    },
                    data={
                        "account": self._params.account["order"]
                    }
                )
            )

        """ check order status """
        if order.status in [ORDER_STATUS["canceled"], ORDER_STATUS["unprocessed"], ORDER_STATUS["delivered"]]:
            return ErrorResponse(
                error=Error(
                    code=errors["not_available"],
                    message={
                        "uz": "Buyurtma yaroqli emas",
                        "ru": "Заказ не доступно"
                    },
                    data={
                        "account": self._params.account["order"]
                    }
                )
            )

        """ check order price """
        if self.check_amount(self._params.amount):
            return SuccessResponse(
                result={
                    "allow": True
                }
            )

        else:
            return ErrorResponse(
                error=Error(
                    code=errors["incorrect_amount"],
                    message={
                        "uz": "Buyurtma summasi hato",
                        "ru": "Неверная сумма"
                    },
                    data={
                        "account": self._params.account["order"]
                    }
                )
            )


