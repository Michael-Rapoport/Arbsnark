import pytest
from brownie import ArbitrageTrader, accounts, reverts, Wei

@pytest.fixture
def arbitrage_trader(accounts):
    return ArbitrageTrader.deploy(accounts[0], {'from': accounts[0]})

# ... (existing tests)

def test_execute_collateral_swap(arbitrage_trader, accounts):
    # Mock DEX routers and token contracts
    uniswap_router = accounts[1]
    sushiswap_router = accounts[2]
    collateral_token = accounts[3]
    target_token = accounts[4]
    weth = accounts[5]

    arbitrage_trader.addDexRouter("UniswapV2", uniswap_router, {'from': accounts[0]})
    arbitrage_trader.addDexRouter("SushiSwap", sushiswap_router, {'from': accounts[0]})

    # Mock the collateral swap execution (this would require more complex mocking in a real test)
    path = [collateral_token, weth, target_token]
    dex_names = ["UniswapV2", "SushiSwap"]
    collateral_amount = Wei("1 ether")
    min_target_amount = Wei("1.01 ether")

    # Send some collateral token to the contract for the test
    collateral_token.transfer(arbitrage_trader, collateral_amount, {'from': accounts[0]})

    initial_balance = arbitrage_trader.balance()
    arbitrage_trader.executeCollateralSwap(collateral_token, target_token, collateral_amount, min_target_amount, {'from': accounts[0]})
    final_balance = arbitrage_trader.balance()

    assert final_balance > initial_balance, "Collateral swap should be profitable"