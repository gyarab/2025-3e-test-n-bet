class IndicatorSelector {
    //TODO: keyboard support for choosing indicators
    //TODO: smoothly animate card expand/collapse
    //TODO: 
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
            <input class="indicator-input border p-2 w-full rounded mb-2" placeholder="Search...">

            <div class="indicator-list bg-white border rounded shadow mb-2 hidden max-h-40 overflow-auto"></div>

            <div class="indicator-cards space-y-3"></div>
        `;

        this.input = this.wrapper.querySelector(".indicator-input");
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
            this.addIndicator(e.target.dataset.value);
        });
    }

    // Adding inidcator after it being chosen
    addIndicator(value) {
        if (this.selected.has(value)) 
            return;

        this.selected.add(value);

        const card = document.createElement("div");
        card.dataset.value = value;
        card.className = "p-3 bg-blue-100 rounded border cursor-pointer";

        card.innerHTML = `
            <div class="flex justify-between items-center">
                <span class="font-semibold capitalize">${value.replace("_", " ")}</span>
                <button class="remove-card text-red-600 font-bold text-lg leading-none px-2">×</button>
            </div>

            <div class="settings mt-3 hidden">
                <label class="block text-sm text-gray-600 mb-1">Parameter</label>
                <input type="number" class="w-full border p-2 rounded" placeholder="Set value...">
            </div>
        `;

        this.cards.appendChild(card);

        const settings = card.querySelector(".settings");
        const removeBtn = card.querySelector(".remove-card");

        card.addEventListener("click", (e) => {
            if (e.target === removeBtn) return;
            settings.classList.toggle("hidden");
        });

        removeBtn.addEventListener("click", (e) => {
            e.stopPropagation();
            this.removeIndicator(value);
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