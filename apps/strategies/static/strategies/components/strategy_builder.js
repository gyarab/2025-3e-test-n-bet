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
            strategyNameInput.value = '';
        });
    }

    // Handle form submission to save strategy
    setupSaveForm() {
        this.saveForm?.addEventListener('submit', async (e) => {
            e.preventDefault();

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

    // Triggered after successful save. Dispatches a global event.
    onSavedSuccess() {
        const event = new CustomEvent("strategy:added", { detail: null });
        window.dispatchEvent(event);
    }
}

export default StrategyBuilder;