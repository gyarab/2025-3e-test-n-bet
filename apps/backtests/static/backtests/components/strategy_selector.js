export default class StrategySelector {
    constructor(root, descriptionWrapper, strategiesData) {
        this.wrapper = root;
        this.descriptionWrapper = descriptionWrapper;

        if (!this.wrapper || !this.descriptionWrapper) {
            throw new Error("StrategySelector: Root or description wrapper element not provided");
        }
        
        this.strategiesData = strategiesData;

        const options = strategiesData.map(i => [i.id, i.name]);
        this.possible_options = options;
        this.current_options = options;
        this.selected = null;

        this.buildUI();
        this.bindEvents();
        this.cacheElements();
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
        this.triggerSelectedStrategyEvent();
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

    // Binds events 
    bindEvents() {


        // Opening the list when typing
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

    cacheElements() {
        this.strategyDescription = this.descriptionWrapper.querySelector(".strategy-description");
        this.descriptionPlaceholder = this.descriptionWrapper.querySelector(".strategy-description-placeholder");

        if (!this.strategyDescription) {
            throw new Error("StrategySelector: Strategy description wrapper not found");
        }
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

        if (this.selected == value) 
            return;

        if (value === undefined || value === null || value === "") {
            return;
        }

        this.removeStrategies();

        this.selected = value;

        this.showDescription(id);

        const cardTemplate = document.getElementById("strategy-card-backtest-template");
        const node = cardTemplate.content.cloneNode(true);
        const card = node.querySelector(".strategy-card-unique");

        card.dataset.value = value;
        card.querySelector(".strategy-name").textContent = value.replace("_", " ");

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
        this.triggerSelectedStrategyEvent();
    }

    showDescription(id) {
        const strategy = this.strategiesData.find(s => s.id == id);

        const cardTemplate = document.getElementById("strategy-description-template");
        const signalModelTemplate = document.getElementById("signal-model-template");
        const actionSignalTemplate = document.getElementById("action-signal-template");

        const node = cardTemplate.content.cloneNode(true);
        const card = node.querySelector(".strategy-description");

        card.querySelector(".strategy-name").textContent = strategy.name;

        for (const param of strategy.parameters) {
            if (param.signal_models?.indicators?.length > 0) {
                const signalModelsList = card.querySelector(".signal-models");
                param.signal_models.indicators.forEach(ind => {
                    const indNode = signalModelTemplate.content.cloneNode(true);
                    indNode.querySelector(".signal-model-name").textContent = ind.name;

                    const paramsList = indNode.querySelector(".signal-model-parameters");
                    for (const [key, val] of Object.entries(ind.parameters || {})) {
                        const li = document.createElement("li");
                        li.textContent = `${key}: ${val}`;
                        paramsList.appendChild(li);
                    }

                    signalModelsList.appendChild(indNode);
                });
            }
            else {
                card.querySelector(".no-signal-models").classList.remove("hidden");
            }

            if (param.action?.buy_signal || param.action?.sell_signal) {
                const isBuy = !!param.action?.buy_signal;
                const action = isBuy ? param.action.buy_signal : param.action.sell_signal;
                const title = isBuy ? "Buy Signal" : "Sell Signal";

                const actionNode = actionSignalTemplate.content.cloneNode(true);
                actionNode.querySelector(".action-title").textContent = title;
                
                actionNode.querySelector(".stop-loss-type").textContent = action.stop_loss.type;
                actionNode.querySelector(".stop-loss-percentage").textContent = action.stop_loss.percentage ? action.stop_loss.percentage + "%" : "-";

                actionNode.querySelector(".take-profit-type").textContent = action.take_profit.type;
                actionNode.querySelector(".take-profit-percentage").textContent = action.take_profit.percentage ? action.take_profit.percentage + "%" : "-";

                actionNode.querySelector(".position-size-type").textContent = action.position_size.type;
                actionNode.querySelector(".position-size-percentage").textContent = action.position_size.percentage ? action.position_size.percentage + "%" : "-";
                
                card.querySelector(".action-models").appendChild(actionNode);
            }
            else {
                card.querySelector(".no-action-models").classList.remove("hidden");
            }
        }

        this.strategyDescription.appendChild(node);

        if (this.descriptionPlaceholder) {
            this.descriptionPlaceholder.classList.add("hidden");
        }
    }

    // Reloads the choice-list. Must be called after each operation
    reloadTheInitialList() {
        let updated = []

        for (const opt of this.possible_options) {       
            if (this.selected != opt) {
                updated.push(opt)
            }
        }

        this.current_options = updated

        this.updateList();
    }

    // Removes the strategy card and description
    removeStrategy(value) {
        this.strategyDescription.innerHTML = "";
        this.selected = null;
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

        this.triggerSelectedStrategyEvent();

        if (this.descriptionPlaceholder) {
            this.descriptionPlaceholder.classList.remove("hidden");
        }
    }

    // Removes all strategies
    removeStrategies() {
        const existingCards = [...this.cards.querySelectorAll(".strategy-card-unique")];
        existingCards.forEach(card => {
            const value = card.dataset.value;
            this.removeStrategy(value);
        });
    }

    // Triggers a custom event to notify that a strategy has been selected or removed
    triggerSelectedStrategyEvent() {
        const event = new Event('strategySelected', { bubbles: true });
        this.wrapper.dispatchEvent(event);
    }

    // Returns the currently selected strategy object or null if none is selected
    getSelectedStrategy() {
        if (!this.selected) return null;

        const strategy = this.strategiesData.find(s => s.name === this.selected);
        return strategy || null;
    }
}