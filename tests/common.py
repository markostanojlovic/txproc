import pytest
from txproc import TxProcessor
import pandas as pd


CLIENT_ACCOUNT_COL = ['client', 'avail', 'held', 'total', 'locked']


def process_all_tx(input_txs):
    tx_processor = TxProcessor()
    for tx in input_txs:
        tx_processor.process_tx(*tx)
    output_df = tx_processor.get_all_accounts()
    return output_df


def expected_df(expected_output):
    return pd.DataFrame(expected_output, columns=CLIENT_ACCOUNT_COL)


def assert_dataframes_match(df1, df2):
    pd.testing.assert_frame_equal(df1.sort_values(by=['client']).reset_index(drop=True),
                                  df2.sort_values(by=['client']).reset_index(drop=True),
                                  check_dtype=False)

