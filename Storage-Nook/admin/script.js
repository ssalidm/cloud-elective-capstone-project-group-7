// Cognito URLs
const cognitoDomain = "https://storagenookapp.auth.eu-west-1.amazoncognito.com";
const clientId = "46h9jukegvt1lk4bp4v5p4p029"; 
const redirectUri = "https://your-production-url/callback"; // Replace with your actual callback URL
const responseType = "token"; 
const scope = "openid email profile"; 

// Attach event listeners to buttons
document.getElementById('login-button').addEventListener('click', () => {
  const loginUrl = `${cognitoDomain}/login?client_id=${clientId}&redirect_uri=${encodeURIComponent(redirectUri)}&response_type=${responseType}&scope=${encodeURIComponent(scope)}`;
  window.location.href = loginUrl;
});

document.getElementById('signup-button').addEventListener('click', () => {
  const signupUrl = `${cognitoDomain}/signup?client_id=${clientId}&redirect_uri=${encodeURIComponent(redirectUri)}&response_type=${responseType}&scope=${encodeURIComponent(scope)}`;
  window.location.href = signupUrl;
});
