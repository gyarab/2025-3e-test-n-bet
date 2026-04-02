import { createChart, CandlestickSeries, createSeriesMarkers } from "https://esm.sh/lightweight-charts";
// Docs: https://tradingview.github.io/lightweight-charts/docs/api

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
    
    // Initialize the chart and plot candles
    init() {
        console.log("Initializing chart with candles:", this.candles);
        this.chart = createChart(this.wrapper, {
            width: this.wrapper.clientWidth,
            height: this.wrapper.clientHeight,
        });

        console.log(this.chart);
        
        this.candlestickSeries = this.chart.addSeries(CandlestickSeries);   

        // Map API candles to LightweightCharts format
        const formattedCandles = this.candles.map(c => ({
            time: Math.floor(new Date(c.open_time).getTime() / 1000),
            open: c.open,
            high: c.high,
            low: c.low,
            close: c.close,
        }));

        this.candlestickSeries.setData(formattedCandles); 

        this.setMarkers();
        this.handleResize();
    }

    // Set markers for trades on the chart
    setMarkers() {
        const markers = this.trades.map(t => (
            console.log ("Processing trade for marker:", t.entry_time),{
            time: Math.floor(new Date(t.entry_time).getTime() / 1000),
            position: t.trade_type === '1' ? "belowBar" : "aboveBar",
            color: t.trade_type === '1' ? "green" : "red",
            shape: t.trade_type === '1' ? "arrowUp" : "arrowDown",
            text: t.trade_type
        }));

        this.markers = createSeriesMarkers(this.candlestickSeries, markers);

        const tooltip = document.getElementById("tooltip");

        this.chart.subscribeCrosshairMove(param => {
            if (!param || !param.point || !param.time) {
                tooltip.classList.add("hidden");
                return;
            }

            const trade = this.trades.find(t =>
                Math.floor(new Date(t.entry_time).getTime() / 1000) === param.time
            );

            if (!trade) {
                tooltip.classList.add("hidden");
                return;
            }

            tooltip.classList.remove("hidden");

            tooltip.innerHTML = `
                <div><b>${trade.trade_type === '1' ? 'LONG' : 'SHORT'}</b></div>
                <div>Entry: ${trade.entry_price}</div>
                <div>Exit: ${trade.exit_price || '-'}</div>
                <div>PnL: ${trade.pnl || '-'}</div>
            `;

            tooltip.style.left = param.point.x + "px";
            tooltip.style.top = param.point.y + "px";
        });
    }

    // Fetch candles from the API based on the provided parameters
    getCandles() {
        return fetch("/api/market/get-candles/" + this.token_id, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": this._getCsrfToken()
            },
            body: JSON.stringify({
                interval: this.timeframe,
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

    // Handle chart resizing. 
    // LightweightCharts doesn't automatically resize, so we need to listen 
    // for changes in the container size and update the chart accordingly.
    handleResize() {
        const resize = () => {
            const width = this.wrapper.clientWidth;
            const height = this.wrapper.clientHeight;

            if (!width || !height) return;

            this.chart.applyOptions({
                width,
                height,
            });
        };

        const observer = new ResizeObserver(resize);
        observer.observe(this.wrapper);

        window.addEventListener("resize", resize); // To handle window resize as well
    }

    _getCsrfToken() {
        return document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');
    }
}