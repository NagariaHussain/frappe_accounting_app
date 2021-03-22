// Get all add to cart buttons
const add_to_cart_buttons = document.querySelectorAll(".atc-button");

// To store cart data
let cart = [];

// Add click listeners to all ATC buttons
for (let button of add_to_cart_buttons) {
    button.addEventListener('click', atcButtonListener);
}

// Add click listener to view cart button
const viewCartButton = document.getElementById("view-cart-button");
viewCartButton.addEventListener('click', (event) => {
    let cartHTML = getCartHTML(cart);

    frappe.msgprint({
        title: __('Cart'),
        message: cartHTML,
        primary_action: {
            'label': __('Generate Invoice'),
            action: downloadInvoice
        }
    });
});

function downloadInvoice() {
    const w = window.open(
        get_full_url('/api/method/accounting_app.accounting_app.doctype.sales_invoice.sales_invoice.generate_invoice')
    );

    if (!w) {
        frappe.msgprint('Please enable popups!');
    }
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


// Generate and return cart HTML content
function getCartHTML(cartList)
{
    if (cartList.length === 0) {
        return "No items in cart";
    }

    let html = "";
    for (let item of cartList) {
        html += `<li>${item}</li>`
    }
    html = `<ol>${html}</ol>`

    return html;
}

function get_full_url(url) {
    if(url.indexOf("http://")===0 || url.indexOf("https://")===0) {
        return url;
    }
    return url.substr(0,1)==="/" ?
        (get_base_url() + url) :
        (get_base_url() + "/" + url);
}

function get_base_url() {
    let url = (frappe.base_url || window.location.origin);
    if(url.substr(url.length-1, 1)=='/') url = url.substr(0, url.length-1);
    return url;
}