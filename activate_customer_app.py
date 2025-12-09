import os

print("🔧 ACTIVATING CUSTOMER INTERACTIONS...")

# --- 1. UPDATED HOME.HTML (Clickable Restaurants) ---
home_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Supreme Food</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body { background-color: #f8f9fa; font-family: 'Segoe UI', sans-serif; }
        .hero { background: linear-gradient(135deg, #00B14F 0%, #008c3e 100%); padding: 60px 0; color: white; border-radius: 0 0 30px 30px; }
        .search-bar { border-radius: 30px; padding: 15px 25px; border: none; box-shadow: 0 5px 15px rgba(0,0,0,0.1); width: 100%; }
        .cat-badge { background: white; color: #333; padding: 10px 20px; border-radius: 20px; margin-right: 10px; cursor: pointer; transition: 0.3s; border: 1px solid #eee; }
        .cat-badge:hover, .cat-badge.active { background: #00B14F; color: white; border-color: #00B14F; }
        .res-card { border: none; border-radius: 15px; overflow: hidden; transition: 0.3s; cursor: pointer; background: white; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
        .res-card:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.1); }
        .res-img { height: 180px; background-color: #ddd; display: flex; align-items: center; justify-content: center; color: #777; font-size: 30px; }
    </style>
</head>
<body>

    <div class="hero text-center">
        <h1 class="mb-3 fw-bold">Find Your Favorite Food</h1>
        <div class="container" style="max-width: 600px;">
            <input type="text" class="search-bar" placeholder="Search pizza, burger, biryani...">
        </div>
    </div>

    <div class="container mt-5">
        <div class="d-flex overflow-auto mb-4 pb-2">
            <span class="cat-badge active">All</span>
            <span class="cat-badge">🍔 Burger</span>
            <span class="cat-badge">🍕 Pizza</span>
            <span class="cat-badge">🍣 Sushi</span>
            <span class="cat-badge">🍛 Desi</span>
        </div>

        <h4 class="mb-4 fw-bold">Featured Restaurants</h4>
        <div class="row g-4">
            <div class="col-md-4" onclick="window.location.href='/customer/menu'">
                <div class="res-card">
                    <div class="res-img"><i class="fas fa-hamburger"></i></div>
                    <div class="p-3">
                        <div class="d-flex justify-content-between">
                            <h5 class="fw-bold m-0">Burger King Supreme</h5>
                            <span class="badge bg-warning text-dark">4.8 <i class="fas fa-star"></i></span>
                        </div>
                        <p class="text-muted small mt-1">American • Fast Food • 20-30 min</p>
                    </div>
                </div>
            </div>

            <div class="col-md-4" onclick="window.location.href='/customer/menu'">
                <div class="res-card">
                    <div class="res-img" style="background:#ffecec; color:#ff5e57;"><i class="fas fa-pizza-slice"></i></div>
                    <div class="p-3">
                        <div class="d-flex justify-content-between">
                            <h5 class="fw-bold m-0">Pizza Hut Pro</h5>
                            <span class="badge bg-warning text-dark">4.5 <i class="fas fa-star"></i></span>
                        </div>
                        <p class="text-muted small mt-1">Italian • Pizza • 30-40 min</p>
                    </div>
                </div>
            </div>

            <div class="col-md-4" onclick="window.location.href='/customer/menu'">
                <div class="res-card">
                    <div class="res-img" style="background:#e8f8ff; color:#0fbcf9;"><i class="fas fa-fish"></i></div>
                    <div class="p-3">
                        <div class="d-flex justify-content-between">
                            <h5 class="fw-bold m-0">Sushi Master</h5>
                            <span class="badge bg-warning text-dark">4.9 <i class="fas fa-star"></i></span>
                        </div>
                        <p class="text-muted small mt-1">Japanese • Sushi • 15-25 min</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

</body>
</html>
"""

# --- 2. UPDATED MENU.HTML (Add to Cart Logic) ---
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

    <div class="container mt-4">
        <h6 class="text-muted mb-3">POPULAR ITEMS</h6>

        <div class="item-card">
            <div>
                <h6 class="fw-bold m-0">Zinger Burger</h6>
                <p class="text-muted small m-0">Spicy crispy chicken with cheese.</p>
                <div class="mt-2 fw-bold">$5.50</div>
            </div>
            <button class="btn btn-outline-success btn-sm" onclick="addToCart(5.50)">ADD</button>
        </div>

        <div class="item-card">
            <div>
                <h6 class="fw-bold m-0">Beef Whopper</h6>
                <p class="text-muted small m-0">Double patty with extra sauce.</p>
                <div class="mt-2 fw-bold">$8.00</div>
            </div>
            <button class="btn btn-outline-success btn-sm" onclick="addToCart(8.00)">ADD</button>
        </div>

         <div class="item-card">
            <div>
                <h6 class="fw-bold m-0">Large Fries</h6>
                <p class="text-muted small m-0">Crispy salted fries.</p>
                <div class="mt-2 fw-bold">$3.00</div>
            </div>
            <button class="btn btn-outline-success btn-sm" onclick="addToCart(3.00)">ADD</button>
        </div>
    </div>

    <div class="cart-bar" id="cartBar" onclick="alert('Order Placed Successfully! (Demo)')">
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

# Save Templates
os.makedirs("templates/customer", exist_ok=True)
with open("templates/customer/home.html", "w", encoding="utf-8") as f:
    f.write(home_html)

with open("templates/customer/menu.html", "w", encoding="utf-8") as f:
    f.write(menu_html)


# --- 3. UPDATE APP.PY (Ensure Routes Exist) ---
app_path = "app.py"
if os.path.exists(app_path):
    with open(app_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Agar Menu Route nahi hai to add kar do
    if "/customer/menu" not in content:
        new_route = """
@app.route('/customer/menu')
def customer_menu():
    return render_template('customer/menu.html')
"""
        # Insert before main run
        parts = content.split("if __name__")
        new_content = parts[0] + new_route + "if __name__" + parts[1]
        
        with open(app_path, "w", encoding="utf-8") as f:
            f.write(new_content)
            
print("✅ CUSTOMER APP ACTIVATED. Menu links are now working.")