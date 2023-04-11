import datetime

from fastapi import HTTPException
from starlette import status

from common.get_db import get_db
from services.order.models.transaction import Transaction
from services.payment.payme.schemas.error_schema import ErrorResponse, Error
from services.payment.payme.schemas.success_schema import SuccessResponse
from services.payment.payme.utils.errors import errors


def get_transaction(transaction_id: int):
    with get_db() as db:
        transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    return transaction

def check_condition_transaction(transaction: Transaction):
    """ check state """
    if transaction.state != 1:
        return ErrorResponse(
                error=Error(
                    code=errors["not_able_to_compute_operation"],
                    message={
                        "uz": "Amaliyotni amalga oshirib bo'lmaydi",
                        "ru": "Невозможно выполнить операцию."
                    }
                ),
                id=transaction.id
            )

    """ check timeout """
    if timeout(transaction.created_at):
        if cancel_transaction(transaction):
            return ErrorResponse(
                error=Error(
                    code=errors["not_able_to_compute_operation"],
                    message={
                        "uz": "Tranzaksiya bekor qilindi!",
                        "ru": "Транзакция отменена!"
                    }
                ),
                id=transaction.id
            )
    else:
        return SuccessResponse(
            result={
                "state": transaction.state,
                "create_time": transaction.created_at,
                "transaction": transaction.transaction,
                "receivers": None
            }
        )


def timeout(created_at):
    left = datetime.datetime.now() - created_at
    time_out = datetime.timedelta(hours=12)
    if left < time_out:
        return False
    else:
        return True


def cancel_transaction(transaction):
    try:
        with get_db() as db:
            transaction = db.query(Transaction).filter_by(id=transaction.id).first()
            transaction.state = -1
            transaction.reason = TRANSACTION_REASON["cancel_by_timeout"]

            db.commit()
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_304_NOT_MODIFIED,
            detail=f"Canceling of transaction has not completed: str(ex)"
        )

    return True


TRANSACTION_REASON = {
    "cancel_by_timeout": 4
}