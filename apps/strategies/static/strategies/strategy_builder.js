document.addEventListener("DOMContentLoaded", () => {
    const select = new TomSelect('#indicators', {
        plugins: ['remove_button'],
        persist: false,

        render: {
            item: function(data, escape) {
                return `
                    <div class="indicator-chip cursor-pointer bg-blue-100 px-3 py-1 rounded-md" data-value="${data.value}">
                        ${escape("adfsd")}
                                        <div class="font-semibold mb-2 capitalize">${value.replace("_", " ")} Settings</div>
                <label class="block text-sm text-gray-600 mb-1">Parameter</label>
                <input type="number" class="w-full border p-2 rounded" placeholder="Set value..." />
                    </div>
                `;
            }
        },

        onItemAdd: function(value, item) {
            item.addEventListener("click", () => {
                console.log("Clicked:", value);
            });

            const paramsBox = document.createElement("div");
            paramsBox.className = "indicator-params bg-gray-50 p-3 rounded-lg border mb-2";

            paramsBox.innerHTML = `
                <div class="font-semibold mb-2 capitalize">${value.replace("_", " ")} Settings</div>
                <label class="block text-sm text-gray-600 mb-1">Parameter</label>
                <input type="number" class="w-full border p-2 rounded" placeholder="Set value..." />
            `;

            item.insertAdjacentElement("afterend", paramsBox);
        },

        onItemRemove: function(value) {
            // Remove associated params UI
            document.querySelectorAll(`.indicator-params`)
                .forEach(el => {
                    if (el.previousElementSibling.dataset.value === value) {
                        el.remove();
                    }
                });
        }
    });
});
