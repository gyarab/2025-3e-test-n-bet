import IndicatorSelector from './indicator_selector.js';

class ConditionBuilder {
    constructor(selector, indicatorsData) {
        this.wrapper = document.querySelector(selector);
        this.indicatorsData = indicatorsData; 
        this.conditions = [];

        this.buildUI();
        this.bindEvents();
    }

    buildUI() {
        this.wrapper.innerHTML = `
            <div class="condition-controls mb-4">
                <button type="button" class="add-condition-btn bg-teal-500 hover:bg-teal-600 text-white font-semibold px-4 py-2 rounded transition">
                    Add Condition
                </button>
            </div>
            <div class="condition-list space-y-4"></div>
        `;

        this.addBtn = this.wrapper.querySelector(".add-condition-btn");
        this.conditionList = this.wrapper.querySelector(".condition-list");
    }

    bindEvents() {
        this.addBtn.addEventListener("click", () => this.addCondition());
    }

    addCondition() {
        const index = this.conditions.length;

        const card = document.createElement("div");
        card.className = "p-4 bg-white rounded-lg shadow-md overflow-hidden transform opacity-0 scale-90 transition-all duration-300";

        const header = document.createElement("div");
        header.className = "flex justify-between items-center mb-3";

        const title = document.createElement("span");
        title.textContent = `Condition ${index + 1}`;
        title.className = "font-semibold text-gray-700";

        const removeBtn = document.createElement("button");
        removeBtn.type = "button";
        removeBtn.className = "bg-gray-300 hover:bg-gray-400 rounded px-2 py-1 text-sm";
        removeBtn.textContent = "Remove";

        header.appendChild(title);
        header.appendChild(removeBtn);
        card.appendChild(header);

        const indicatorContainer = document.createElement("div");
        indicatorContainer.className = "indicator-selector-container";
        card.appendChild(indicatorContainer);

        this.conditionList.appendChild(card);

        requestAnimationFrame(() => {
            card.classList.remove("opacity-0", "scale-90");
            card.classList.add("opacity-100", "scale-100");
        });

        const indicatorSelector = new IndicatorSelector(indicatorContainer, [], this.indicatorsData);

        this.conditions.push({ card, indicatorSelector });

        removeBtn.addEventListener("click", () => this.removeCondition(index));
    }

    removeCondition(index) {
        const condition = this.conditions[index];
        if (!condition) return;

        const { card } = condition;

        // Animate removal
        card.classList.remove("opacity-100", "scale-100");
        card.classList.add("opacity-0", "scale-90");

        card.addEventListener(
            "transitionend",
            () => {
                card.remove();
                // Remove from array
                this.conditions.splice(index, 1);
                // Re-render titles
                this.conditions.forEach((c, i) => {
                    c.card.querySelector("span").textContent = `Condition ${i + 1}`;
                });
            },
            { once: true }
        );
    }
}

export default ConditionBuilder;
