import BacktestGraph from "../components/backtest_graph.js";

export default class BacktestDetail {
    constructor(root, backtestData) {
        this.wrapper = root;
        this.backtestData = backtestData;

        this.parseData(backtestData);
        this.init();
    }

    init() {
        this.generateGraph(this.wrapper.querySelector("#chart"));
    }

    parseData(backtestData) {
        this.token = backtestData.asset.name;
        this.timeframe = backtestData.timeframe;
        this.start_date = backtestData.start_date;
        this.end_date = backtestData.end_date;
        this.trades = backtestData.trades;
        this.candles_amount = backtestData.candles_amount;
    }

    generateGraph(root) {
        if (root) {
            this.graph = new BacktestGraph(root, this.token, this.timeframe, this.candles_amount);
        }
    }
}