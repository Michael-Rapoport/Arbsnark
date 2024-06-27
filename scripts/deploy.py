
from brownie import ArbitrageTrader, accounts, config
from web3 import Web3

def main():
    account = accounts.add(config['wallets']['from_key'])
    aave_lending_pool_addresses_provider = config['networks'][network.show_active()]['aave_lending_pool_addresses_provider']

    arbitrage_trader = ArbitrageTrader.deploy(
        aave_lending_pool_addresses_provider,
        {'from': account},
        publish_source=config['networks'][network.show_active()].get('verify', False)
    )

    print(f"ArbitrageTrader deployed at: {arbitrage_trader.address}")

    # Add DEX routers
    for dex_name, router_address in config['dex_routers'].items():
        arbitrage_trader.addDexRouter(dex_name, router_address, {'from': account})
        print(f"Added {dex_name} router: {router_address}")

    # Set price feeds
    for token_address, price_feed_address in config['price_feeds'].items():
        arbitrage_trader.setPriceFeed(token_address, price_feed_address, {'from': account})
        print(f"Set price feed for token {token_address}: {price_feed_address}")

    # Set min profit threshold and max loss limit
    arbitrage_trader.setMinProfitThreshold(Web3.toWei(0.01, 'ether'), {'from': account})
    arbitrage_trader.setMaxLossLimit(Web3.toWei(0.5, 'ether'), {'from': account})

    print("Deployment and initial setup complete.")
