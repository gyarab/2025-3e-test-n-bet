import ConditionBuilder from '../components/condition_builder.js';

document.addEventListener("DOMContentLoaded", () => {
    const conditionBuilderRoot = document.getElementById('condition-builder-root');
    if (!conditionBuilderRoot) return;

    let indicatorsData = [];

    fetch('/api/strategies/indicators/')
        .then(res => {
            if (res.status === 400) {
                window.location.href = '/backtests/';
                return;
            }
            return res.json();
        })
        .then(data => {
            indicatorsData = data.indicators;

            const conditionBuilder = new ConditionBuilder(
                    conditionBuilderRoot,
                    indicatorsData
                );

            document.getElementById('hide-strategy-builder')
                ?.addEventListener('click', () => {
                    conditionBuilder.clear();
                });
        });
});