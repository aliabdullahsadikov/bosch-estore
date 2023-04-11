from common.get_db import get_db
from services.order.models.transaction import Transaction
from services.payment.payme.schemas.check_transaction import ValidateCheckTransaction
from pydantic import validator, BaseModel, ValidationError

from services.payment.payme.schemas.create_transaction import ValidatorCreateTransaction
from services.payment.payme.schemas.error_schema import ErrorResponse, Error
from services.payment.payme.schemas.success_schema import SuccessResponse
from services.payment.payme.utils.errors import errors
from services.payment.payme.utils.transaction import get_transaction, check_condition_transaction


class CreateTransaction:

    def __init__(self, params):
        self.params = params
        self.error = None

    def call(self):
        """ validation """
        validate = self._validate()
        if not validate["valid"]:
            return validate["data"]

        """ find transaction by id """
        transaction = get_transaction(self.params["id"])
        if not transaction:
            return ErrorResponse(
                error=Error(
                    code=errors["transaction_not_found"],
                    message={
                        "uz": "Tranzaksiya topilmadi",
                        "ru": "Транзакция не найдено"
                    }
                ),
                id=self.params["id"]
            )
        else:
            return check_condition_transaction(transaction)

    def _validate(self):
        try:
            data = ValidatorCreateTransaction(**self.params)
        except ValidationError as err:
            return {
                    "valid": False,
                    "data": ErrorResponse(
                        error=Error(
                            code=errors["paycom_error"],
                            message={
                                "uz": f"Parametrlarda kamchilik: {err}",
                                "ru": f"Отсутствующие параметры: {err}"
                            }
                        ),
                        id=self.params["id"]
                    )
                }

        return {
            "valid": True,
            "data": data
        }
