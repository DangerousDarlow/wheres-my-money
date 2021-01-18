from datetime import date
from uuid import UUID, uuid4

class Transaction:
    def __init__(self, id = uuid4(), date = date.today(), amount = 0, description = ''):
        self.id = id
        self.date = date
        self.amount = amount
        self.description = description

AmountScalingFactor = 1000000
