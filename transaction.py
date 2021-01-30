from datetime import datetime
from uuid import UUID, uuid4


class Transaction:
    def __init__(self, id, timestamp, amount, description, added, account):
        self.id = id
        self.timestamp = timestamp
        self.amount = amount
        self.description = description
        self.added = added
        self.account = account


AmountScalingFactor = 1000000
