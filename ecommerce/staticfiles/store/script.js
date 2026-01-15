// --------------------
// CONFIRM REMOVE FROM CART
// --------------------
function confirmRemove() {
    return confirm("Are you sure you want to remove this item?");
}

// --------------------
// QUANTITY INCREASE / DECREASE (UI ONLY)
// --------------------
function increaseQty(id) {
    let qtyInput = document.getElementById("qty-" + id);
    qtyInput.value = parseInt(qtyInput.value) + 1;
}

function decreaseQty(id) {
    let qtyInput = document.getElementById("qty-" + id);
    if (qtyInput.value > 1) {
        qtyInput.value = parseInt(qtyInput.value) - 1;
    }
}

// --------------------
// AUTO SUBMIT CATEGORY FILTER
// --------------------
document.addEventListener("DOMContentLoaded", function () {
    const categorySelect = document.getElementById("category-select");
    if (categorySelect) {
        categorySelect.addEventListener("change", function () {
            window.location.href = this.value;
        });
    }
});
