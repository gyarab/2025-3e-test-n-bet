class IndicatorSelector {
    constructor(selector, options) {
        this.wrapper = document.querySelector(selector);
        this.possible_options = options;
        this.current_options = options;
        this.selected = new Map();

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

        this.renderList();
    }

    // Opens the drop-list
    renderList() {
        const q = this.input.value.toLowerCase();
        this.list.innerHTML = "";

        this.current_options
            .filter(opt => opt.includes(q))
            .forEach(opt => {
                const el = document.createElement("div");
                el.className = "p-2 hover:bg-gray-100 cursor-pointer";
                el.dataset.value = opt;
                console.log(opt)
                this.list.appendChild(el);
            });
    }

    // Adds open/close events 
    bindEvents() {
        this.input.addEventListener("input", () => this.renderList());
        this.input.addEventListener("focus", () => this.list.classList.remove("hidden"));

        document.addEventListener("click", (e) => {
            if (!this.wrapper.contains(e.target)) {
                this.list.classList.add("hi`dden");
            }
        });

        this.list.addEventListener("click", (e) => {
            if (!e.target.dataset.value) return;
            this.addIndicator(e.target.dataset.value);
        });
    }

    // Adding inidcator after it being chosen
    addIndicator(value) {
        if (this.selected.has(value)) return;

        this.selected.set(value, true);

        const card = document.createElement("div");
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
            
            if (isSelected) {
                updated.push(opt)
            }
        }

        this.current_options = updated

        this.renderList();
    }

    // Removes the indicator
    removeIndicator(value) {
        this.selected.delete(value);
        const card = this.cards.querySelector(
            `[data-value="${value}"]`
        );
        const all = this.cards.children;
        for (const c of all) {
            if (c.querySelector("span").textContent.toLowerCase().replace(" ", "_") === value) {
                c.remove();
            }
        }

        this.reloadTheInitialList()
    }
}

export default IndicatorSelector;