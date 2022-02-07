from client import Client
import pandas as pd
import numpy as np
from pandas import DataFrame

CLIENT_ACCOUNT_COL = ['client', 'avail', 'held', 'total', 'locked']


class Bank:

    def __init__(self):
        self.clients = dict()
        self.client_ids = list()

    def _add_new_client(self, cid):
        formatted_cid = np.uint16(cid)
        self.client_ids.append(formatted_cid)
        self.clients[formatted_cid] = Client(formatted_cid)

    def is_account_open(self, cid):
        return np.uint16(cid) in self.client_ids

    def get_client(self, cid) -> Client:
        formatted_cid = np.uint16(cid)
        if formatted_cid not in self.client_ids:
            self._add_new_client(formatted_cid)
        return self.clients[formatted_cid]

    def print_all_clients(self):
        print("client,available,   held,   total, locked")
        for client in self.clients.values():
            print(client)

    def get_all_client_accounts_as_pd_df(self) -> DataFrame:
        df_all = pd.DataFrame(columns=['client', 'avail', 'held', 'total', 'locked'])
        for client in self.clients.values():
            df = client.get_client_as_df()
            df_all = pd.concat([df, df_all], ignore_index=True)
        return df_all
