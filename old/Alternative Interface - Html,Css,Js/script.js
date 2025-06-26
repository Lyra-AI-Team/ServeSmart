function toggleMenu() {
    const navLinks = document.querySelector('.nav-links');
    navLinks.classList.toggle('show');
}
// Function to change theme
function changeTheme(theme) {
    document.body.className = theme;
}

// Function to add product to cart
function addToCart(product, price) {
    let cartItems = JSON.parse(localStorage.getItem('cartItems')) || [];
    cartItems.push({ product, price });
    localStorage.setItem('cartItems', JSON.stringify(cartItems));
    
    // Show notification
    let notification = document.getElementById('notification');
    notification.innerText = `${product} added to cart!`;
    notification.style.display = 'block';
    setTimeout(() => {
        notification.style.display = 'none';
    }, 1500);
}

// Function to display cart items and total
function displayCart() {
    let cartItems = JSON.parse(localStorage.getItem('cartItems')) || [];
    let cartItemsDiv = document.getElementById('cartItems');
    let totalDiv = document.getElementById('total');

    cartItemsDiv.innerHTML = '';
    let total = 0;

    cartItems.forEach((item, index) => {
        cartItemsDiv.innerHTML += `
            <p>
                ${item.product} - $${item.price}
                <button onclick="removeFromCart(${index})">Remove</button>
            </p>`;
        total += item.price;
    });

    totalDiv.innerHTML = `<h3>Total: $${total}</h3>`;
}

// Function to remove a single item from cart
function removeFromCart(index) {
    let cartItems = JSON.parse(localStorage.getItem('cartItems')) || [];
    cartItems.splice(index, 1);
    localStorage.setItem('cartItems', JSON.stringify(cartItems));
    displayCart();
}

// Function to clear the cart
function clearCart() {
    localStorage.removeItem('cartItems');
    displayCart();
}

// Call displayCart if on cart page
if (document.getElementById('cartItems')) {
    displayCart();
}
