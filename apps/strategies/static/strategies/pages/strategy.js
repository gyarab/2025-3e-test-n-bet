import StrategyBuilder from '../components/strategy_builder.js';
import StrategyList from '../components/strategy_list.js';

document.addEventListener("DOMContentLoaded", () => {
    initStrategyBuilder();
    initStrategyList();
});

function initStrategyBuilder() {
    const strategyBuilderRoot = document.getElementById('strategy-builder');
    if (!strategyBuilderRoot) return;

    fetch('/api/strategies/indicators/') //TODO: recieve indicators directly from the view, not via fetch
        .then(res => {
            if (res.status === 400) {
                window.location.href = '/backtests/';
                return;
            }
            return res.json();
        })
        .then(data => {
            new StrategyBuilder(strategyBuilderRoot, data.indicators);
        });
}

function initStrategyList() {
    const strategyListRoot = document.getElementById('strategy-list-root');
    if (strategyListRoot) {
        const strategiesData = JSON.parse(document.getElementById('strategies-data').textContent);
        new StrategyList(strategyListRoot, strategiesData);
    }
}

