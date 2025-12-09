import os

print("🔧 ACTIVATING SUPER ADMIN (PLATFORM OWNER)...")

# --- 1. SUPER ADMIN DASHBOARD HTML ---
super_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Platform Owner | Supreme Delivery</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #1a1a2e; color: white; font-family: 'Segoe UI', sans-serif; }
        .sidebar { height: 100vh; position: fixed; width: 260px; background: #16213e; padding: 20px; border-right: 1px solid #0f3460; }
        .main-content { margin-left: 260px; padding: 30px; }
        .card { background: #0f3460; border: none; color: white; margin-bottom: 20px; }
        .btn-add { background: #e94560; color: white; border: none; }
        .table { color: white; }
    </style>
</head>
<body>

    <div class="sidebar">
        <h3 style="color:#e94560;">👑 OWNER</h3>
        <hr>
        <p>📊 Platform Stats</p>
        <p>🏢 Manage Restaurants</p>
        <p>🚴 Manage Drivers</p>
        <p>💰 Commission</p>
        <br>
        <a href="/" class="btn btn-outline-light w-100">Logout</a>
    </div>

    <div class="main-content">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2>Registered Restaurants</h2>
            <button class="btn btn-add px-4" onclick="addRestaurant()">+ Add New Restaurant</button>
        </div>

        <div class="row">
            <div class="col-md-4"><div class="card p-3"><h3>12</h3><small>Total Restaurants</small></div></div>
            <div class="col-md-4"><div class="card p-3"><h3>$54,000</h3><small>Total Platform Revenue</small></div></div>
            <div class="col-md-4"><div class="card p-3"><h3>1,200</h3><small>Total Users</small></div></div>
        </div>

        <div class="card p-3 mt-4">
            <table class="table table-dark table-hover">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Restaurant Name</th>
                        <th>Owner</th>
                        <th>Status</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody id="resTable">
                    </tbody>
            </table>
        </div>
    </div>

    <script>
        // Mock Data for Demo
        const restaurants = [
            {id: 1, name: "Burger King Supreme", owner: "admin", status: "Active"},
            {id: 2, name: "Pizza Hut Pro", owner: "manager_ali", status: "Active"},
            {id: 3, name: "Sushi Master", owner: "sushi_chef", status: "Paused"}
        ];

        function renderTable() {
            const tbody = document.getElementById('resTable');
            tbody.innerHTML = "";
            restaurants.forEach(r => {
                tbody.innerHTML += `
                    <tr>
                        <td>#${r.id}</td>
                        <td>${r.name}</td>
                        <td>${r.owner}</td>
                        <td><span class="badge ${r.status === 'Active' ? 'bg-success' : 'bg-warning'}">${r.status}</span></td>
                        <td>
                            <button class="btn btn-sm btn-info" onclick="alert('Viewing Details')">View</button>
                            <button class="btn btn-sm btn-danger" onclick="deleteRes(${r.id})">Remove</button>
                        </td>
                    </tr>
                `;
            });
        }

        function addRestaurant() {
            const name = prompt("Enter New Restaurant Name:");
            if(name) {
                restaurants.push({id: restaurants.length + 1, name: name, owner: "new_owner", status: "Active"});
                renderTable();
            }
        }

        function deleteRes(id) {
            if(confirm("Are you sure you want to remove this restaurant?")) {
                alert("Restaurant Removed!");
                // In real app, call API DELETE
            }
        }

        renderTable();
    </script>
</body>
</html>
"""

os.makedirs("templates/admin", exist_ok=True)
with open("templates/admin/super_dashboard.html", "w", encoding="utf-8") as f:
    f.write(super_html)

# --- 2. UPDATE APP.PY (Add Super Admin Logic) ---
app_path = "app.py"
with open(app_path, "r", encoding="utf-8") as f:
    content = f.read()

# Add Super Admin Route
if "/admin/super" not in content:
    new_route = """
@app.route('/admin/super')
def super_admin_dashboard():
    return render_template('admin/super_dashboard.html')
"""
    # Login Logic Update for 'owner'
    login_fix = """
    if username == "owner":
        role = "super_admin"
        redirect_url = "/admin/super"
    elif username == "admin": 
"""
    
    # Inject Route
    parts = content.split("if __name__")
    temp_content = parts[0] + new_route + "if __name__" + parts[1]
    
    # Inject Login Logic
    if 'if username == "admin":' in temp_content:
        temp_content = temp_content.replace('if username == "admin":', login_fix)
        
    with open(app_path, "w", encoding="utf-8") as f:
        f.write(temp_content)

print("✅ SUPER ADMIN DASHBOARD ACTIVATED.")
print("👉 Login as: owner / 123")