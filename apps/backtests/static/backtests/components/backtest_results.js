export default class BacktestResults {
    constructor(root) {
        if (!root) {
            throw new Error("BacktestResults: Root element not provided");
        }

        this.wrapper = root;

        this.backtestData = null;
        this.reset();
    }

    // Creates the HTML elements
    buildUI(backtestData) {
        this.backtestData = backtestData;

        const cardTemplate = document.getElementById("backtest-results-card-template");
        const node = cardTemplate.content.cloneNode(true);
        const card = node.querySelector(".backtest-results");

        card.querySelector(".initial-balance").textContent = `$${this.backtestData.initial_balance}`;
        card.querySelector(".final-balance").textContent = `$${Math.round(Number(this.backtestData.final_balance))}`;
        card.querySelector(".profit-loss").textContent = `$${Math.round(Number(this.backtestData.profit_loss))}`;
        card.querySelector(".total-trades").textContent = this.backtestData.total_trades;
        card.querySelector(".total-wins").textContent = this.backtestData.total_wins;
        card.querySelector(".total-losses").textContent = this.backtestData.total_losses;
        card.querySelector(".total-not-closed").textContent = this.backtestData.not_closed_trades;
        card.querySelector(".backtest-token").textContent = this.backtestData.token;
        card.querySelector(".backtest-timeframe").textContent = this.backtestData.timeframe;

        this.wrapper.appendChild(card);
        this.wrapper.classList.remove("hidden");
    }
    
    reset() {
        this.wrapper.innerHTML = "";
        this.wrapper.classList.add("hidden");
    }
}