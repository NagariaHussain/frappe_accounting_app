// Get all add to cart buttons
const add_to_cart_buttons = document.querySelectorAll(".atc-button");

// Add click listeners to all ATC buttons
for (let button of add_to_cart_buttons) {
    button.addEventListener('click', atcButtonListener);
}

// Add to cart event callback
function atcButtonListener(event) {
    console.log(
        event.target.getAttribute("data-name"), 
        "will be added to the cart!"
    );
}