class IndicatorSelector {
    //TODO: keyboard support for choosing indicators
    //TODO: smoothly animate card expand/collapse
    //TODO: fix bugs that when something is added and i click enter it deletes
    constructor(selector, options) {
        this.wrapper = document.querySelector(selector);
        this.possible_options = options;
        this.current_options = options;
        this.selected = new Set();

        this.buildUI();
        this.bindEvents();
    }

    // Creates the HTML elements
    buildUI() {
        this.wrapper.innerHTML = `
            <input name="indicator-input" class="indicator-input border p-2 w-full rounded mb-2" placeholder="Add new indicator...">

            <div class="indicator-list bg-white border rounded shadow mb-2 hidden max-h-40 overflow-auto"></div>

            <div class="indicator-cards space-y-3"></div>
        `;

        this.input = this.wrapper.querySelector("input[name='indicator-input']");
        this.list = this.wrapper.querySelector(".indicator-list");
        this.cards = this.wrapper.querySelector(".indicator-cards");

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
                console.log("Clicked outside indicator selector");
            }
        });
        
        // Choosing an indicator from the list
        this.list.addEventListener("click", (e) => {
            e.stopPropagation();
            if (!e.target.dataset.value) return;
            this.addIndicator(e.target.dataset.value);

            if (!this.wrapper.contains(e.target)) {
                this.list.classList.add("hidden");
                this.clearHighlight([...this.list.querySelectorAll(".bg-gray-200")]);
            }
        });

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

    // Adding inidcator after it being chosen
    addIndicator(value) {
        if (this.selected.has(value)) 
            return;

        if (value === undefined || value === null || value === "") {
            return;
        }
            

        this.selected.add(value);

        const card = document.createElement("div");
        card.dataset.value = value;
        card.className = "p-3 bg-blue-100 rounded border cursor-pointer";

        card.innerHTML = `
            <div class="p-4 bg-white rounded-2xl shadow-md hover:shadow-lg transition-shadow duration-200 cursor-pointer border border-gray-100">
                <div class="flex justify-between items-center mb-3">
                    <span class="flex items-center justify-center px-4 py-2 bg-teal-100 text-teal-700 font-semibold rounded-full capitalize tracking-wide">
                        ${value.replace("_", " ")}
                    </span>
                    <button type="button" class="remove-card text-white bg-gray-500 hover:bg-gray-600 rounded-full w-6 h-6 flex items-center justify-center shadow-md transition-colors duration-200">
                        x
                    </button>
                </div>
                <div class="settings mt-2 hidden">
                    <label class="block text-sm font-medium text-gray-700 mb-1">Parameter</label>
                    <input type="number" class="w-full border border-gray-300 rounded-lg p-2 focus:ring-2 focus:ring-teal-400 focus:border-teal-400 transition duration-150" placeholder="Set value...">
                </div>
            </div>
        `;


        this.cards.appendChild(card);

        const settings = card.querySelector(".settings");
        const header = card.querySelector(".flex");
        const removeBtn = card.querySelector(".remove-card");

        removeBtn.addEventListener("click", (e) => {
            e.stopPropagation();
            e.preventDefault();
            this.removeIndicator(value);
        });

        header.addEventListener("click", (e) => {
            e.stopPropagation();
            e.preventDefault();
            settings.classList.toggle("hidden");
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

    // Removes the indicator
    removeIndicator(value) {
        this.selected.delete(value);
        const card = this.cards.querySelector(
            `[data-value="${value}"]`
        );
        const all = this.cards.children;
        for (const c of all) {
            if (c.dataset.value === value) {
                c.remove();
            }
        }

        this.reloadTheInitialList()
    }
}

export default IndicatorSelector;