import IndicatorSelector from './indicator_selector.js';

class ConditionBuilder {
    constructor(root, indicatorsData) {
        this.wrapper = root;
        this.indicatorsData = indicatorsData; 

        this.conditions = [];

        this.buildUI();
        this.bindEvents();
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
        this.setRiskModelToggles(card);

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

    // Set up risk model toggles for a condition card (hide/show % input based on type)
    setRiskModelToggles(card) {
        const stopLoss = card.querySelector('[data-role="stop-loss"]');
        const takeProfit = card.querySelector('[data-role="take-profit"]');
        const positionSize = card.querySelector('[data-role="position-size"]');


        const stopLossType = stopLoss.querySelector('select');
        const stopLossPct = stopLoss.querySelector('input');

        const takeProfitType = takeProfit.querySelector('select');
        const takeProfitPct = takeProfit.querySelector('input');

        const positionSizeType = positionSize.querySelector('select');
        const positionSizePct = positionSize.querySelector('input');

        stopLossPct.parentElement.style.display = stopLossType.value === 'relative' ? 'none' : 'block';
        takeProfitPct.parentElement.style.display = takeProfitType.value === 'relative' ? 'none' : 'block';
        positionSizePct.parentElement.style.display = positionSizeType.value === 'relative' ? 'none' : 'block';

        stopLossType.addEventListener('change', () => {
            stopLossPct.parentElement.style.display = stopLossType.value === 'relative' ? 'none' : 'block';
        });

        takeProfitType.addEventListener('change', () => {
            takeProfitPct.parentElement.style.display = takeProfitType.value === 'relative' ? 'none' : 'block';
        });

        positionSizeType.addEventListener('change', () => {
            positionSizePct.parentElement.style.display = positionSizeType.value === 'relative' ? 'none' : 'block';
        });
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

    collectConditionsData() {
        return this.conditions.map(({ indicatorSelector }) =>
            indicatorSelector.getSelectedIndicators().map(ind =>
            )
        );
    }
}

export default ConditionBuilder;
