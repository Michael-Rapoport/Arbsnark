import "./AdvancedStrategies.sol";

contract ArbitrageTrader {
    AdvancedStrategies public advancedStrategies;

    constructor(address aaveLendingPoolAddressesProvider) {
        advancedStrategies = new AdvancedStrategies(this);
    }

    function executeArbitrageWithMeanReversion(
        address[] memory path,
        string[] memory dexNames,
        uint256 amountIn,
        uint256 minAmountOut
    ) public {
        advancedStrategies.meanReversionStrategy(path[0], path[1]);
    }

    function executeArbitrageWithVolatilityArbitrage(
        address[] memory path,
        string[] memory dexNames,
        uint256 amountIn,
        uint256 minAmountOut
    ) public {
        advancedStrategies.volatilityArbitrage(path[0], path[1]);
    }
}