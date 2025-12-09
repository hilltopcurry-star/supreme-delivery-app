import os

print("🔧 ACTIVATING ACCEPT/REJECT BUTTONS...")

# --- 1. UPDATE APP.PY (Add Status Update API) ---
app_path = "app.py"
if os.path.exists(app_path):
    with open(app_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Agar status update ka route nahi hai to add karo
    if "/api/orders/update" not in content:
        new_route = """
@app.route('/api/orders/update', methods=['POST'])
def update_order():
    try:
        data = request.get_json()
        order_id = data.get('order_id')
        new_status = data.get('status')
        
        order = Order.query.get(order_id)
        if order:
            order.status = new_status
            db.session.commit()
            return jsonify({"success": True, "new_status": new_status})
        return jsonify({"error": "Order not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
"""
        parts = content.split("if __name__")
        new_content = parts[0] + new_route + "if __name__" + parts[1]
        
        with open(app_path, "w", encoding="utf-8") as f:
            f.write(new_content)

# --- 2. UPDATE DASHBOARD.HTML (Button Click Logic) ---
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
        .status-badge { padding: 5px 10px; border-radius: 15px; font-weight: bold; font-size: 0.9em; }
        .status-Preparing { background-color: #ffeeba; color: #856404; }
        .status-Ready { background-color: #d4edda; color: #155724; }
        .status-Rejected { background-color: #f8d7da; color: #721c24; }
    </style>
</head>
<body>

    <div class="sidebar">
        <h3>🍔 MANAGER</h3>
        <hr>
        <p>📊 Dashboard</p>
        <p>📦 Orders <span class="badge bg-danger" id="countBadge">0</span></p>
        <a href="/" class="btn btn-outline-light w-100 mt-5">Logout</a>
    </div>

    <div class="main-content">
        <h2 class="mb-4">Live Incoming Orders</h2>
        <button onclick="fetchOrders()" class="btn btn-primary mb-3">🔄 Refresh List</button>

        <div class="card p-3 border-0 shadow-sm">
            <table class="table table-hover align-middle">
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
        async function updateStatus(id, status) {
            if(!confirm("Mark Order #" + id + " as " + status + "?")) return;

            await fetch('/api/orders/update', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({order_id: id, status: status})
            });
            fetchOrders(); // Refresh table
        }

        async function fetchOrders() {
            const res = await fetch('/api/restaurant/orders');
            const orders = await res.json();
            
            const table = document.getElementById('orderTable');
            table.innerHTML = "";
            document.getElementById('countBadge').innerText = orders.length;

            orders.forEach(order => {
                let actionButtons = "";
                
                // Sirf agar Preparing hai tabhi buttons dikhao
                if(order.status === 'Preparing' || order.status === 'Pending') {
                    actionButtons = `
                        <button class="btn btn-sm btn-success me-2" onclick="updateStatus(${order.id}, 'Ready')">Accept</button>
                        <button class="btn btn-sm btn-danger" onclick="updateStatus(${order.id}, 'Rejected')">Reject</button>
                    `;
                } else {
                    actionButtons = `<span class="text-muted">Completed</span>`;
                }

                table.innerHTML += `
                    <tr>
                        <td>#${order.id}</td>
                        <td>${order.items}</td>
                        <td>$${order.total}</td>
                        <td><span class="status-badge status-${order.status}">${order.status}</span></td>
                        <td>${actionButtons}</td>
                    </tr>
                `;
            });
        }

        fetchOrders();
        setInterval(fetchOrders, 5000);
    </script>
</body>
</html>
"""

with open("templates/restaurant/dashboard.html", "w", encoding="utf-8") as f:
    f.write(dashboard_html)

print("✅ BUTTONS ACTIVATED. Orders can now be Accepted/Rejected.")