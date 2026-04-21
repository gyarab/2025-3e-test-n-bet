import BacktestDetail from "../components/backtest_detail.js";

document.addEventListener("DOMContentLoaded", () => {
    initBacktestDetail();
});

function initBacktestDetail() {
    const backtestData = JSON.parse(document.getElementById('backtest-data').textContent);

    if (!backtestData) {
        console.error("Invalid or missing strategies data");
        return;
    }

    console.log("Backtest data:", backtestData);

    const root = document.getElementById("backtest-detail");

    if (!root) {
        console.error("BacktestDetail root element not found");
        return;
    }

    const backtestDetail = new BacktestDetail(root, backtestData);
}


            