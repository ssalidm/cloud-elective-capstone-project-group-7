document.getElementById('admin-login-form').addEventListener('submit', function (event) {
    event.preventDefault();
  
    // Get form values
    const email = document.getElementById('admin-email').value;
    const password = document.getElementById('admin-password').value;
  
    // Mock authentication (replace this with Cognito integration)
    if (email === 'admin@example.com' && password === 'password123') {
      alert('Login successful!');
      // Redirect to the admin dashboard (mock URL for now)
      window.location.href = "dashboard.html";
    } else {
      alert('Invalid email or password!');
    }
  });
  