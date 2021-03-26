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
    const itemsQuery = getCartItemsAsQueryString(); 
    const w = window.open(
        get_full_url(
            '/api/method/accounting_app.accounting_app.doctype.sales_invoice.sales_invoice.generate_invoice?'
            + itemsQuery)
    );

    if (!w) {
        frappe.msgprint('Please enable popups!');
    }
}

function getCartItemsAsQueryString() {
    let queryString = "";
    setQty(cart);
    for (let item of cart) {
        queryString += encodeURIComponent(item.name) + `=${item.qty}&`
    }

    return queryString;
}

function setQty(cart) {
    const qtyInputs = document.getElementsByClassName('qty-input');

    for (let input of qtyInputs) {
        const name = input.getAttribute('data-name');
        const qty = input.value;
        
        // inefficient, should change the structure of cart object instead
        const itemIndex = cart.findIndex((i) => (i.name == name));
        cart[itemIndex].qty = qty;
    }
}

// Add to cart event callback
function atcButtonListener(event) {
    const atcButton = event.target;
    const itemName = atcButton.getAttribute("data-name");

    if (atcButton.hasAttribute('data-added')) {
        // Item already added to cart, remove it
        const itemIndex = cart.findIndex((i) => (i.name == itemName));
        cart.splice(itemIndex, 1);
        
        // Remove the added attribute
        atcButton.removeAttribute('data-added');
        
        // Change button style and text
        atcButton.innerText = 'Add to cart';
        atcButton.classList.replace('btn-danger', 'btn-success');

    } else {
        // Add this item to cart
        cart.push({
            name: itemName,
            qty: 1
        });

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
        html += `<li>${item.name}`
        // Add qty input
        html += `
        <div class="input-group my-3">
        <input data-name="${item.name}" type="number" class="form-control qty-input" placeholder="Qty" aria-label="Recipient's username" aria-describedby="basic-addon2" value=${item.qty}>
        <div class="input-group-append">
            <span class="input-group-text" id="basic-addon2">Units</span>
        </div>
        </div>
        </li>
        `
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