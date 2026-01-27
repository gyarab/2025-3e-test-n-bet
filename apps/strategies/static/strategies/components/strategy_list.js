import StrategyCard from '../components/strategy_card.js';

class StrategyList {
    constructor(rootElement, strategies) {
        this.root = rootElement;
        this.strategies = strategies;
        this.container = this.root.querySelector('.strategy-container');
        this.noStrategiesTitle = this.root.querySelector('.no-strategies-title');

        this.buildUI();

        window.addEventListener("strategy:changed", (e) => {
            this.handleStrategyChanged(e.detail);
        });
    }

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
                new StrategyCard(this.container, strategy);
            });
        }
    }

    reload() {
        this.container.innerHTML = '';
        this.buildUI();
    }

    
    handleStrategyAdded(event) {
        const newStrategy = event.detail;
        this.strategies.push(newStrategy);
        this.reload();
    }
}

export default StrategyList;