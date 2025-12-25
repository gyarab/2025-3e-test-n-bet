import { strategyCardTemplate } from "./strategy_card_template.js";

class StrategySelector {
    constructor(selector, strategysData) {
        this.wrapper = document.querySelector(selector);

        const options = strategysData.strategys.map(i => i.name);
        this.possible_options = options;
        this.current_options = options;
        this.selected = new Set();

        this.strategysData = strategysData.strategys;

        this.buildUI();
        this.bindEvents();
    }

    // Creates the HTML elements
    buildUI() {
        this.wrapper.innerHTML = `
            <input name="strategy-input" class="strategy-input border p-2 w-full rounded mb-2" placeholder="Add new strategy...">

            <div class="strategy-list bg-white border rounded shadow mb-2 hidden max-h-40 overflow-auto"></div>

            <div class="strategy-cards"></div>
        `;

        this.input = this.wrapper.querySelector("input[name='strategy-input']");
        this.list = this.wrapper.querySelector(".strategy-list");
        this.cards = this.wrapper.querySelector(".strategy-cards");

        this.updateList();
    }

    // Changes the list's content based on the input
    updateList() {
        const q = this.input.value.toLowerCase();
        this.list.innerHTML = "";
        
        const optionsToShow = this.current_options.filter(opt => 
            opt.toLowerCase().includes(q)
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
            el.dataset.value = opt;
            el.textContent = opt;
            this.list.appendChild(el);
        });
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
        
        // Choosing an strategy from the list
        this.list.addEventListener("click", (e) => {
            e.stopPropagation();
            if (!e.target.dataset.value) return;
            this.addStrategy(e.target.dataset.value);

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
                this.addStrategy(items[index].dataset.value);
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

    // Adding inidcator after it being chosen
    addStrategy(value) {
        if (this.selected.has(value)) 
            return;

        if (value === undefined || value === null || value === "") {
            return;
        }

        this.selected.add(value);

        const card = document.createElement("div");
        card.dataset.value = value;
        card.className = "overflow-hidden transform opacity-0 scale-80 max-h-0 mb-3 transition-all duration-500 ease-out p-3 bg-teal-300 rounded border cursor-pointer";

        card.innerHTML = strategyCardTemplate(value.replace("_", " "));

        this.cards.appendChild(card);
        
        // Because card was just added, we need to wait for the next frame to trigger the transition
        requestAnimationFrame(() => {
            card.classList.remove("opacity-0", "scale-80", "max-h-0");
            card.classList.add("opacity-100", "scale-100", "max-h-[500px]");
        });

        const settings = card.querySelector(".settings");
        const parametersContainer = card.querySelector(".parameters");
        this.addParameterToStrategy(parametersContainer, value);

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
            this.removeStrategy(value);
        });

        this.reloadTheInitialList()
    }

    // Reloads the choice-list. Must be called after each operation
    reloadTheInitialList() {
        let updated = []

        for (const opt of this.possible_options) {
            const isSelected = this.selected.has(opt)
            
            if (!isSelected) {
                updated.push(opt)
            }
        }

        this.current_options = updated

        this.updateList();
    }

    // Removes the strategy
    removeStrategy(value) {
        this.selected.delete(value);
        const card = this.cards.querySelector(
            `[data-value="${value}"]`
        );
        if (!card) return;
        
        card.classList.remove("opacity-100", "scale-100", "max-h-[500px]");
        card.classList.add("opacity-0", "scale-80", "max-h-0", "p-0", "mb-0");

        card.addEventListener("transitionend", () => {
            card.remove();
            const all = this.cards.children;
            this.reloadTheInitialList();
        });
    }
}

export default StrategySelector;