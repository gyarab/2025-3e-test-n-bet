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
    

    hide() {
        this.wrapper.classList.add('hidden');
    }


    show() {
        this.wrapper.classList.remove('hidden');
    }


    init() {
        this.wrapper.classList.add('hidden');
        this.root.querySelector('.create-strategy-btn').addEventListener('click', () => {
            this.show();
        });
    }


    initConditionBuilder(conditionBuilderRoot, indicatorsData) {
        return new ConditionBuilder(
            conditionBuilderRoot,
            indicatorsData
        );
    }


    setupEventListeners() {
        this.setupCreateButton();
        this.setupHideButton();
        this.setupSaveForm();
    }


    setupCreateButton() {
        this.createBtn?.addEventListener('click', () => {
            this.show();
        });
    }


    setupHideButton() {
        this.hideBtn?.addEventListener('click', () => {
            this.conditionBuilder.clear();
            this.hide();
            strategyNameInput.value = '';
        });
    }


    setupSaveForm() {
        this.saveForm?.addEventListener('submit', async (e) => {
            e.preventDefault();

            const name = this.strategyNameInput.value;
            
            const parameters = this.conditionBuilder.getConditionsData();
            console.log('Collected Parameters:', parameters);

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
}

export default StrategyBuilder;