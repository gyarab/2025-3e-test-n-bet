import Indicator from './indicator.js';

class IndicatorSelector {
    constructor(root, indicatorsData) {
        this.wrapper = root;

        this.indicators = indicatorsData.indicators.map(i => new Indicator(i.name, i.parameters)); // All available indicators
        this.available_indicators = this.indicators; // Available to select
        this.selected_indicators = new Set(); // Selected

        this.buildUI();
        this.bindEvents();
    }

    // Creates the HTML elements
    buildUI() {
        this.wrapper.innerHTML = `
            <input name="indicator-input" class="indicator-input border p-2 w-full rounded mb-2" placeholder="Add new indicator...">
            <div class="indicator-list bg-white border rounded shadow mb-2 hidden max-h-40 overflow-auto"></div>
            <div class="indicator-cards"></div>
        `;

        this.input = this.wrapper.querySelector("input[name='indicator-input']");
        this.list = this.wrapper.querySelector(".indicator-list");
        this.cards = this.wrapper.querySelector(".indicator-cards");

        this.updateList();
    }

    // Changes the list's html content based on the input
    updateList() {
        const q = this.input.value.toLowerCase();
        this.list.innerHTML = "";
        
        const optionsToShow = this.available_indicators.filter(opt => 
            opt.getName().toLowerCase().includes(q)
        );
        
        if (optionsToShow.length === 0) {
            const empty = document.createElement("div");
            empty.className = "p-2 text-gray-400 text-sm";
            empty.textContent = "No results found";
            this.list.appendChild(empty);
            return;
        }

        optionsToShow.forEach(opt => {
            const el = document.createElement("div");
            el.className = "p-2 hover:bg-gray-100 cursor-pointer";
            el.dataset.value = this.getIndicatorId(opt);
            el.textContent = opt.getName();
            this.list.appendChild(el);
        });
    }


    // Reloads the choice-list. Must be called after each operation
    reloadTheInitialList() {
        let updated = []

        for (const opt of this.indicators) {  
            if (!this.isSelected(opt)) {
                updated.push(opt)
            }
        }

        this.available_indicators = updated

        this.updateList();
    }
    

    // Adds open/close list events 
    bindEvents() {
        this.input.addEventListener("input", () => {
            this.updateList();
            this.list.classList.remove("hidden"); 
            this.clearHighlight([...this.list.querySelectorAll(".bg-gray-200")]);
        });

        this.input.addEventListener("focus", () => this.list.classList.remove("hidden"));
        
        // Closing the list when clicking outside
        document.addEventListener("click", (e) => {
            if (!this.wrapper.contains(e.target)) {
                this.list.classList.add("hidden");
            }
        });
        
        // Choosing an indicator from the list
        this.list.addEventListener("click", (e) => {
            e.stopPropagation();
            if (!e.target.dataset.value) return;
            this.addIndicatorById(e.target.dataset.value);

            if (!this.wrapper.contains(e.target)) {
                this.list.classList.add("hidden");
                this.clearHighlight([...this.list.querySelectorAll(".bg-gray-200")]);
            }
        });

        // Keyboard navigation
        this.input.addEventListener("keydown", (e) => {
            if (e.key === "Enter") {
                e.preventDefault();
                e.stopPropagation();
            }

            const items = [...this.list.querySelectorAll("[data-value]")];

            if (items.length === 0 || this.list.classList.contains("hidden")) {
                if (["ArrowUp", "ArrowDown"].includes(e.key)) {
                    e.preventDefault();
                    e.stopPropagation();
                }
                return false;
            }

            let index = items.findIndex(i => i.classList.contains("bg-gray-200"));

            if (e.key === "ArrowDown") {
                e.preventDefault();
                index = this.highlightMatch(items, index, 1);
            }

            if (e.key === "ArrowUp") {
                e.preventDefault();
                index = this.highlightMatch(items, index, -1);
            }

            if (e.key === "Enter" && index >= 0) {
                e.preventDefault();
                e.stopPropagation();
                this.addIndicator(items[index].dataset.value);
            }

            if (e.key === "Escape") {
                e.preventDefault();
                e.stopPropagation();
                this.clearHighlight([...this.list.querySelectorAll(".bg-gray-200")]);
                this.list.classList.add("hidden");
            }
        });       
    }

    // Highlights the matched item in the list
    highlightMatch(items, index, delta= 1) {
        if (index >= 0) 
            items[index].classList.remove("bg-gray-200");
        index = (index + delta + items.length) % items.length;
        items[index].classList.add("bg-gray-200");
        items[index].scrollIntoView({ block: "nearest" });
        return index;
    }

    // Clears all highlights
    clearHighlight(items) {
        items.forEach(i => i.classList.remove("bg-gray-200"));
    }

    createIndicatorCard(name, id) {
        const tpl = document.getElementById("indicator-card-template");
        const node = tpl.content.cloneNode(true);

        const card = node.querySelector(".indicator-card");
        card.querySelector(".indicator-title").textContent = name;
        card.dataset.id = id;

        return card;
    }

    

