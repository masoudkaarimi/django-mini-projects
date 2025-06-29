class CartManager {
    constructor() {
        this.storageKey = 'shopping_cart';
        this.expirationKey = 'shopping_cart_expiration';
        // Todo:
        this.expirationTime = 15 * 60 * 1000; // 15 minutes in milliseconds
        // Todo:
        this.csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    }

    async init() {
        await this.checkExpiration();
        this.attachEvents();
        this.updateCartUI();
        if (this.isAuthenticated()) {
            await this.syncWithServer();
        }
    }

    getCart() {
        const cartData = localStorage.getItem(this.storageKey);
        if (!cartData) return {items: [], total: 0, itemCount: 0};

        try {
            return JSON.parse(cartData);
        } catch (e) {
            console.error('Error parsing cart data:', e);
            return {items: [], total: 0, itemCount: 0};
        }
    }

    saveCart(cart) {
        localStorage.setItem(this.storageKey, JSON.stringify(cart));

        const expiration = Date.now() + this.expirationTime;
        localStorage.setItem(this.expirationKey, expiration.toString());

        this.updateCartUI();
    }

    async checkExpiration() {
        const expirationTime = localStorage.getItem(this.expirationKey);

        if (!expirationTime) {
            // No expiration time set, set it now
            const expiration = Date.now() + this.expirationTime;
            localStorage.setItem(this.expirationKey, expiration.toString());
            return;
        }

        // Check if the cart has expired
        if (Date.now() > parseInt(expirationTime)) {
            await this.clearCart();
            return true;
        }

        return false;
    }

    async clearCart() {
        localStorage.removeItem(this.storageKey);
        localStorage.removeItem(this.expirationKey);

        if (this.isAuthenticated()) {
            await this.clearServerCart();
        }

        this.updateCartUI();
    }

    async addItem(productVariantId, quantity = 1) {
        productVariantId = parseInt(productVariantId);
        quantity = parseInt(quantity);

        if (isNaN(productVariantId) || isNaN(quantity) || quantity <= 0) {
            console.error('Invalid variant ID or quantity');
            return false;
        }

        if (this.isAuthenticated()) {
            return this.addServerItem(productVariantId, quantity);
        }

        // Check inventory availability
        const inventoryCheck = await this.checkInventory(productVariantId, quantity);
        if (!inventoryCheck.available) {
            showToast(inventoryCheck.message || 'Item is out of stock', 'warning');
            return false;
        }

        // For guest users, update local storage
        const cart = this.getCart();
        const existingItemIndex = cart.items.findIndex(item => item.productVariantId === productVariantId);

        if (existingItemIndex !== -1) {
            // Update existing item
            cart.items[existingItemIndex].quantity += quantity;
        } else {
            // Add new item
            cart.items.push({
                productVariantId,
                quantity,
                dateAdded: Date.now()
            });
        }

        // Update cart totals
        this.updateCartTotals(cart);

        // Save to local storage
        this.saveCart(cart);

        return true;
    }

    async updateItemQuantity(productVariantId, quantity) {
        productVariantId = parseInt(productVariantId);
        quantity = parseInt(quantity);

        if (isNaN(productVariantId) || isNaN(quantity)) {
            console.error('Invalid variant ID or quantity');
            return false;
        }

        if (this.isAuthenticated()) {
            return this.updateServerItem(productVariantId, quantity);
        }

        // For guest users, update local storage
        const cart = this.getCart();
        const existingItemIndex = cart.items.findIndex(item => item.productVariantId === productVariantId);

        if (existingItemIndex === -1) {
            console.error("Item isn't found in the cart");
            return false;
        }

        if (quantity <= 0) {
            // Remove item if quantity is 0 or negative
            cart.items.splice(existingItemIndex, 1);
        } else {
            // Check inventory availability
            const inventoryCheck = await this.checkInventory(productVariantId, quantity);
            if (!inventoryCheck.available) {
                showToast(inventoryCheck.message || 'Not enough stocks available', 'warning');
                return false;
            }

            // Update quantity
            cart.items[existingItemIndex].quantity = quantity;
        }

        // Update cart totals
        this.updateCartTotals(cart);

        // Save to local storage
        this.saveCart(cart);

        // Update the UI directly without page refresh
        this.updateCartItemUI(productVariantId, quantity);

        return true;
    }

    removeItem(productVariantId) {
        productVariantId = parseInt(productVariantId);

        if (isNaN(productVariantId)) {
            console.error('Invalid variant ID');
            return false;
        }

        if (this.isAuthenticated()) {
            return this.removeServerItem(productVariantId);
        }

        // For guest users, update local storage
        const cart = this.getCart();
        const existingItemIndex = cart.items.findIndex(item => item.productVariantId === productVariantId);

        if (existingItemIndex === -1) {
            console.error("Item isn't found in the cart");
            return false;
        }

        // Remove item
        cart.items.splice(existingItemIndex, 1);

        // Update cart totals
        this.updateCartTotals(cart);

        // Save to local storage
        this.saveCart(cart);

        return true;
    }

    updateCartTotals(cart) {
        cart.itemCount = cart.items.reduce((total, item) => total + item.quantity, 0);
        // Todo:
        // Note: We can't calculate accurate total price client-side as we don't have pricing info
        // This will be calculated on the server when checking out
    }

    async checkInventory(productVariantId, quantity) {
        try {
            const url = window.inventoryCheckUrl.replace('0', productVariantId);
            const response = await fetch(`${url}?quantity=${quantity}`);
            if (!response.ok) throw new Error('Network response was not ok');
            return await response.json();
        } catch (error) {
            console.error('Error checking inventory:', error);
            return {available: false, message: 'Error checking inventory'};
        }
    }

    async addServerItem(productVariantId, quantity) {
        try {
            const formData = new FormData();
            formData.append('product_variant_id', productVariantId);
            formData.append('quantity', quantity);

            const response = await fetch(window.addToCartUrl, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': this.csrfToken,
                },
                body: formData
            });

            const data = await response.json();

            if (data.success) {
                this.updateCartUIFromServerData(data.cart_data);
                return true;
            } else {
                showToast(data.message || 'Error adding item to cart', 'error');
                return false;
            }
        } catch (error) {
            console.error('Error adding item to server cart:', error);
            return false;
        }
    }

    async updateServerItem(productVariantId, quantity) {
        try {
            const formData = new FormData();
            formData.append('product_variant_id', productVariantId);
            formData.append('quantity', quantity);

            const response = await fetch(window.updateCartUrl, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': this.csrfToken,
                },
                body: formData
            });

            const data = await response.json();

            if (data.success) {
                this.updateCartUIFromServerData(data.cart_data);
                return true;
            } else {
                showToast(data.message || 'Error updating cart', 'error');
                return false;
            }
        } catch (error) {
            console.error('Error updating server cart:', error);
            return false;
        }
    }

    async removeServerItem(productVariantId) {
        try {
            const formData = new FormData();
            formData.append('product_variant_id', productVariantId);

            const response = await fetch(window.removeFromCartUrl, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': this.csrfToken,
                },
                body: formData
            });

            const data = await response.json();

            if (data.success) {
                this.updateCartUIFromServerData(data.cart_data);
                return true;
            } else {
                showToast(data.message || 'Error removing item from cart', 'error');
                return false;
            }
        } catch (error) {
            console.error('Error removing item from server cart:', error);
            return false;
        }
    }

    async clearServerCart() {
        try {
            const response = await fetch(window.clearCartUrl, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': this.csrfToken,
                }
            });

            const data = await response.json();

            if (data.success) {
                this.updateCartUIFromServerData({items: [], total: 0, item_count: 0});
                return true;
            } else {
                showToast(data.message || 'Error clearing cart', 'error');
                return false;
            }
        } catch (error) {
            console.error('Error clearing server cart:', error);
            return false;
        }
    }

    async syncWithServer() {
        if (!this.isAuthenticated()) return false;

        try {
            const cart = this.getCart();

            if (cart.items.length === 0) return true;

            const response = await fetch(window.syncCartUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.csrfToken,
                },
                body: JSON.stringify({items: cart.items})
            });

            const data = await response.json();

            if (data.success) {
                // Clear local storage after successful sync
                localStorage.removeItem(this.storageKey);
                localStorage.removeItem(this.expirationKey);

                // Update UI with server data
                this.updateCartUIFromServerData(data.cart_data);
                return true;
            } else {
                console.error('Error syncing cart:', data.message);
                return false;
            }
        } catch (error) {
            console.error('Error syncing cart with server:', error);
            return false;
        }
    }

    updateCartUIFromServerData(cartData) {
        const cartCount = document.querySelector('.cart-count');
        if (cartCount) {
            cartCount.textContent = cartData.item_count || 0;
        }

        const cartItemsContainer = document.querySelector('.cart-items-section');
        if (cartItemsContainer && cartData.items) {
            window.location.reload();
        }
    }

    updateCartUI() {
        // Update UI for all users (based on localStorage for guests)
        const cart = this.getCart();
        const cartCount = document.querySelector('.cart-count');

        if (!this.isAuthenticated() && cartCount) {
            cartCount.textContent = cart.itemCount || 0;
        }
    }

    updateCartItemUI(productVariantId, quantity) {
        // Update specific cart item in the UI without refreshing
        const itemQuantityElement = document.querySelector(`.cart-item[data-product-variant-id="${productVariantId}"] .item-quantity`);
        if (itemQuantityElement) {
            if (quantity <= 0) {
                // Remove the item from DOM if quantity is zero
                const cartItem = itemQuantityElement.closest('.cart-item');
                if (cartItem) {
                    cartItem.remove();
                }
            } else {
                // Update the quantity display
                itemQuantityElement.textContent = quantity;

                // If there's a subtotal element, you might need to update it here
                // This depends on your specific HTML structure
            }
        }
    }

    isAuthenticated() {
        return document.body.dataset.authenticated.toLowerCase() === 'true';
    }

    attachEvents() {
        // Add to cart buttons
        document.addEventListener('click', e => {
            const addToCartButton = e.target.closest('.add-to-cart');
            if (!addToCartButton) return;

            e.preventDefault();
            e.stopPropagation();

            const productVariantId = addToCartButton.dataset.productVariantId;
            const quantity = addToCartButton.dataset.quantity || 1;

            // Prevent multiple clicks
            if (addToCartButton.dataset.processing === 'true') return;

            addToCartButton.dataset.processing = 'true';

            this.addItem(productVariantId, quantity).then(success => {
                if (success) {
                    showToast('Item added to cart', 'success');
                } else {
                    showToast('Failed to add item to cart', 'error');
                }

                addToCartButton.dataset.processing = 'false';
            });
        });

        // Clear cart button
        document.addEventListener('click', async e => {
            const clearCartButton = e.target.closest('.clear-cart');
            if (!clearCartButton) return;

            e.preventDefault();
            e.stopPropagation();

            // Prevent multiple clicks
            if (clearCartButton.dataset.processing === 'true') return;

            clearCartButton.dataset.processing = 'true';

            if (confirm('Are you sure you want to clear your cart?')) {
                await this.clearCart();
                showToast('Cart cleared successfully', 'success');
            }

            clearCartButton.dataset.processing = 'false';
        });

        // Handle login events for cart synchronization
        document.addEventListener('login-success', async () => {
            await this.syncWithServer();
        });
    }
}

document.addEventListener('DOMContentLoaded', async () => {
    window.cartManager = new CartManager();
    await window.cartManager.init();
});
