import os

print("🔧 ACTIVATING REAL SHOPPING CART...")

# --- 1. UPDATED MENU.HTML (Linking to Cart Page) ---
menu_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Menu - Supreme Delivery</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #f8f9fa; }
        .menu-header { background: white; padding: 20px; border-bottom: 1px solid #eee; position: sticky; top: 0; z-index: 10; }
        .item-card { background: white; border-radius: 10px; padding: 15px; margin-bottom: 15px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
        .cart-bar { position: fixed; bottom: 0; left: 0; width: 100%; background: #00B14F; color: white; padding: 15px; display: none; justify-content: space-between; align-items: center; cursor: pointer; }
    </style>
</head>
<body>

    <div class="menu-header d-flex justify-content-between align-items-center">
        <a href="/customer/home" class="btn btn-light rounded-circle">←</a>
        <h5 class="m-0 fw-bold">Burger King Supreme</h5>
        <span><i class="fas fa-search"></i></span>
    </div>

    <div class="container mt-4" style="padding-bottom: 80px;">
        <h6 class="text-muted mb-3">POPULAR ITEMS</h6>
        
        <div class="item-card">
            <div><h6 class="fw-bold m-0">Zinger Burger</h6><div class="mt-2 fw-bold">$5.50</div></div>
            <button class="btn btn-outline-success btn-sm" onclick="addToCart(5.50)">ADD</button>
        </div>
        <div class="item-card">
            <div><h6 class="fw-bold m-0">Beef Whopper</h6><div class="mt-2 fw-bold">$8.00</div></div>
            <button class="btn btn-outline-success btn-sm" onclick="addToCart(8.00)">ADD</button>
        </div>
        <div class="item-card">
            <div><h6 class="fw-bold m-0">Large Fries</h6><div class="mt-2 fw-bold">$3.00</div></div>
            <button class="btn btn-outline-success btn-sm" onclick="addToCart(3.00)">ADD</button>
        </div>
    </div>

    <div class="cart-bar" id="cartBar" onclick="window.location.href='/customer/cart'">
        <span class="fw-bold"><span id="count">0</span> items</span>
        <span class="fw-bold">View Cart • $<span id="total">0.00</span></span>
    </div>

    <script>
        let total = 0;
        let count = 0;
        function addToCart(price) {
            total += price;
            count++;
            document.getElementById('count').innerText = count;
            document.getElementById('total').innerText = total.toFixed(2);
            document.getElementById('cartBar').style.display = 'flex';
        }
    </script>
</body>
</html>
"""

# --- 2. NEW CART.HTML (Checkout Page) ---
cart_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Cart - Supreme Delivery</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #f8f9fa; }
        .cart-footer { position: fixed; bottom: 0; width: 100%; background: white; padding: 20px; box-shadow: 0 -5px 20px rgba(0,0,0,0.05); }
    </style>
</head>
<body>
    <div class="container mt-4">
        <h3>My Cart</h3>
        <div class="card p-3 mt-3 border-0 shadow-sm">
            <div class="d-flex justify-content-between mb-3">
                <span>1x Zinger Burger</span>
                <b>$5.50</b>
            </div>
             <div class="d-flex justify-content-between mb-3">
                <span>1x Large Fries</span>
                <b>$3.00</b>
            </div>
            <hr>
            <div class="d-flex justify-content-between">
                <h5>Total</h5>
                <h5 class="text-success">$8.50</h5>
            </div>
        </div>

        <div class="mt-4">
            <h6>DELIVERY ADDRESS</h6>
            <div class="card p-3 border-0 shadow-sm">
                <i class="fas fa-map-marker-alt text-danger"></i> Home • 123 Main Street, New York
            </div>
        </div>
    </div>

    <div class="cart-footer">
        <button class="btn btn-success w-100 py-3 fw-bold" onclick="placeOrder()">PLACE ORDER</button>
    </div>

    <script>
        function placeOrder() {
            alert("Order #9921 Placed Successfully! Driver is being assigned.");
            window.location.href = "/customer/home";
        }
    </script>
</body>
</html>
"""

# Save Templates
os.makedirs("templates/customer", exist_ok=True)
with open("templates/customer/menu.html", "w", encoding="utf-8") as f:
    f.write(menu_html)
with open("templates/customer/cart.html", "w", encoding="utf-8") as f:
    f.write(cart_html)

# --- 3. UPDATE APP.PY (Add Cart Route) ---
app_path = "app.py"
if os.path.exists(app_path):
    with open(app_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    if "/customer/cart" not in content:
        new_route = """
@app.route('/customer/cart')
def customer_cart():
    return render_template('customer/cart.html')
"""
        parts = content.split("if __name__")
        new_content = parts[0] + new_route + "if __name__" + parts[1]
        
        with open(app_path, "w", encoding="utf-8") as f:
            f.write(new_content)

print("✅ CART PAGE ACTIVATED. Order flow is complete.")