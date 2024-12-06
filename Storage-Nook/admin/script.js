document.getElementById('admin-login-form').addEventListener('submit', function (event) {
  event.preventDefault();


  const email = document.getElementById('admin-email').value;
  const password = document.getElementById('admin-password').value;

  // loading spinner
  const loadingSpinner = document.getElementById('loading-spinner');
  loadingSpinner.style.display = 'block';

  // Mock authentication 
  setTimeout(() => {  //mock api call
    if (email === 'admin@example.com' && password === 'password123') {
      alert('Login successful!');
      // Redirect to the admin dashboard 
      window.location.href = "dashboard.html";
    } else {
      // Hide the loading spinner
      loadingSpinner.style.display = 'none';
      
      // Display the error message in the div
      const errorMessage = document.getElementById('error-message');
      errorMessage.textContent = 'Invalid email or password!';
      errorMessage.style.display = 'block';
    }
  }, 1000); // Simulate a 1 second delay
});
