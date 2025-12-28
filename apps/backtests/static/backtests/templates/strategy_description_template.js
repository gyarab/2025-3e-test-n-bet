export function strategyDescriptionTemplate(strategyName, parameters) {
    // Returns a DOM element representing the strategy description
    const div = document.createElement("div");
    div.className = "strategy-description";

    console.log(parameters[0]);

    parameters = parameters[0] || {};
    
    let signal_models = "";
    

    if (parameters.signal_models?.indicators?.length) {
        parameters.signal_models.indicators.forEach(ind => {
            signal_models += `
                <div class="border border-gray-200 rounded-lg p-2 mb-2 bg-gray-50">
                    <h4 class="font-semibold text-gray-700">${ind.name}</h4>
                    <ul class="ml-4 text-gray-600">
                        ${Object.entries(ind.parameters || {})
                            .map(([key, val]) => `<li>${key}: ${val}</li>`)
                            .join("")}
                    </ul>
                </div>
            `;
        });
    }

    let action_models = "";


    if (parameters.action?.buy_signal) {
        const action = parameters.action.buy_signal;
        action_models += renderSignal(action, "Buy Signal");
    }

    if (parameters.action?.sell_signal) {
        const action = parameters.action.sell_signal;
        action_models += renderSignal(action, "Sell Signal");
    }

    div.innerHTML = `
        <div class="p-4 bg-white rounded-2xl shadow-md transition-shadow duration-200 cursor-pointer border border-gray-100">
            <div class="card-header flex justify-between items-center">
                <h2 class="text-md font-semibold">${strategyName}</h2>
            </div>
            <div class="settings overflow-y-auto h-full mt-4">
                ${signal_models || `<p class="text-gray-400">No signal models available</p>`}
                <hr class="my-2">
                ${action_models || `<p class="text-gray-400">No action models available</p>`}
            </div>
        </div>
    `;

    return div;
}

// Helper function to render a signal's details
function renderSignal(signal, title) {
    if (!signal) return "";
    return `
        <div class="border border-gray-200 rounded-lg p-2 mb-2 bg-white">
            <h4 class="font-semibold text-gray-700">${title}</h4>
            <ul class="ml-4 text-gray-600">
                <li>Stop Loss: ${signal.stop_loss.type} - ${signal.stop_loss.percentage ?? "-"}</li>
                <li>Take Profit: ${signal.take_profit.type} - ${signal.take_profit.percentage ?? "-"}</li>
                <li>Position Size: ${signal.position_size.type} - ${signal.position_size.percentage ?? "-"}</li>
            </ul>
        </div>
    `;
}