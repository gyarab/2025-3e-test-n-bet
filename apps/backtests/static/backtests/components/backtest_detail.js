import BacktestGraph from "../components/backtest_graph.js";

export default class BacktestDetail {
    constructor(root, backtestData) {
        this.wrapper = root;
        this.backtestData = backtestData;

        this.parseData(backtestData);
        this.init();
    }

    init() {
        this.setupTradesToggle();
        this.generateGraph(this.wrapper.querySelector("#chart"));
    }

    parseData(backtestData) {
        this.token = backtestData.asset.name;
        this.token_id = backtestData.asset.id;
        this.timeframe = backtestData.timeframe;
        this.start_date = backtestData.start_date;
        this.end_date = backtestData.end_date;
        this.trades = backtestData.trades;
        this.candles_amount = backtestData.candles_amount;
    }

    generateGraph(root) {
        if (root) {
            this.graph = new BacktestGraph(root, this.token_id, this.timeframe, this.candles_amount, this.start_date, this.end_date, this.trades);
        }
    }

    setupTradesToggle() {
        const trades_bar = this.wrapper.querySelector(".trades-bar");
        const toggleText = trades_bar.querySelector("span.text-sm");

        const trades_table = this.wrapper.querySelector(".trades-table");
        const trades_container = trades_table.querySelector(".trades-container");

        if (!trades_bar || !trades_table || !trades_container || !toggleText) {
            console.error("Trades toggle elements not found");
            return;
        }

        const toggleExpand = (e) => {
            e.stopPropagation();
            e.preventDefault();

            const isHidden = trades_container.classList.contains("hidden");
            toggleText.textContent = isHidden ? "Open" : "Close";

            // Animate settings section
            if (trades_container.classList.contains("max-h-0")) {
                // Expanding
                trades_container.classList.remove("max-h-0", "opacity-0");
                trades_container.classList.add("max-h-100", "opacity-100", "mt-6");
                trades_container.style.overflowY = "hidden";

                // Adding overflow auto after transition
                trades_container.addEventListener("transitionend", function handler() {
                    trades_container.style.overflowY = "auto";
                    trades_container.removeEventListener("transitionend", handler);
                });
            } else {
                // Collapsing
                trades_container.classList.remove("max-h-100", "opacity-100", "mt-6");
                trades_container.classList.add("max-h-0", "opacity-0");
                trades_container.style.overflowY = "hidden";
            }
        };

        trades_bar.addEventListener("click", toggleExpand);
    }
}