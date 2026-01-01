export function backtestResultsTableTemplate(initialBalance, finalBalance, profitLoss, token, timeframe, totalTrades, totalWins, totalLosses, trades) {
    return `
        <div class="bg-white rounded-2xl shadow p-5">
            <h2 class="text-lg font-semibold mb-4">Backtest Result</h2>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                <div class="bg-gray-50 p-3 rounded-lg shadow-sm text-center">
                    <div class="text-gray-500 text-sm">Initial Balance</div>
                    <div class="text-lg font-medium">$<span id="initial-balance">${initialBalance}</span></div>
                </div>
                <div class="bg-gray-50 p-3 rounded-lg shadow-sm text-center">
                    <div class="text-gray-500 text-sm">Final Balance</div>
                    <div class="text-lg font-medium">$<span id="final-balance">${finalBalance}</span></div>
                </div>
                <div class="bg-gray-50 p-3 rounded-lg shadow-sm text-center">
                    <div class="text-gray-500 text-sm">Profit / Loss</div>
                    <div class="text-lg font-medium text-green-600" id="profit-loss">${profitLoss}</div>
                </div>
                <div class="bg-gray-50 p-3 rounded-lg shadow-sm text-center">
                    <div class="text-gray-500 text-sm">Token</div>
                    <div class="text-lg font-medium" id="backtest-token">${token}</div>
                </div>
                <div class="bg-gray-50 p-3 rounded-lg shadow-sm text-center">
                    <div class="text-gray-500 text-sm">Timeframe</div>
                    <div class="text-lg font-medium" id="backtest-timeframe">${timeframe}</div>
                </div>
                <div class="bg-gray-50 p-3 rounded-lg shadow-sm text-center">
                    <div class="text-gray-500 text-sm">Total Trades</div>
                    <div class="text-lg font-medium" id="total-trades">${totalTrades}</div>
                </div>
                <div class="bg-gray-50 p-3 rounded-lg shadow-sm text-center">
                    <div class="text-gray-500 text-sm">Wins</div>
                    <div class="text-lg font-medium text-green-600" id="total-wins">${totalWins}</div>
                </div>
                <div class="bg-gray-50 p-3 rounded-lg shadow-sm text-center">
                    <div class="text-gray-500 text-sm">Losses</div>
                    <div class="text-lg font-medium text-red-500" id="total-losses">${totalLosses}</div>
                </div>
            </div>
        </div>
    `;
}
