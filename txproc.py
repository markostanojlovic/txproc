import pandas as pd
from pandas import DataFrame
from bank import Bank


class TxProcessor:

    def __init__(self):
        self.bank = Bank()
        self.tx_log = pd.DataFrame(columns=['type', 'client', 'tx', 'amount'])
        self.tx_under_dispute = list()

    def _find_dw_tx(self, txid) -> DataFrame:
        """
        Assumption: dispute can happen only on deposit type of transaction
        """
        return self.tx_log.loc[(self.tx_log['tx'] == txid) &
                               (self.tx_log['type'] == "deposit")]

    def _get_amount(self, tx_df: DataFrame):
        if tx_df.empty:
            return 0.0
        return tx_df["amount"].iloc[-1]

    def is_txid_uniq(self, txid):
        search = self.tx_log.loc[(self.tx_log['tx'] == txid)
                                 & (self.tx_log['type'].isin(["deposit", "withdrawal"]))]
        return search.empty

    def process_tx(self, tx_type, cid, txid, amount=None):
        if tx_type == "deposit":
            if self.is_txid_uniq(txid):
                cl = self.bank.get_client(cid)
                if cl.locked == "false":
                    cl.deposit(amount)
        elif tx_type == "withdrawal":
            if self.bank.is_account_open(cid) and self.is_txid_uniq(txid):
                cl = self.bank.get_client(cid)
                if cl.locked == "false":
                    cl.withdrawal(amount)
        elif tx_type == "dispute":
            if self.bank.is_account_open(cid) and txid not in self.tx_under_dispute:
                dispute_tx = self._find_dw_tx(txid)
                dispute_amount = self._get_amount(dispute_tx)
                cl = self.bank.get_client(cid)
                if cl.locked == "false":
                    cl.dispute(dispute_amount)
                self.tx_under_dispute.append(txid)
        elif tx_type == "resolve":
            if txid in self.tx_under_dispute and self.bank.is_account_open(cid):
                resolve_tx = self._find_dw_tx(txid)
                resolve_amount = self._get_amount(resolve_tx)
                cl = self.bank.get_client(cid)
                if cl.locked == "false":
                    cl.resolve(resolve_amount)
                self.tx_under_dispute.remove(txid)
        elif tx_type == "chargeback":
            if txid in self.tx_under_dispute and self.bank.is_account_open(cid):
                chback_tx = self._find_dw_tx(txid)
                chback_amount = self._get_amount(chback_tx)
                cl = self.bank.get_client(cid)
                if cl.locked == "false":
                    cl.chargeback(chback_amount)
                self.tx_under_dispute.remove(txid)
        else:
            return
        new_tx_log = pd.DataFrame([[tx_type, cid, txid, amount]], columns=self.tx_log.columns)
        self.tx_log = pd.concat([self.tx_log, new_tx_log], ignore_index=True)

    def print_accounts(self):
        self.bank.print_all_clients()

    def get_all_accounts(self):
        return self.bank.get_all_client_accounts_as_pd_df()

    def print_all_tx_logs(self):
        print("\n-----------------\n")
        print(self.tx_log)