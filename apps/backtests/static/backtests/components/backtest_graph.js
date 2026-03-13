export default class BacktestGraph {
    constructor(root, token, timeframe, candleAmount) {
        this.wrapper = root;
        this.token = token;
        this.timeframe = timeframe;
        this.candleAmount = candleAmount;

        this.candles = [];
    }
    
    init() {
        const chart = LightweightCharts.createChart(this.root, {
            width: 1000,
            height: 500
        });

        const candles = chart.addCandlestickSeries();
        candles.setData(this.candles);
        
        // Send trades from backtest detail page to the graph 
        const markers = trades.map(t => ({
            time: t.entry_time.slice(0,10),
            position: t.trade_type === "buy" ? "belowBar" : "aboveBar",
            color: t.trade_type === "buy" ? "green" : "red",
            shape: t.trade_type === "buy" ? "arrowUp" : "arrowDown",
            text: t.trade_type
        }));

        candles.setMarkers(markers);
    }

    getCandles(token, interval = "1h", candleAmount = 100) {

        const response = fetch("/api/get-candles/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": this._getCsrfToken()
            },
            body: JSON.stringify({
                token: token,
                interval: interval,
                candle_amount: candleAmount
            })
        });

        const data = response.json();

        if (data.status !== "success") {
            throw new Error(data.message);
        }

        this.candles = data.candles;
    }

    _getCsrfToken() {
        return document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');
    }
}