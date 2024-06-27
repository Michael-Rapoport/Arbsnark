
import pytest
from brownie import ArbitrageTrader, accounts, reverts, Wei

@pytest.fixture
def arbitrage_trader(accounts):
    return ArbitrageTrader.deploy(accounts[0], {'from': accounts[0]})

def test_add_dex_router(arbitrage_trader, accounts):
    arbitrage_trader.addDexRouter("UniswapV2", accounts[1], {'from': accounts[0]})
    assert arbitrage_trader.dexRouters("UniswapV2") == accounts[1]

def test_set_price_feed(arbitrage_trader, accounts):
    arbitrage_trader.setPriceFeed(accounts[1], accounts[2], {'from': accounts[0]})
    assert arbitrage_trader.priceFeeds(accounts[1]) == accounts[2]

def test_execute_arbitrage(arbitrage_trader, accounts):
    # Mock DEX routers and token contracts
    uniswap_router = accounts[1]
    sushiswap_router = accounts[2]
    token_a = accounts[3]
    token_b = accounts[4]
    weth = accounts[5]

    arbitrage_trader.addDexRouter("UniswapV2", uniswap_router, {'from': accounts[0]})
    arbitrage_trader.addDexRouter("SushiSwap", sushiswap_router, {'from': accounts[0]})

    # Mock the trade execution (this would require more complex mocking in a real test)
    path = [weth, token_a, token_b, weth]
    dex_names = ["UniswapV2", "SushiSwap", "UniswapV2"]
    amount_in = Wei("1 ether")
    min_amount_out = Wei("1.01 ether")

    # Send some ETH to the contract for the test
    accounts[0].transfer(arbitrage_trader, "2 ether")

    initial_balance = arbitrage_trader.balance()
    arbitrage_trader.executeArbitrage(path, dex_names, amount_in, min_amount_out, {'from': accounts[0]})
    final_balance = arbitrage_trader.balance()

    assert final_balance > initial_balance, "Arbitrage should be profitable"

def test_execute_flash_loan_arbitrage(arbitrage_trader, accounts):
    # This test would require mocking the Aave lending pool and flash loan process
    pass

def test_withdraw_funds(arbitrage_trader, accounts):
    initial_balance = accounts[1].balance()
    accounts[0].transfer(arbitrage_trader, "1 ether")
    arbitrage_trader.withdrawFunds(accounts[1], "0.5 ether", {'from': accounts[0]})
    assert accounts[1].balance() == initial_balance + Wei("0.5 ether")

def test_withdraw_token(arbitrage_trader, accounts, MockToken):
    token = MockToken.deploy({'from': accounts[0]})
    token.transfer(arbitrage_trader, "1000 ether", {'from': accounts[0]})
    arbitrage_trader.withdrawToken(token, accounts[1], "500 ether", {'from': accounts[0]})
    assert token.balanceOf(accounts[1]) == "500 ether"

def test_only_owner(arbitrage_trader, accounts):
    with reverts("Ownable: caller is not the owner"):
        arbitrage_trader.addDexRouter("UniswapV2", accounts[1], {'from': accounts[1]})

def test_reentrancy_guard(arbitrage_trader, accounts):
    # This test would require a mock contract that attempts a reentrant call
    pass
