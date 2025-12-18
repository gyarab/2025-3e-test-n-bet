export function indicatorCardTemplate(indicatorName) {
    return `
        <div class="p-4 bg-white rounded-2xl shadow-md hover:shadow-lg transition-shadow duration-200 cursor-pointer border border-gray-100">
            <div class="card-header flex justify-between items-center">
                <div class="flex items-center space-x-3">
                    <span class="flex items-center justify-center px-4 py-2 bg-teal-100 text-teal-700 font-semibold rounded-full capitalize tracking-wide">
                        ${indicatorName}
                    </span>
                    <svg class="arrow w-4 h-4 left text-teal-700 transition-transform duration-200" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="6 9 12 15 18 9" />
                    </svg>
                </div>
                <button type="button" class="remove-card bg-gray-500 hover:bg-gray-600 rounded-full w-6 h-6 flex items-center justify-center shadow-md transition-colors duration-200">
                    <svg class="w-3.5 h-3.5 text-white" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <line x1="15" y1="5" x2="5" y2="15" />
                        <line x1="5" y1="5" x2="15" y2="15" />
                    </svg>
                </button>
            </div>
            <div class="settings overflow-y-auto max-h-0 opacity-0 transition-all duration-200 ease-in-out">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1 mt-3">Condition</label>
                    <select class="w-full border border-gray-300 rounded-lg p-2 focus:ring-2 focus:ring-teal-400 focus:border-teal-400 transition duration-150 mb-3">
                        <option value="greater_than">Greater Than</option>
                        <option value="less_than">Less Than</option>
                    </select>
                    <input type="number" class="w-full border border-gray-300 rounded-lg p-2 focus:ring-2 focus:ring-teal-400 focus:border-teal-400 transition duration-150" placeholder="Value" required>
                </div> 
                <hr class="my-3">
                <div class="parameters space-y-3">
                    <!-- Parameter settings -->
                </div>              
            </div>
        </div>
    `;
}
