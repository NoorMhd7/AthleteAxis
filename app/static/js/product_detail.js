function handleAddToCart(button) {
    button.textContent = 'Item Added';
    setTimeout(() => {
        button.textContent = 'Add To Cart';
    }, 2000);
}

document.getElementById('quantity').addEventListener('change', function() {
    document.getElementById('form-quantity').value = this.value;
});
                    