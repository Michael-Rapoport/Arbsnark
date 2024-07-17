import pytest
from brownie import ArbitrageTrader, accounts, reverts, Wei

@pytest.fixture
def arbitrage_trader(accounts):
    return ArbitrageTrader.deploy(accounts[0], {'from': accounts[0]})

def test_reentrancy_guard(arbitrage_trader, accounts):
    # Mock a contract that attempts a reentrant call
    class ReentrancyAttacker:
        def __init__(self, arbitrage_trader):
            self.arbitrage_trader = arbitrage_trader

        def attack(self):
            self.arbitrage_trader.withdrawFunds(accounts[1], Wei("0.5 ether"), {'from': accounts[1]})
            self.arbitrage_trader.attack()

    attacker = ReentrancyAttacker(arbitrage_trader)
    with reverts("ReentrancyGuard: reentrant call"):
        attacker.attack()