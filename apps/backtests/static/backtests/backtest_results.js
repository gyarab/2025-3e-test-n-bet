import { backtestResultsTableTemplate } from "./templates/backtest_results_table_template.js";

export default class BacktestResults {
    constructor(selector) {
        this.wrapper = document.querySelector(selector);
        
        if (!this.wrapper) {
            throw new Error(`BacktestResults: selector "${selector}" not found`);
        }

        this.backtestData = null;
        this.reset();
    }

    // Creates the HTML elements
    buildUI(backtestData) {
        this.backtestData = backtestData;

        const results = backtestResultsTableTemplate(
            this.backtestData.initial_balance,
            this.backtestData.final_balance,
            this.backtestData.profit_loss,
            this.backtestData.token,
            this.backtestData.timeframe,
            this.backtestData.total_trades,
            this.backtestData.total_wins,
            this.backtestData.total_losses,
            this.backtestData.not_closed_trades,
            this.backtestData.trades
        );
        this.wrapper.innerHTML = results;
        this.wrapper.classList.remove("hidden");
    }
    
    reset() {
        this.wrapper.innerHTML = "";
        this.wrapper.classList.add("hidden");
    }
}