// Get all add to cart buttons
const add_to_cart_buttons = document.querySelectorAll(".atc-button");

// To store cart data
let cart = [];

// Add click listeners to all ATC buttons
for (let button of add_to_cart_buttons) {
    button.addEventListener('click', atcButtonListener);
}

// Add to cart event callback
function atcButtonListener(event) {
    const atcButton = event.target;
    const itemName = atcButton.getAttribute("data-name");

    if (atcButton.hasAttribute('data-added')) {
        // Item already added to cart, remove it
        const itemIndex = cart.indexOf(itemName);
        cart.splice(itemIndex, 1);
        // Remove the added attribute
        atcButton.removeAttribute('data-added');
        // Change button style and text
        atcButton.innerText = 'Add to cart';
        atcButton.classList.replace('btn-danger', 'btn-success');
    } else {
        // Add this item to cart
        cart.push(itemName);
        // Add the added attribute
        atcButton.setAttribute('data-added', '');
        // Change button style and text
        atcButton.innerText = 'Remove';
        atcButton.classList.replace('btn-success', 'btn-danger');
    }
}
