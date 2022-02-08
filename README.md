# txproc

## Setup 

In `requirement.txt` is list of external python libs required to run the txproc.  

## How to run 

In python virtual env, run

`python payment_engine.py transactions.csv`

`transactions.csv` is available to test if txproc is working. There are cases that should be covering same cases as in integration tests. This means both basic scenarios and scenarios that discard tx due to something wrong with it.


## About implementation 

- Performance is not considered during the implementation, only perf consideration was chunking huge csv file
- Security was also not taken into account
- Data types and input data correctness is assumed and not handled
- Exception handling is not implemented

`Client` class stores basic info for client account. `Bank` is storing client accounts and one tx processing engine is instantiating one Bank object and processes transaction according to input by type. Storing Client object is done in dictionary, which is not optimal for performance and large transactions (pandas data frames would suite better), but it's fastest impl solution. 

### Additional assumptions: 

- Transaction ID should be unique, duplicate tx ids should be ignored and discarded
- Is request to withdraw more funds than available, tx is discarded
- Dispute for withdrawal is ignored as well as other types except for deposit

