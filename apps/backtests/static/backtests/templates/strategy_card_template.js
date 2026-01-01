export function strategyCardTemplate(strategyName) {
    return `
        <div class="p-4 bg-white rounded-2xl transition-shadow duration-200 cursor-pointer border border-gray-100">
            <div class="card-header flex justify-between items-center">
                <div class="flex items-center space-x-3">
                    <span class="flex items-center justify-center px-4 py-2 bg-teal-100 text-teal-700 font-semibold rounded-full capitalize tracking-wide">
                        ${strategyName}
                    </span>
                </div>
                <button type="button" class="remove-card bg-gray-500 hover:bg-gray-600 rounded-full w-6 h-6 flex items-center justify-center shadow-md transition-colors duration-200">
                    <svg class="w-3.5 h-3.5 text-white" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <line x1="15" y1="5" x2="5" y2="15" />
                        <line x1="5" y1="5" x2="15" y2="15" />
                    </svg>
                </button>
            </div>
        </div>
    `;
}
