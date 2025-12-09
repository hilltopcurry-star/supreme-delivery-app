import os

print("🔧 ACTIVATING REAL ORDER SYSTEM...")

# --- 1. UPDATE CART.HTML (Connect to API) ---
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
        <button id="orderBtn" class="btn btn-success w-100 py-3 fw-bold" onclick="placeRealOrder()">PLACE ORDER ($8.50)</button>
        <p id="msg" class="text-center mt-2 small"></p>
    </div>

    <script>
        async function placeRealOrder() {
            const btn = document.getElementById('orderBtn');
            const msg = document.getElementById('msg');
            
            btn.disabled = true;
            btn.innerText = "Processing...";

            try {
                // Asli API Call
                const res = await fetch('/api/orders', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        items: [{name: 'Zinger', price: 5.50}, {name: 'Fries', price: 3.00}],
                        total: 8.50 
                    })
                });

                const data = await res.json();

                if (res.ok) {
                    msg.innerText = "Order #" + data.order_id + " Placed! Redirecting...";
                    msg.style.color = "green";
                    setTimeout(() => {
                        window.location.href = "/customer/home";
                    }, 2000);
                } else {
                    msg.innerText = "Failed: " + data.error;
                    msg.style.color = "red";
                    btn.disabled = false;
                }
            } catch (err) {
                msg.innerText = "Server Error";
                btn.disabled = false;
            }
        }
    </script>
</body>
</html>
"""

# Save Cart Template
with open("templates/customer/cart.html", "w", encoding="utf-8") as f:
    f.write(cart_html)


# --- 2. UPDATE APP.PY (Add API Endpoint) ---
app_path = "app.py"
if os.path.exists(app_path):
    with open(app_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Agar API route nahi hai to add karo
    if "/api/orders" not in content:
        new_route = """
@app.route('/api/orders', methods=['POST'])
def place_order():
    try:
        data = request.get_json()
        # Database mein save karein
        new_order = Order(status="Preparing", total=data.get('total', 0.0))
        db.session.add(new_order)
        db.session.commit()
        
        # Real-time alert (Console only for now)
        print(f"🔔 NEW ORDER #{new_order.id} RECEIVED: ${new_order.total}")
        
        return jsonify({"status": "success", "order_id": new_order.id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
"""
        parts = content.split("if __name__")
        new_content = parts[0] + new_route + "if __name__" + parts[1]
        
        with open(app_path, "w", encoding="utf-8") as f:
            f.write(new_content)

print("✅ REAL ORDERING SYSTEM ACTIVATED.")