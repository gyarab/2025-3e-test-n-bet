import StrategyCard from '../components/strategy_card.js';

class StrategyList {
    constructor(rootElement, strategies) {
        this.root = rootElement;
        this.strategies = strategies;
        this.container = this.root.querySelector('.strategy-container');
        this.noStrategiesTitle = this.root.querySelector('.no-strategies-title');

        // this.cards = [];

        this.buildUI();

        window.addEventListener("strategy:added", () => {
            this.handleStrategyAdded();
        });
    }

    // Build the UI for the strategy list
    buildUI() {
        if (this.strategies.length === 0) {
            this.noStrategiesTitle.classList.remove('hidden');
            this.container.classList.add('hidden');
            return;
        }
        else {
            this.noStrategiesTitle.classList.add('hidden');
            this.container.classList.remove('hidden');

            this.strategies.forEach(strategy => {
                const card = new StrategyCard(this.container, strategy);
                // this.cards.push(card);
            });
        }
    }

    // Reload the strategy list UI
    reload() {
        this.container.innerHTML = '';
        this.buildUI();
    }

    // Handle the event when a new strategy is added. Fetch updated strategies and reload the list.
    handleStrategyAdded() {
        this.fetchUserStrategies().then(data => {
            this.strategies = data;
            this.reload();
        });
    }

    // Fetch the user's strategies from the server
    fetchUserStrategies() {
        return fetch("/api/strategies/get/", {
            method: "GET",
            credentials: "same-origin",
            headers: {
                "Accept": "application/json",
            },
        })
        .then(response => {
            return response.json().then(data => {
                if (!response.ok) {
                    console.error(data.message || "Failed to fetch strategies");
                }
                return data.strategies;
            });
        });
    }
}

export default StrategyList;