    // Adding inidcator after it being chosen
    addIndicatorById(id) {
        if (id === undefined || id === null || id === "") {
            return;
        }

        const indicator = this.getIndicatorById(id);

        if (this.isSelected(indicator)) 
            return;

        this.addIndicatorToSelected(indicator);

        const card = this.createIndicatorCard(indicator.getName(), id);
        
        this.cards.appendChild(card);
        
        // Because card was just added, we need to wait for the next frame to trigger the transition
        requestAnimationFrame(() => {
            card.classList.remove("opacity-0", "scale-80", "max-h-0");
            card.classList.add("opacity-100", "scale-100", "max-h-[500px]");
        });

        const settings = card.querySelector(".settings");
        const parametersContainer = card.querySelector(".parameters");
        this.addParameterToIndicator(parametersContainer, id);

        const header = card.querySelector(".card-header");
        const removeBtn = card.querySelector(".remove-card");
        const expandIcon = card.querySelector(".arrow");
        
        //Toggles the parameter settings section
        const toggleExpand = (e) => {
            e.stopPropagation();
            e.preventDefault();

            expandIcon.classList.toggle("rotate-180");
            expandIcon.classList.toggle("text-teal-900");

            // Animate settings section
            if (settings.classList.contains("max-h-0")) {
                // Expanding
                settings.classList.remove("max-h-0", "opacity-0");
                settings.classList.add("max-h-40", "opacity-100", "mt-2");
                settings.style.overflowY = "hidden";

                // Adding overflow auto after transition
                settings.addEventListener("transitionend", function handler() {
                    settings.style.overflowY = "auto";
                    settings.removeEventListener("transitionend", handler);
                });
            } else {
                // Collapsing
                settings.classList.remove("max-h-40", "opacity-100", "mt-2");
                settings.classList.add("max-h-0", "opacity-0");
                settings.style.overflowY = "hidden";
            }
        };

        header.addEventListener("click", toggleExpand);
        expandIcon.addEventListener("click", toggleExpand);

        removeBtn.addEventListener("click", (e) => {
            e.stopPropagation();
            e.preventDefault();
            this.removeIndicator(id);
        });

        this.reloadTheInitialList()
    }

    // Adds parameter inputs based on the indicator's parameters
    addParameterToIndicator(settings, id) {
        const indicator = this.getIndicatorById(id);
        const indicatorName = indicator.getName();

        function capitalizeWords(str) {
            return str
                .split("_") 
                .map(word => word.charAt(0).toUpperCase() + word.slice(1))
                .join(" ");
        };

        this.indicators.forEach(indicator => {
            if (indicator.getName() === indicatorName) {
                indicator.getParameters().forEach(param => {
                    const container = document.createElement("div");

                    const label = document.createElement("label");
                    label.className = "block text-sm font-medium text-gray-700 mb-1";
                    label.textContent = capitalizeWords(param.name);
                    container.appendChild(label);

                    const input = document.createElement("input");
                    input.type = "number";
                    input.min = param.min;
                    input.max = param.max;
                    input.className = "w-full border border-gray-300 rounded-lg p-2 focus:ring-2 focus:ring-teal-400 focus:border-teal-400 transition duration-150";  
                    input.placeholder = param.default;  
                    input.value = param.default;
                    
                    // Update indicator parameter value on input change
                    input.addEventListener('input', () => {
                        indicator.setValue(param.name, parseFloat(input.value));
                    });

                    // Ensuring the value stays within bounds
                    input.addEventListener('blur', () => {
                        input.value = Math.min(input.max, Math.max(input.min, input.value));
                    });

                    container.appendChild(input);

                    settings.appendChild(container);
                });
            }
        });
    }


    // Removes the indicator based on its data-value
    removeIndicatorById(id) {
        if (id === undefined || id === null || id === "") {
            return;
        }

        const indicator = this.getIndicatorById(id);

        this.removeIndicatorFromSelected(indicator);

        const card = this.cards.querySelector(
            `[data-value="${id}"]`
        );
        if (!card) return;
        
        card.classList.remove("opacity-100", "scale-100", "max-h-[500px]");
        card.classList.add("opacity-0", "scale-80", "max-h-0", "p-0", "mb-0");

        card.addEventListener("transitionend", () => {
            card.remove();
            this.reloadTheInitialList();
        });
    }

    // Removes indicator from selected set
    removeIndicatorFromSelected(ind) {
        this.selected_indicators.delete(ind);
    }

    // Returns indicator by its id
    getIndicatorById(id) {
        return this.indicators[id];
    }

    // Returns indicator's id
    getIndicatorId(indicator) {
        return this.indicators.findIndex(opt => opt === indicator);
    }

    // Checks if indicator is already selected
    isSelected(indicator) {
        return this.selected_indicators.has(indicator);
    }

    // Adds indicator to selected set
    addIndicatorToSelected(ind) {
        this.selected_indicators.add(ind);
    }
    
    // Returns array of selected indicators
    getSelectedIndicators() {
        return Array.from(this.selected_indicators);
    }

    // Returns data of selected indicators
    getSelectedIndicatorsData() {
        const selectedIndicators = Array.from(this.selected_indicators);
        const data = selectedIndicators.map(ind => {
            return ind.getIndicatorData();
        });
        return data;
    }
}

export default IndicatorSelector;