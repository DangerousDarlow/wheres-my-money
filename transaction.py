from datetime import date
from uuid import UUID, uuid4


class Transaction:
    def __init__(self, id=uuid4(), timestamp=date.today(), amount=0, description=''):
        self.id = id
        self.timestamp = timestamp
        self.amount = amount
        self.description = description


AmountScalingFactor = 1000000
