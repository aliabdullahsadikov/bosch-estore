from pydantic import BaseModel


class CheckPerformTransactionParamsSchema(BaseModel):
    amount: int
    account: dict

