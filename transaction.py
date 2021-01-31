from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4


class Transaction:
    def __init__(self, id, timestamp, amount, description, added, account):
        self.id = id
        self.timestamp = timestamp
        self.amount = amount
        self.description = description
        self.added = added
        self.account = account

    def to_string(self):
        amount = Decimal(self.amount) / AmountScalingFactor
        amountStr = '{0:.2f}'.format(amount)
        return '{:<}   {:<}   {:>8}   {:<}'.format(str(self.id), str(self.timestamp), amountStr, self.description)


AmountScalingFactor = 1000000
