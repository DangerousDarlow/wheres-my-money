from datetime import date
from uuid import UUID, uuid4

class Transaction:
    id = uuid4()
    date = date.today()
    amount = 0
    description = str