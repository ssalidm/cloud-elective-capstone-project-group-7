document.getElementById('admin-login-form').addEventListener('submit', function (event) {
  event.preventDefault();

  // Get form values
  const email = document.getElementById('admin-email').value;
  const password = document.getElementById('admin-password').value;

  // Mock authentication 
  if (email === 'admin@example.com' && password === 'password123') {
    alert('Login successful!');
    // Redirect to the admin dashboard 
    window.location.href = "dashboard.html";
  } else {
    // Display the error message in the div
    const errorMessage = document.getElementById('error-message');
    errorMessage.textContent = 'Invalid email or password!';
    errorMessage.style.display = 'block';
  }
});
