import StrategyBuilder from '../components/strategy_builder.js';


document.addEventListener("DOMContentLoaded", () => {
    const strategyBuilderRoot = document.getElementById('strategy-builder');
    if (!strategyBuilderRoot) return;

    fetch('/api/strategies/indicators/')
        .then(res => {
            if (res.status === 400) {
                window.location.href = '/backtests/';
                return;
            }
            return res.json();
        })
        .then(data => {
            const strategyBuilder = new StrategyBuilder(strategyBuilderRoot, data.indicators);
        });
});

