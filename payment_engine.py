import sys
import pandas as pd
from txproc import TxProcessor

CHUNK_SIZE = 10000


def print_help():
    print("""
Error:
    Mandatory argument is csv file, example:
    python payment_engine.py transactions.csv
    """)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)
    transaction_processor = TxProcessor()
    df = pd.read_csv(sys.argv[1], chunksize=CHUNK_SIZE)
    for chunk in df:
        for _, row in chunk.iterrows():
            tx = (row['type'], row['client'], row['tx'], row['amount'])
            transaction_processor.process_tx(*tx)
    transaction_processor.print_accounts()