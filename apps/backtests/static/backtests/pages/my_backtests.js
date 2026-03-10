import BacktestList from "../components/backtest_list";

document.addEventListener("DOMContentLoaded", () => {
    initBacktestList();
});

function initBacktestList() {
    const backtestsData = JSON.parse(document.getElementById('backtests-data').textContent);

    if (!backtestsData || !Array.isArray(backtestsData)) {
        console.error("Invalid or missing strategies data");
        return;
    }

    const backtestList = BacktestList();
}