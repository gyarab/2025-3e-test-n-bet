import BacktestDetail from "../components/backtest_detail.js";

document.addEventListener("DOMContentLoaded", () => {
    initBacktestDetail();
});

function initBacktestDetail() {
    const backtestData = JSON.parse(document.getElementById('backtest-data').textContent);

    console.log("Received backtest data:", backtestData);

    if (!backtestData) {
        console.error("Invalid or missing strategies data");
        return;
    }

    const root = document.getElementById("backtest-detail");

    const backtestDetail = new BacktestDetail(root, backtestData);
}