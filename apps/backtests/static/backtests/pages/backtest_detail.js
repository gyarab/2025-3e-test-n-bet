import BacktestDetail from "../components/backtest_detail";

document.addEventListener("DOMContentLoaded", () => {
    initBacktestDetail();
});

function initBacktestDetail() {
    const backtestData = JSON.parse(document.getElementById('backtest-data').textContent);

    if (!backtestData || !Array.isArray(backtestData)) {
        console.error("Invalid or missing strategies data");
        return;
    }

    const root = document.getElementById("backtest-detail");

    const backtestDetail = BacktestDetail(root, backtestData);
}