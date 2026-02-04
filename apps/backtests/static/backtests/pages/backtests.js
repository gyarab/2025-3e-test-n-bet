import BacktestRunner from "../components/backtest_runner.js";

document.addEventListener("DOMContentLoaded", () => {
    initBacktestRunner();
});

function initBacktestRunner() {
    const backtestRunnerRoot = document.getElementById('backtest-runner-root');

    if (!backtestRunnerRoot) {
        console.error("BacktestRunner root element not found");
        return;
    }

    const strategiesData = JSON.parse(document.getElementById('strategies-data').textContent);

    if (!strategiesData || !Array.isArray(strategiesData)) {
        console.error("Invalid or missing strategies data");
        return;
    }

    const backtestRunner = new BacktestRunner(backtestRunnerRoot, strategiesData);
}