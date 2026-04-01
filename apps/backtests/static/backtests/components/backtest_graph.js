export default class BacktestGraph {
    constructor(root, token_id, timeframe, candleAmount, start_date, end_date, trades) {
        if (!root) {
            throw new Error("BacktestGraph: Root element not provided");
        }

        this.wrapper = root;
        this.token_id = token_id;
        this.timeframe = timeframe;
        this.candleAmount = candleAmount;
        this.start_date = start_date;
        this.end_date = end_date;
        this.trades = trades;

        console.log("Initializing BacktestGraph with:", {
            token_id,
            timeframe,
            candleAmount,
            start_date,
            end_date,
            trades
        });

        this.getCandles(token_id, timeframe, candleAmount, start_date)
            .then(() => this.init())
            .catch(error => console.error("Error fetching candles:", error));
    }
    
    init() {
        console.log("Initializing chart with candles:", this.candles);
        const chart = window.LightweightCharts.createChart(this.wrapper, {
            width: this.wrapper.clientWidth || 1000,
            height: this.wrapper.clientHeight || 500,
        });

        const candlestickSeries = chart.addCandlestickSeries();

        // Map API candles to LightweightCharts format
        const formattedCandles = this.candles.map(c => ({
            time: Math.floor(new Date(c.open_time).getTime() / 1000),
            open: c.open,
            high: c.high,
            low: c.low,
            close: c.close,
        }));

        candlestickSeries.setData(formattedCandles);
        
        // Send trades from backtest detail page to the graph 
        const markers = this.trades.map(t => ({
            time: t.entry_time.slice(0,10),
            position: t.trade_type === "buy" ? "belowBar" : "aboveBar",
            color: t.trade_type === "buy" ? "green" : "red",
            shape: t.trade_type === "buy" ? "arrowUp" : "arrowDown",
            text: t.trade_type
        }));

        candles.setMarkers(markers);
    }

    getCandles() {
        return fetch("/api/market/get-candles/" + this.token_id, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": this._getCsrfToken()
            },
            body: JSON.stringify({
                interval: this.interval,
                candle_amount: this.candleAmount,
                start_date: this.start_date
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status !== "success") {
                throw new Error(data.message);
            }
            this.candles = data.candles;
        });
    }

    _getCsrfToken() {
        return document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');
    }
}