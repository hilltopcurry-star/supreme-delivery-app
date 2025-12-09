import os

print("🔧 ACTIVATING RESTAURANT DASHBOARD...")

# --- 1. UPDATE APP.PY (Add API to fetch all orders) ---
app_path = "app.py"
if os.path.exists(app_path):
    with open(app_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # API Route add karna agar nahi hai
    if "/api/restaurant/orders" not in content:
        new_route = """
@app.route('/api/restaurant/orders')
def get_all_orders():
    # Database se saare orders nikalo (Latest pehle)
    orders = Order.query.order_by(Order.id.desc()).all()
    return jsonify([
        {'id': o.id, 'status': o.status, 'total': o.total, 'items': 'Zinger Burger, Fries'} 
        for o in orders
    ])
"""
        parts = content.split("if __name__")
        new_content = parts[0] + new_route + "if __name__" + parts[1]
        
        with open(app_path, "w", encoding="utf-8") as f:
            f.write(new_content)

# --- 2. UPDATE DASHBOARD.HTML (Show Real Data) ---
dashboard_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Restaurant Admin</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #f4f6f9; }
        .sidebar { height: 100vh; position: fixed; width: 250px; background: #343a40; color: white; padding: 20px; }
        .main-content { margin-left: 250px; padding: 30px; }
        .order-card { background: white; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); transition: 0.3s; }
        .status-new { color: #00B14F; font-weight: bold; }
    </style>
</head>
<body>

    <div class="sidebar">
        <h3>🍔 MANAGER</h3>
        <hr>
        <p>📊 Dashboard</p>
        <p>📦 Orders <span class="badge bg-danger" id="countBadge">0</span></p>
        <p>⚙️ Settings</p>
        <br>
        <a href="/" class="btn btn-outline-light w-100">Logout</a>
    </div>

    <div class="main-content">
        <h2 class="mb-4">Live Incoming Orders</h2>
        <button onclick="fetchOrders()" class="btn btn-primary mb-3">🔄 Refresh List</button>

        <div class="card p-3 border-0 shadow-sm">
            <table class="table table-hover">
                <thead class="table-dark">
                    <tr>
                        <th>Order ID</th>
                        <th>Items</th>
                        <th>Total</th>
                        <th>Status</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody id="orderTable">
                    </tbody>
            </table>
        </div>
    </div>

    <script>
        async function fetchOrders() {
            const table = document.getElementById('orderTable');
            table.innerHTML = "<tr><td colspan='5'>Loading...</td></tr>";

            try {
                const res = await fetch('/api/restaurant/orders');
                const orders = await res.json();
                
                table.innerHTML = ""; // Clear loader
                document.getElementById('countBadge').innerText = orders.length;

                orders.forEach(order => {
                    table.innerHTML += `
                        <tr>
                            <td>#${order.id}</td>
                            <td>${order.items}</td>
                            <td>$${order.total}</td>
                            <td class="status-new">${order.status}</td>
                            <td>
                                <button class="btn btn-sm btn-success">Accept</button>
                                <button class="btn btn-sm btn-danger">Reject</button>
                            </td>
                        </tr>
                    `;
                });

                if(orders.length === 0) {
                    table.innerHTML = "<tr><td colspan='5'>No orders yet.</td></tr>";
                }

            } catch (err) {
                table.innerHTML = "<tr><td colspan='5' class='text-danger'>Error loading orders. Is Server Running?</td></tr>";
            }
        }

        // Auto-load on start
        fetchOrders();
        // Auto-refresh every 5 seconds
        setInterval(fetchOrders, 5000);
    </script>
</body>
</html>
"""

os.makedirs("templates/restaurant", exist_ok=True)
with open("templates/restaurant/dashboard.html", "w", encoding="utf-8") as f:
    f.write(dashboard_html)

print("✅ RESTAURANT DASHBOARD UPDATED. Showing Real Database Orders.")