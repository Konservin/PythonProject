document.querySelectorAll(".delete-filter-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
        const filterId = btn.getAttribute("data-id");
        const filterName = btn.getAttribute("data-name");

        // Set modal data
        document.getElementById("filterToDeleteName").textContent = filterName;
        const form = document.getElementById("delete-filter-form");
        form.action = `/filters/${filterId}/delete`;

        // Show modal
        const modal = new bootstrap.Modal(document.getElementById("deleteFilterModal"));
        modal.show();
    });
});