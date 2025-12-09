import os

print("🔧 FIXING LOGIN PAGE HEADERS...")

# --- NEW LOGIN.HTML (With Headers Fix) ---
login_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - Supreme Delivery</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background: #f4f6f9; height: 100vh; display: flex; align-items: center; justify-content: center; font-family: 'Segoe UI', sans-serif; }
        .login-card { width: 400px; padding: 30px; background: white; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }
        .nav-pills .nav-link.active { background-color: #00B14F; }
        .nav-link { color: #333; cursor: pointer; }
        .btn-primary { background-color: #00B14F; border: none; }
        .btn-primary:hover { background-color: #009e46; }
    </style>
</head>
<body>

    <div class="login-card">
        <h3 class="text-center mb-4" style="color: #00B14F; font-weight: bold;">GRAB FOOD</h3>
        
        <ul class="nav nav-pills mb-4 justify-content-center">
            <li class="nav-item">
                <a class="nav-link active" onclick="setRole('customer', this)">Customer</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" onclick="setRole('restaurant', this)">Restaurant</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" onclick="setRole('driver', this)">Driver</a>
            </li>
        </ul>

        <div class="mb-3">
            <label>Username</label>
            <input type="text" id="username" class="form-control" placeholder="e.g. admin or user">
        </div>
        <div class="mb-3">
            <label>Password</label>
            <input type="password" id="password" class="form-control" placeholder="123">
        </div>
        
        <button onclick="login()" class="btn btn-primary w-100 py-2">Login</button>
        <p id="msg" class="text-center text-danger mt-3 small"></p>
        
        <div class="text-center mt-3">
            <small class="text-muted">Logging in as: <strong id="roleDisplay">customer</strong></small>
        </div>
    </div>

    <script>
        let currentRole = 'customer';

        function setRole(role, element) {
            currentRole = role;
            document.getElementById('roleDisplay').innerText = role;
            // Tabs visual update
            document.querySelectorAll('.nav-link').forEach(el => el.classList.remove('active'));
            element.classList.add('active');
        }

        async function login() {
            const u = document.getElementById('username').value;
            const p = document.getElementById('password').value;
            const msg = document.getElementById('msg');

            if(!u || !p) {
                msg.innerText = "Please fill all fields";
                return;
            }

            msg.innerText = "Connecting...";
            msg.style.color = "blue";

            try {
                // FIX IS HERE: Adding 'Content-Type': 'application/json'
                const res = await fetch('/auth/login', {
                    method: 'POST',
                    headers: { 
                        'Content-Type': 'application/json' 
                    },
                    body: JSON.stringify({ 
                        username: u, 
                        password: p, 
                        role: currentRole 
                    })
                });

                const data = await res.json();

                if (res.ok) {
                    msg.style.color = "green";
                    msg.innerText = "Success! Redirecting...";
                    setTimeout(() => {
                        window.location.href = data.redirect;
                    }, 1000);
                } else {
                    msg.style.color = "red";
                    msg.innerText = data.error || "Login Failed";
                }
            } catch (err) {
                msg.style.color = "red";
                msg.innerText = "Server Error: " + err.message;
            }
        }
    </script>
</body>
</html>
"""

# Ensure templates folder exists
if not os.path.exists('templates'):
    os.makedirs('templates')

with open("templates/login.html", "w", encoding="utf-8") as f:
    f.write(login_html)

print("✅ login.html FIXED. Headers added.")
"""

**Step 3: Save aur Run** 🚀
1.  Notepad **Save (`Ctrl+S`)** karein aur band kar dein.
2.  Terminal mein yeh commands chalayen:

```powershell
python fix_login_header.py
python app.py