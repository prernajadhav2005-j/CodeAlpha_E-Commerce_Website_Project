function updateQty(itemId, action) {
  fetch(`/cart/update/${itemId}/${action}/`)
    .then(response => {
      if (response.ok) {
        location.reload();
      }
    });
}
