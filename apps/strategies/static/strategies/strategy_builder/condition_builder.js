import IndicatorSelector from './indicator_selector.js';
import { conditionCardTemplate } from './condition_card_template.js';

class ConditionBuilder {
    constructor(selector, indicatorsData) {
        this.wrapper = document.querySelector(selector);
        this.indicatorsData = indicatorsData; 
        this.conditions = [];
        this.index = 0;

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

    // Add a new condition card
    addCondition() {
        const card = document.createElement("div");
        card.className = "p-4 bg-emerald-100 rounded-lg shadow-md overflow-hidden transform opacity-0 scale-90 transition-all duration-300";
        card.id = `condition-card-${this.index}`;  
        
        const cardName = `Condition ${this.conditions.length + 1}`;
        card.innerHTML = conditionCardTemplate(cardName, this.index);
        this.setRiskModelToggles(card, this.index);

        this.conditionList.appendChild(card);

        requestAnimationFrame(() => {
            card.classList.remove("opacity-0", "scale-90");
            card.classList.add("opacity-100", "scale-100");
        });

        const indicatorId = `indicator-selector-${this.index}`;
        const indicatorSelector = new IndicatorSelector(`#${indicatorId}`, this.indicatorsData);
        this.conditions.push({ card, indicatorSelector });

        const removeId = `remove-condition-btn-${this.index}`;
        const removeBtn = card.querySelector(`#${removeId}`);
        removeBtn.addEventListener("click", () => this.removeCondition(card.id));

        this.index += 1;
  
        this.toggleConditionControls();
    }

    // Set up risk model toggles for a condition card (hide/show % input based on type)
    setRiskModelToggles(card, index) {
        const stopLossType = card.querySelector(`#stop-loss-type-${index}`);
        const stopLossPct = card.querySelector(`#stop-loss-pct-${index}`);

        const takeProfitType = card.querySelector(`#take-profit-type-${index}`);
        const takeProfitPct = card.querySelector(`#take-profit-pct-${index}`);

        const positionSizeType = card.querySelector(`#position-size-type-${index}`);
        const positionSizePct = card.querySelector(`#position-size-pct-${index}`);

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
    removeCondition(cardId) {
        const index = this.conditions.findIndex(
            c => c.card.id === cardId
        );

        if (index === -1) return;

        const { card } = this.conditions[index];

        card.classList.remove("opacity-100", "scale-100");
        card.classList.add("opacity-0", "scale-90");

        card.addEventListener(
            "transitionend",
            () => {
                card.remove();
                this.conditions.splice(index, 1);

                this.conditions.forEach((c, i) => {
                    c.card.querySelector("span").textContent = `Condition ${i + 1}`;
                });

                this.toggleConditionControls();
            },
            { once: true }
        );     
    }

    // Toggle condition controls based on number of conditions, adjust margin
    toggleConditionControls() {
        if (this.conditions.length === 0) {
            this.conditionControls.classList.remove("mb-4");
        }
        else {
            this.conditionControls.classList.add("mb-4");
        }
    }

    // Clear all conditions
    clear() {
        this.conditions.forEach(({ card }) => card.remove());
        this.conditions = [];
        this.index = 0;
        this.toggleConditionControls();
    }
}

export default ConditionBuilder;
