import pytest
from brownie import ArbitrageTrader, accounts, reverts, Wei
from unittest.mock import patch

@pytest.fixture
def arbitrage_trader(accounts):
    return ArbitrageTrader.deploy(accounts[0], {'from': accounts[0]})

def test_execute_flash_loan_arbitrage(arbitrage_trader, accounts):
    # Mock the Aave lending pool
    with patch('contracts.ArbitrageTrader.aavePool') as mock_aave_pool:
        mock_aave_pool.flashLoan.return_value = None
        mock_aave_pool.repay.return_value = None

        # Execute the flash loan arbitrage
        path = [accounts[1], accounts[2], accounts[3]]
        dex_names = ['UniswapV2', 'SushiSwap']
        amount_in = Wei('1 ether')
        min_amount_out = Wei('1.01 ether')

        arbitrage_trader.executeArbitrageWithFlashLoan(path, dex_names, amount_in, min_amount_out, {'from': accounts[0]})

        # Verify that the flash loan was requested and repaid
        mock_aave_pool.flashLoan.assert_called_once_with(arbitrage_trader, accounts[1], amount_in, b'')
        mock_aave_pool.repay.assert_called_once_with(accounts[1], amount_in, 2, arbitrage_trader)