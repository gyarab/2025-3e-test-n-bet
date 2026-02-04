import Indicator from "./indicator.js";

class StrategyCard {
    constructor(root, strategy) {
        this.root = root;
        this.strategy = strategy;
        this.card = null;

        if(!this.strategy || !this.root) {
            console.error("StrategyCard: Missing strategy data or root element.");
            return;
        }
        
        this.id = strategy.id;

        if (!Array.isArray(this.strategy.parameters)) {
            this.strategy.parameters = [];
        }

        this.buildUI();
        this.setupEvents(this.card);
    }

    // Build the strategy card UI
    buildUI() { 
        const cardTemplate = document.getElementById("strategy-card-template");
        const node = cardTemplate.content.cloneNode(true);
        this.card = node.querySelector(".strategy-card");

        this.setBasicValues();
        this.setBaseStrategy();
        this.setParameters();
        
        this.root.appendChild(this.card);
    }   

    // Set strategy parameters in the card
    setParameters() {
        const paramsContainer = this.card.querySelector(".strategy-parameters");
        const noParamsText = this.card.querySelector(".no-parameters");

        const paramTemplate = document.getElementById("parameters-for-strategy-template");
        
        if (this.strategy.parameters && Object.keys(this.strategy.parameters).length > 0) {
            this.strategy.parameters.forEach(param => {
                const paramNode = paramTemplate.content.cloneNode(true);

                this.insertIndicators(paramNode, param); // Setting indicators inside the parameter
                this.insertRiskModel(paramNode, param); // Setting risk model inside the parameter
                
                paramsContainer.appendChild(paramNode);
            });
            noParamsText.classList.add("hidden");
        }
        else {
            paramsContainer.classList.add("hidden");
            noParamsText.classList.remove("hidden");
        }
    }

    // Insert indicators associated with a parameter
    insertIndicators(paramNode, param) {
        const indicatorTemplate = document.getElementById("indicator-for-strategy-template");

        const indicatorsContainer = paramNode.querySelector(".indicator-items-list");
        const noIndicatorsText = paramNode.querySelector(".no-indicators");

        if (param.signal_models && param.signal_models.indicators && param.signal_models.indicators.length > 0) {
            param.signal_models.indicators.forEach(indicator => {
                const indicatorNode = indicatorTemplate.content.cloneNode(true);     

                const indicatorTitleSpan = indicatorNode.querySelector(".indicator-title");
                indicatorTitleSpan.textContent = indicator.name;

                const indicatorParamsSpan = indicatorNode.querySelector(".indicator-parameters");
                const indicatorEntity = Indicator.fromJSON(indicator);
                const rawParams = indicatorEntity.getIndicatorData().parameters;
                
                const formattedParams = Object.entries(rawParams).map(([key, value]) => {
                    const readableKey = key.replaceAll("_", " ").split(" ").map(w => w.replace(/^\w/, c => c.toUpperCase())).join(" ");
                    return `${readableKey}: ${value}`;
                }).join("; ");

                indicatorParamsSpan.textContent = formattedParams;

                indicatorsContainer.appendChild(indicatorNode);
            });
            noIndicatorsText.classList.add("hidden");
        }
        else {
            indicatorsContainer.classList.add("hidden");
            noIndicatorsText.classList.remove("hidden");
        }
    }

    // Insert risk model details associated with a parameter
    insertRiskModel(paramNode, param) {
        const buySignalContainer = paramNode.querySelector(".action-buy-signal");
        const shortSignalContainer = paramNode.querySelector(".action-short-signal");

        if (param && param.action) {
            if (param.action.buy_signal) {
                const buySignal = param.action.buy_signal;
                buySignalContainer.querySelector(".stop-loss-percentage").textContent = buySignal.stop_loss.type + ", " + buySignal.stop_loss.percentage + "%";
                buySignalContainer.querySelector(".take-profit-percentage").textContent = buySignal.take_profit.type + ", " + buySignal.take_profit.percentage + "%";
                buySignalContainer.querySelector(".position-size-percentage").textContent = buySignal.position_size.type + ", " + buySignal.position_size.percentage + "%";
            }
            else {
                buySignalContainer.classList.add("hidden");
            }
            if (param.action.short_signal) {
                const shortSignal = param.action.short_signal;
                shortSignalContainer.querySelector(".stop-loss-percentage").textContent = shortSignal.stop_loss.type + ", " + shortSignal.stop_loss.percentage + "%";
                shortSignalContainer.querySelector(".take-profit-percentage").textContent = shortSignal.take_profit.type + ", " + shortSignal.take_profit.percentage + "%";
                shortSignalContainer.querySelector(".position-size-percentage").textContent = shortSignal.position_size.type + ", " + shortSignal.position_size.percentage + "%";
            }
            else {
                shortSignalContainer.classList.add("hidden");
            }
        } else {
            buySignalContainer.classList.add("hidden");
            shortSignalContainer.classList.add("hidden");
        }
    }

    // Set basic values like title and dataset
    setBasicValues() {
        this.card.querySelector(".strategy-title").textContent = this.strategy.name;
        this.card.dataset.value = JSON.stringify(this.id);
    }

    // Set base strategy information
    setBaseStrategy() {
        const baseStrategyTitle = this.card.querySelector(".base-strategy-title");
        const baseStrategyElem = this.card.querySelector(".base-strategy");

        if (this.strategy.base_strategy_id) {
            baseStrategyTitle.textContent = this.strategy.base_strategy_name;
        }
        else {
            baseStrategyElem.classList.add("hidden");
        }
    }

    // Setup event listeners for the card
    setupEvents() {
        const deleteButton = this.card.querySelectorAll('.delete-button');

        deleteButton.forEach(button => {
            button.addEventListener('click', async (e) => {
                if (confirm('Are you sure you want to delete this strategy?')) {
                    this.delete();
                }
            });
        });
    }

    delete() {
        const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');

        if (!csrfToken) {
            console.error("CSRF token not found");
        }

        fetch(`/api/strategies/delete`, {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
            },
            body: JSON.stringify({
                strategy_id: this.id,
            }),
        })
        .then(response => {
            response.json().then(data => {
                if (!response.ok) {
                    alert(data.message || "Failed to delete strategy");
                }
                else {
                    alert("Strategy deleted successfully");
                    this.root.removeChild(this.card);
                } 
            });
        });
    }
}

export default StrategyCard;