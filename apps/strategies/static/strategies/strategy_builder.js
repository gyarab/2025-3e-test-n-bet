import IndicatorSelector from './indicator_selector.js'

document.addEventListener("DOMContentLoaded", () => {
    new IndicatorSelector("#indicator-select", [
        "RSI",
        "SMA",
        "MACD"
    ]);
});
