import pytest
from tests.integration_common import *


def test_deposit_amount_type_int():
    tx_input = [("deposit", 1, 1, 1)]
    expected_output = [[1, 1.0, 0.0, 1.0, "false"]]
    assert_dataframes_match(process_all_tx(tx_input), expected_df(expected_output))


@pytest.mark.skip(reason="feature under dev")
def test_deposit_amount_type_str():
    tx_input = [("deposit", 1, 1, "a")]
    assert process_all_tx(tx_input).empty
