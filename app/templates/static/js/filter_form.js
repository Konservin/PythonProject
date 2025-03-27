document.addEventListener("change", function (e) {
    if (e.target.matches(".type-select")) {
        const typeSelect = e.target;
        const criteriaRow = typeSelect.closest(".row");

        const valueInput = criteriaRow.querySelector(".value-input");
        const selectedOption = typeSelect.options[typeSelect.selectedIndex];
        let valueType = selectedOption.getAttribute("data-value-type");

        if (!valueType) {
            valueType = valueTypes[selectedOption.value];
        }

        if (valueInput) {
            if (valueType === "int") valueInput.type = "number";
            else if (valueType === "date") valueInput.type = "date";
            else valueInput.type = "text";
        }
    }
    if (e.target.matches("select[name^='type_'], select[name='new_type[]']")) {
        const typeSelect = e.target;
        const selectedTypeId = typeSelect.value;

        // Find the sibling subtype select
        const subtypeSelect = typeSelect.closest(".row").querySelector("select[name^='subtype_'], select[name='new_subtype[]']");

        // Fetch filtered subtypes
        fetch(`/subtypes/${selectedTypeId}`)
            .then(response => response.json())
            .then(subtypes => {
                // Clear existing options
                subtypeSelect.innerHTML = "";
                // Add new ones
                subtypes.forEach(subtype => {
                    const option = document.createElement("option");
                    option.value = subtype.id;
                    option.textContent = subtype.name;
                    subtypeSelect.appendChild(option);
                });
            });
    }
});

        document.getElementById("add-criteria").addEventListener("click", function () {
            const tmpl = document.getElementById("criteria-template");
            const clone = tmpl.content.cloneNode(true);
            const newRow = clone.querySelector(".criteria-row");
            criteriaCollection = document.getElementById("criteria-list");
            criteriaCollection.appendChild(clone);
            let event = new Event('change', { bubbles: true });
            newRow.querySelector('.type-select').dispatchEvent(event);
        });

        document.addEventListener("click", function (e) {
            if (e.target.classList.contains("remove-criteria")) {
                const row = e.target.closest(".criteria-row");
                row.remove();
            }
        });

document.getElementById("save-filter").addEventListener("click", function (e) {
    const criteriaRows = document.querySelectorAll(".criteria-row");
    let isValid = true;

    criteriaRows.forEach((row) => {
        const valueInput = row.querySelector(".value-input");

        // Reset validation state
        valueInput.classList.remove("is-invalid");

        // Check for empty value
        if (!valueInput.value.trim()) {
            valueInput.classList.add("is-invalid");
            isValid = false;
        }

        // Optional: Type-specific validation
        if (valueInput.type === "number" && isNaN(valueInput.value)) {
            valueInput.classList.add("is-invalid");
            isValid = false;
        }

        if (valueInput.type === "date") {
            const dateValue = new Date(valueInput.value);
            if (isNaN(dateValue.getTime())) {
                valueInput.classList.add("is-invalid");
                isValid = false;
            }
        }
    });

const errorBlock = document.getElementById("form-error");
if (!isValid) {
    e.preventDefault(); // Stop form submission
    errorBlock.classList.remove("d-none"); // Show error
} else {
    errorBlock.classList.add("d-none"); // Hide error if previously shown
}
});
