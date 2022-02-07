import pandas as pd
from pandas import DataFrame

ROUNDING_PRECISION = 4


class Client:

    def __init__(self, id):
        self.client_id = id
        self.avail = 0.0
        self.held = 0.0
        self.total = 0.0
        self.locked = "false"

    def __str__(self):
        return f"{self.client_id: 6}," \
               f"{round(self.avail, ROUNDING_PRECISION): 9}," \
               f"{round(self.held, ROUNDING_PRECISION): 7}," \
               f"{round(self.total, ROUNDING_PRECISION): 8},  {self.locked}"

    def deposit(self, amount):
        self.avail += amount
        self.total += amount

    def withdrawal(self, amount):
        if self.avail >= amount:
            self.avail -= amount
            self.total -= amount

    def dispute(self, amount):
        self.held += amount
        self.avail -= amount

    def resolve(self, amount):
        self.held -= amount
        self.avail += amount

    def chargeback(self, amount):
        self.held -= amount
        self.total -= amount
        self.locked = "true"

    def get_client_as_df(self) -> DataFrame:
        return pd.DataFrame([[self.client_id,
                              round(self.avail, ROUNDING_PRECISION),
                              round(self.held, ROUNDING_PRECISION),
                              round(self.total, ROUNDING_PRECISION),
                              self.locked
                              ]], columns=['client', 'avail', 'held', 'total', 'locked'])

