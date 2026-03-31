import ConditionBuilder from './condition_builder.js';

class StrategyBuilder {
    constructor(root, indicatorsData) {
        this.root = root;
        this.wrapper = this.root.querySelector('.strategy-builder-wrapper');
        this.conditionBuilder = this.initConditionBuilder(
            this.wrapper.querySelector('.condition-builder-root'),
            indicatorsData
        );

        this.saveForm = this.wrapper.querySelector('form');
        this.strategyNameInput = this.wrapper.querySelector('.strategy-name-input');
        this.hideBtn = this.wrapper.querySelector('.hide-strategy-builder-btn');
        this.createBtn = document.getElementById('create-strategy-button');
        this.strategyNameInput = this.wrapper.querySelector('.strategy-name-input');

        this.setupEventListeners();
        this.init();
    }
    
    // Initial setup of the StrategyBuilder component
    init() {
        this.wrapper.classList.add('hidden');
        this.root.querySelector('.create-strategy-btn').addEventListener('click', () => {
            this.show();
        });
    }

    // Setup all event listeners
    setupEventListeners() {
        this.setupCreateButton();
        this.setupHideButton();
        this.setupSaveForm();
    }

    // Handle create button click
    setupCreateButton() {
        this.createBtn?.addEventListener('click', () => {
            this.show();
        });
    }

    // Handle hide button click
    setupHideButton() {
        this.hideBtn?.addEventListener('click', () => {
            this.conditionBuilder.clear();
            this.hide();
            this.strategyNameInput.value = '';
        });
    }

    // Handle form submission to save strategy
    setupSaveForm() {
        this.saveForm?.addEventListener('submit', async (e) => {
            e.preventDefault();

            if (!this.checkIfCanSave()) {
                alert('Please provide a strategy name, at least one condition, and select indicators for the conditions.');
                return;
            }

            if (!await this.checkName()) {
                alert('Strategy name already exists. Please choose a different name.');
                return;
            }

            const name = this.strategyNameInput.value;
            const parameters = this.conditionBuilder.getConditionsData();
            const csrftoken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');

            try {
                const response = await fetch('/api/strategies/save/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken
                    },
                    body: JSON.stringify({
                        name: name,
                        parameters: parameters,
                        base_strategy_id: null
                    })
                });

                const result = await response.json();

                if (response.ok) {
                    alert('Strategy saved successfully!');
                    this.onSavedSuccess();
                    this.hide();
                } else {
                    alert('Error: ' + result.message);
                }
            } catch (error) {
                console.error('Error sending request:', error);
                alert('Failed to connect to the server.');
            }
        });
    }

    // Check if the strategy can be saved (has name, conditions, and selected indicators)
    checkIfCanSave() {
        const hasName = this.strategyNameInput.value.trim() !== '';
        const hasConditions = this.conditionBuilder.conditions.length > 0;
        let hasSelectedIndicator = false;

        this.conditionBuilder.conditions.map(({ card, indicatorSelector }) => {
            if (indicatorSelector.getSelectedIndicatorsData().length > 0) {
                hasSelectedIndicator = true;
                return;
            }
        });

        if (hasName && hasConditions && hasSelectedIndicator) {
            return true;
        }
        return false;
    }

    // Check if the strategy name is unique by fetching existing strategies and comparing names
    async checkName() {
        const name = this.strategyNameInput.value.trim();
        
        try {
            const response = await fetch("/api/strategies/get/", {
                method: "GET",
                credentials: "same-origin",
                headers: {
                    "Accept": "application/json",
                },
            });

            const data = response.json();

            if (!response.ok) {
                console.error(data.message || "Failed to fetch strategies");
                return false;
            }

            const strategies = data.strategies || [];

            console.log("Existing strategies:", strategies);

            return !strategies.some(s => s.name === name);

        } catch (error) {
            console.error("Error fetching strategies:", error);
            return false;
        }
    }

    // Initialize the ConditionBuilder component
    initConditionBuilder(conditionBuilderRoot, indicatorsData) {
        return new ConditionBuilder(
            conditionBuilderRoot,
            indicatorsData
        );
    }

    // Hide the StrategyBuilder component
    hide() {
        this.wrapper.classList.add('hidden');
    }

    // Show the StrategyBuilder component
    show() {
        this.wrapper.classList.remove('hidden');
    }

    // Triggered after successful save. Dispatches a global event to update the strategy list.
    onSavedSuccess() {
        const event = new CustomEvent("strategy:added", { detail: null });
        window.dispatchEvent(event);
        this.reset();
    }

    reset() {
        this.conditionBuilder.clear();
        this.hide();
        this.strategyNameInput.value = '';
    }
}

export default StrategyBuilder;