export function conditionCardTemplate(cardName, index) {
    // cardName is like "Condition 1", "Condition 2", etc.
    // index is the unique index for IDs

    const indicatorId = `indicator-selector-${index}`;
    const removeId = `remove-condition-btn-${index}`;
    const signalId = `signal-select-${index}`;

    return `
        <div class="flex justify-between items-center mb-3">
            <span class="font-semibold text-gray-700">${cardName}</span>
            <button type="button" id="${removeId}" class="remove-card bg-gray-500 hover:bg-gray-600 rounded-full w-6 h-6 flex items-center justify-center shadow-md transition-colors duration-200">
                <svg class="w-3.5 h-3.5 text-white" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="15" y1="5" x2="5" y2="15" />
                    <line x1="5" y1="5" x2="15" y2="15" />
                </svg>
            </button>
        </div>

        <div class="indicator-selector-container" id="${indicatorId}"></div>

        <div class="bg-gray-50 border border-gray-200 rounded-lg p-4 space-y-4">
            <div>
                <label class="block text-gray-700 font-semibold mb-1" for="${signalId}">Signal:</label>
                <select id="${signalId}" class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-teal-400">
                    <option value="LONG">LONG</option>
                    <option value="SHORT">SHORT</option>
                </select>
            </div>

            <div class="mt-3 grid grid-cols-2 gap-3">
                <div class="flex flex-col space-y-2 stop-loss-pair border border-gray-200 rounded px-3 py-2 bg-transparent shadow-sm">   
                    <div>
                        <label class="block text-gray-700 font-semibold mb-1" for="stop-loss-type-${index}">Stop Loss Type:</label>
                        <select id="stop-loss-type-${index}" class="w-full border border-gray-300 rounded px-2 py-1">
                            <option value="fixed">Fixed</option>
                            <option value="relative">Relative</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-gray-700 font-semibold mb-1" for="stop-loss-pct-${index}">Stop Loss %:</label>
                        <input type="number" step="0.01" id="stop-loss-pct-${index}" class="w-full border border-gray-300 rounded px-2 py-1" placeholder="e.g. 2.5" required>
                    </div>
                </div>
                <div class="flex flex-col space-y-2 take-profit-pair border border-gray-200 rounded px-3 py-2 bg-transparent shadow-sm">
                    <div>
                        <label class="block text-gray-700 font-semibold mb-1" for="take-profit-type-${index}">Take Profit Type:</label>
                        <select id="take-profit-type-${index}" class="w-full border border-gray-300 rounded px-2 py-1">
                            <option value="fixed">Fixed</option>
                            <option value="relative">Relative</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-gray-700 font-semibold mb-1" for="take-profit-pct-${index}">Take Profit %:</label>
                        <input type="number" step="0.01" id="take-profit-pct-${index}" class="w-full border border-gray-300 rounded px-2 py-1" placeholder="e.g. 5" required>
                    </div>
                </div>
                <div class="flex grid col-span-2 grid-cols-2 gap-10 position-size-pair border border-gray-200 rounded px-3 py-2 bg-transparent shadow-sm"> 
                    <div>
                        <label class="block text-gray-700 font-semibold mb-1" for="position-size-type-${index}">Position Size Type:</label>
                        <select id="position-size-type-${index}" class="w-full border border-gray-300 rounded px-2 py-1">
                            <option value="fixed">Fixed</option>
                            <option value="relative">Relative</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-gray-700 font-semibold mb-1" for="position-size-pct-${index}">Position Size %:</label>
                        <input type="number" step="0.01" id="position-size-pct-${index}" class="w-full border border-gray-300 rounded px-2 py-1" placeholder="e.g. 1" required>
                    </div>
                </div>
            </div>
        </div>
    `;
}
