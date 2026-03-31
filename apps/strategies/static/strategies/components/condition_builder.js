import IndicatorSelector from './indicator_selector.js';

class ConditionBuilder {
    constructor(root, indicatorsData) {
        this.wrapper = root;
        this.indicatorsData = indicatorsData; 

        this.conditions = [];

        this.buildUI();
        this.bindEvents();

        this.defaultTakeProfitPct = 5;
        this.defaultStopLossPct = 2.5;
        this.defaultPositionSizePct = 1;
    }

    buildUI() {
        this.wrapper.innerHTML = `
            <div class="condition-controls">
                <button type="button" class="add-condition-btn bg-teal-500 hover:bg-teal-600 text-white font-semibold px-4 py-2 rounded transition">
                    Add Condition
                </button>
            </div>
            <div class="grid condition-list xl:grid-cols-2 md:grid-cols-1 sm:grid-cols-1 gap-4"></div>
        `;

        this.addBtn = this.wrapper.querySelector(".add-condition-btn");
        this.conditionList = this.wrapper.querySelector(".condition-list");
        this.conditionControls = this.wrapper.querySelector(".condition-controls");
    }

    // Event bindings
    bindEvents() {
        this.addBtn.addEventListener("click", () => this.addCondition());
    }

    createConditionCard(name) {
        const tpl = document.getElementById("condition-card-template");
        const node = tpl.content.cloneNode(true);

        const card = node.querySelector(".condition-card");
        card.querySelector(".card-title").textContent = name;

        return card;
    }

    // Add a new condition card
    addCondition() {   
        const cardName = `Condition ${this.conditions.length + 1}`;
        const card = this.createConditionCard(cardName);
        this.setupRiskModel(card);

        this.conditionList.appendChild(card);

        // Trigger animation
        requestAnimationFrame(() => {
            card.classList.remove("opacity-0", "scale-90");
            card.classList.add("opacity-100", "scale-100");
        });

        const indicatorRoot = card.querySelector('[data-role="indicator-selector"]');
        const indicatorSelector = new IndicatorSelector(indicatorRoot, this.indicatorsData);
        this.conditions.push({ card, indicatorSelector });

        const removeBtn = card.querySelector(`[data-role="remove-btn"]`);
        removeBtn.addEventListener("click", () => this.removeCondition(card));

        this.toggleConditionControls();
    }

    setupRiskModelExpanding(card) {
        const long_signal = card.querySelector(".long-signal");
        const short_signal = card.querySelector(".short-signal");

        function setupOpenClose(container) {
            const expandIcon = container.querySelector(".arrow");
            const settings = container.querySelector(".risk-model-content");

            const toggleExpand = (e) => {
                e.stopPropagation();
                e.preventDefault();

                expandIcon.classList.toggle("rotate-180");
                expandIcon.classList.toggle("text-teal-900");

                // Animate settings section
                if (settings.classList.contains("max-h-0")) {
                    // Expanding
                    settings.classList.remove("max-h-0", "opacity-0");
                    settings.classList.add("max-h-100", "opacity-100", "mt-3");
                    settings.style.overflowY = "hidden";

                    // Adding overflow auto after transition
                    settings.addEventListener("transitionend", function handler() {
                        settings.style.overflowY = "auto";
                        settings.removeEventListener("transitionend", handler);
                    });
                } else {
                    // Collapsing
                    settings.classList.remove("max-h-100", "opacity-100", "mt-3");
                    settings.classList.add("max-h-0", "opacity-0");
                    settings.style.overflowY = "hidden";
                }
            };

            expandIcon.addEventListener("click", toggleExpand);
            container.querySelector("label").addEventListener("click", toggleExpand);
        }

        setupOpenClose(long_signal);
        setupOpenClose(short_signal);
    }

    // Set up risk model toggles for a condition card (hide/show % input based on type)
    setupRiskModel(card) {
        const stopLossElements = card.querySelectorAll('[data-role="stop-loss"]');
        const takeProfitElements = card.querySelectorAll('[data-role="take-profit"]');
        const positionSizeElements = card.querySelectorAll('[data-role="position-size"]');

        // Helper function to attach toggle behavior
        function setupToggle(container) {
            const selectEl = container.querySelector('select');
            const inputEl = container.querySelector('input');

            inputEl.parentElement.style.display = selectEl.value === 'relative' ? 'none' : 'block';

            selectEl.addEventListener('change', () => {
                inputEl.parentElement.style.display = selectEl.value === 'relative' ? 'none' : 'block';
            });
        }

        stopLossElements.forEach(setupToggle);
        takeProfitElements.forEach(setupToggle);
        positionSizeElements.forEach(setupToggle);

        this.setupRiskModelExpanding(card);
    }

    // Remove a condition card
    removeCondition(card) {
        const index = this.conditions.findIndex(
            c => c.card === card
        );

        if (index === -1) return;

        card.classList.remove("opacity-100", "scale-100");
        card.classList.add("opacity-0", "scale-90");

        card.addEventListener("transitionend",() => {
            card.remove();
            this.conditions.splice(index, 1);
            this.renumberConditions();
            this.toggleConditionControls();
        }, { once: true });     
    }

    // Toggle visibility of condition controls based on conditions count
    toggleConditionControls() {
        if (this.conditions.length === 0) {
            this.conditionControls.classList.remove("mb-4");
        }
        else {
            this.conditionControls.classList.add("mb-4");
        }
    }

    // Renumber condition cards after removal
    renumberConditions() {
        this.conditions.forEach((c, i) => {
            c.card.querySelector("span").textContent = `Condition ${i + 1}`;
        });
    }   

    // Clear all conditions
    clear() {
        this.conditions.forEach(({ card }) => card.remove());
        this.conditions = [];
        this.toggleConditionControls();
    }

    // Get action (buy/sell) signal model data for a condition
    getActionData(card) {
        const longSignalEl = card.querySelector(".long-signal");
        const shortSignalEl = card.querySelector(".short-signal");

        const extractSettings = (signalEl) => {
            return {
                stop_loss: {
                    type: signalEl.querySelector('[data-role="stop-loss"] select').value,
                    percentage: signalEl.querySelector('[data-role="stop-loss"] input').value || this.defaultStopLossPct
                },
                take_profit: {
                    type: signalEl.querySelector('[data-role="take-profit"] select').value,
                    percentage: signalEl.querySelector('[data-role="take-profit"] input').value || this.defaultTakeProfitPct
                },
                position_size: {
                    type: signalEl.querySelector('[data-role="position-size"] select').value,
                    percentage: signalEl.querySelector('[data-role="position-size"] input').value || this.defaultPositionSizePct
                }
            }
        };
        
        const buy_settings = extractSettings(longSignalEl);
        const short_settings = extractSettings(shortSignalEl);

        console.log("Buy settings:", buy_settings);
        console.log("Short settings:", short_settings);

        return {
            buy_signal: buy_settings ? buy_settings : null,
            short_signal: short_settings ? short_settings : null,
        };
    }

    // Get all conditions data in serializable format
    getConditionsData() {
        const conditionsArray = [];

        this.conditions.map(({ card, indicatorSelector }) => {
            if (indicatorSelector.getSelectedIndicatorsData().length === 0) {
                return;
            }
            conditionsArray.push({
                signal_models: {
                    indicators: indicatorSelector.getSelectedIndicatorsData(),
                    prediction_models: [] // Future feature
                },
                action: this.getActionData(card),
            });  
        });

        return conditionsArray;
    }
}

export default ConditionBuilder;
