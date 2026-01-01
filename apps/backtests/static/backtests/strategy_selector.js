import { strategyCardTemplate } from "./templates/strategy_card_template.js";
import { strategyDescriptionTemplate } from "./templates/strategy_description_template.js";

export default class StrategySelector {
    constructor(selector, strategiesData) {
        this.wrapper = document.querySelector(selector);

        this.strategiesData = strategiesData;

        const options = strategiesData.map(i => [i.id, i.name]);
        this.possible_options = options;
        this.current_options = options;
        this.selected = new Set();

        this.buildUI();
        this.bindEvents();
    }

    // Creates the HTML elements
    buildUI() {
        this.wrapper.innerHTML = `
            <div class="flex items-center space-x-2">
                <input name="strategy-input" class="strategy-input border p-2 w-full rounded mb-2" placeholder="Select strategy...">
                <a href="/strategies/" class="inline-block">
                    <button type="button" class="mb-2 px-4 py-2 bg-teal-500 text-white rounded hover:bg-teal-600 transition-colors duration-200 flex items-center justify-center">
                        <span class="text-1xl font-bold transform scale-5">+</span>
                    </button>
                </a>
            </div>
            <div class="strategy-list bg-white border rounded shadow mb-2 hidden max-h-40 overflow-auto"></div>
            <div class="strategy-cards"></div>
        `;

        this.input = this.wrapper.querySelector("input[name='strategy-input']");
        this.list = this.wrapper.querySelector(".strategy-list");
        this.cards = this.wrapper.querySelector(".strategy-cards");

        this.updateList();
        this.updateButtonColor();
    }

    // Changes the list's content based on the input
    updateList() {
        const q = this.input.value.toLowerCase();
        this.list.innerHTML = "";
        
        const optionsToShow = this.current_options.filter(opt => 
            opt[1].toLowerCase().includes(q)
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
            el.dataset.value = opt; // Set data-value attribute to find it later
            el.textContent = opt[1];
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
    addStrategy(datasetValue) {
        
        const id = datasetValue.split(",")[0];
        const value = datasetValue.split(",")[1];

        if (this.selected.has(value)) 
            return;

        if (value === undefined || value === null || value === "") {
            return;
        }

        for (const selectedValue of [...this.selected]) {
            this.removeStrategy(selectedValue);
        }

        this.selected.add(value);
        this.showDescription(id);

        const card = document.createElement("div");
        card.dataset.value = value;

        card.className = "strategy-card-unique overflow-hidden transform opacity-0 scale-80 max-h-0 transition-all duration-500 ease-out cursor-pointer";
        card.id = `strategy-card-${id}`;
        card.innerHTML = strategyCardTemplate(value.replace("_", " "));

        this.cards.appendChild(card);
        
        // Because card was just added, we need to wait for the next frame to trigger the transition
        requestAnimationFrame(() => {
            card.classList.remove("opacity-0", "scale-80", "max-h-0");
            card.classList.add("opacity-100", "scale-100", "max-h-[500px]");
        });

        const removeBtn = card.querySelector(".remove-card");

        removeBtn.addEventListener("click", (e) => {
            e.stopPropagation();
            e.preventDefault();
            this.removeStrategy(value);
        });

        this.reloadTheInitialList();
        this.updateButtonColor();
    }

    showDescription(id) {
        const strategy = this.strategiesData.find(s => s.id == id);

        const field = document.getElementById("strategy-description");
        field.appendChild(strategyDescriptionTemplate(strategy.name, strategy.parameters));
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
        document.getElementById("strategy-description").innerHTML = "";
        this.selected.delete(value);
        const card = this.cards.querySelector(
            `[data-value="${value}"]`
        );
        if (!card) return;
        
        card.classList.remove("opacity-100", "scale-100", "max-h-[500px]");
        card.classList.add("opacity-0", "scale-80", "max-h-0", "p-0", "mb-0");

        card.addEventListener("transitionend", () => {
            card.remove();
            this.reloadTheInitialList();
        });

        this.updateButtonColor();
    }

    updateButtonColor() {
        console.log("fsdfds")
        const startBtn = document.getElementById("start-backtest-btn");
        console.log(startBtn);  
        console.log(this.selected);

        if (this.selected.size > 0) {
            startBtn.classList.remove("bg-gray-400", "cursor-not-allowed");
            startBtn.classList.add("bg-teal-600", "hover:bg-teal-700");
            startBtn.disabled = false;
        } else {
            startBtn.classList.remove("bg-teal-600", "hover:bg-teal-700");
            startBtn.classList.add("bg-gray-400", "cursor-not-allowed");
            startBtn.disabled = true;
        }
    }

    
}