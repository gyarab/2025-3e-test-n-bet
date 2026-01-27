import Indicator from "./indicator.js";

class StrategyCard {
    constructor(root, strategy) {
        this.root = root;
        this.strategy = strategy;

        if(!this.strategy || !this.root) {
            console.error("StrategyCard: Missing strategy data or root element.");
            return;
        }
        
        this.id = strategy.id;
        console.log(this.strategy); 

        if (!Array.isArray(this.strategy.parameters)) {
            this.strategy.parameters = [];
        }

        this.buildUI();
        this.setup();
        
    }

    buildUI() { 
        const tpl = document.getElementById("strategy-card-template");
        const node = tpl.content.cloneNode(true);

        const card = node.querySelector(".strategy-card");

        this.setBasicValues(card);
        this.setBaseStrategy(card);
        
        const paramsContainer = card.querySelector(".strategy-parameters");
        const noParamsText = card.querySelector(".no-parameters");
        console.log(paramsContainer);

        // If there are parameters...
        if (this.strategy.parameters && Object.keys(this.strategy.parameters).length > 0) {
            const paramTemplate = document.getElementById("condition-for-strategy-template");
            
            this.strategy.parameters.forEach(param => {
                const paramNode = paramTemplate.content.cloneNode(true);
                paramsContainer.appendChild(paramNode);

                const indicatorTemplate = document.getElementById("indicator-for-strategy-template");
                console.log(indicatorTemplate);

                const indicatorsContainer = paramNode.querySelector(".indicator-items-list");
                const noIndicatorsText = paramNode.querySelector(".no-indicators");
                const paramContainer = paramNode.querySelector(".param-container");

                console.log(indicatorsContainer)
                console.log(noIndicatorsText)
                console.log(paramContainer)
                

                if (param.signal_models && param.signal_models.indicators && param.signal_models.indicators.length > 0) {
                    param.signal_models.indicators.forEach(indicator => {
                        
                        console.log(indicatorTemplate)
                        const indicatorNode = indicatorTemplate.content.cloneNode(true);

                        console.log(indicatorNode);

                        const indicatorTitleSpan = indicatorNode.querySelector(".indicator-title");
                        indicatorTitleSpan.textContent = indicator.name;

                        const indicatorParamsSpan = indicatorNode.querySelector(".indicator-parameters");
                        const indicatorEntity = Indicator.fromJSON(indicator);
                        console.log(indicatorEntity.getIndicatorData());
                    });
                    noIndicatorsText.classList.add("hidden");
                }
                else {
                    indicatorsContainer.classList.add("hidden");
                    noIndicatorsText.classList.remove("hidden");
                }

            });
            noParamsText.classList.add("hidden");
        }
        else {
            paramsContainer.classList.add("hidden");
            noParamsText.classList.remove("hidden");
        }

        this.root.appendChild(card);
    }   

    setBasicValues(card) {
        card.querySelector(".strategy-title").textContent = this.strategy.name;
        card.dataset.value = JSON.stringify(this.id);
    }

    setBaseStrategy(card) {
        const baseStrategyTitle = card.querySelector(".base-strategy-title");
        const baseStrategyElem = card.querySelector(".base-strategy");

        if (this.strategy.base_strategy_id) {
            baseStrategyTitle.textContent = this.strategy.base_strategy_name;
        }
        else {
            baseStrategyElem.classList.add("hidden");
        }
    }

    setup() {
        const deleteButton = document.querySelectorAll('button.delete-button');

        const csrf_token = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');

        deleteButton.forEach(button => {
            button.addEventListener('click', async (e) => {
                const strategyId = e.target.id;
                if (confirm('Are you sure you want to delete this strategy?')) {
                    console.log('Deleting strategy with ID:', strategyId);
                    try {
                        const response = await fetch(`/api/strategies/delete`, {
                            method: 'DELETE',
                            headers: {
                                'X-CSRFToken': csrf_token,
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({ strategy_id: strategyId }),
                        });
                        if (response.ok) {
                            e.target.closest('div.strategy-card').remove();
                        } else {
                            alert('Failed to delete strategy.');
                        }
                    } catch (error) {
                        console.error('Error:', error);
                        alert('An error occurred while deleting the strategy.');
                    }
                }
            });
        });
    }

    save() {

    }
}

export default StrategyCard;