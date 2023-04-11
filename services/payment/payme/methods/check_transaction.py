from common.get_db import get_db
from services.order.models.transaction import Transaction
from services.payment.payme.schemas.check_transaction import ValidateCheckTransaction
from pydantic import validator, BaseModel, ValidationError

from services.payment.payme.schemas.error_schema import ErrorResponse, Error
from services.payment.payme.schemas.success_schema import SuccessResponse
from services.payment.payme.utils.errors import errors


class CheckTransaction:

    def __init__(self, params):
        self.params = params
        self.error = None

    def call(self):
        #  validate
        validate = self._validate()
        if not validate["valid"]:
            return validate["data"]

        #  perform
        with get_db() as db:
            transaction = db.query(Transaction).filter(Transaction.id == self.params["id"]).first()
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

            return SuccessResponse(
                result={
                        "create_time": transaction.created_at,
                        "perform_time": transaction.updated_at,
                        "cancel_time": transaction.cancel_time,
                        "transaction": transaction.id,
                        "state": transaction.state,
                        "reason": None
                    },
                id=self.params["id"]
            )

    def _validate(self):
        try:
            data = ValidatorCheckTransaction(**self.params)
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


class ValidatorCheckTransaction(BaseModel):
    id: str