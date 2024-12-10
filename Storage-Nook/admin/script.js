// Cognito URLs
const cognitoDomain = "https://storagenookapp.auth.eu-west-1.amazoncognito.com/";
const clientId = "46h9jukegvt1lk4bp4v5p4p029"; 
// const redirectUri = "https://storage-nook-admin.s3.eu-west-1.amazonaws.com/admin/dashboard.html"; // Replace with your actual callback URL
const redirectUri = "http://localhost:8000"; // Replace with your actual callback URL

const responseType = "token"; 
const scope = "openid email profile"; 
-
function parseAccessToken() {
    const hash = window.location.hash;
    if (!hash) return null;
    const params = new URLSearchParams(hash.substring(1));
    return params.get('access_token');
  }
  
  document.addEventListener('DOMContentLoaded', () => { ;
    const loginButton = document.getElementById('login-button');
    if (loginButton) {
        loginButton.addEventListener('click', () => {
            const loginUrl = `https://storagenookapp.auth.eu-west-1.amazoncognito.com/login?client_id=46h9jukegvt1lk4bp4v5p4p029&response_type=token&scope=email+openid+profile&redirect_uri=https://storage-nook-admin.s3.eu-west-1.amazonaws.com/admin/dashboard.html`;
            window.location.href = loginUrl;
        });
    } else {
        console.error('Login button not found');
    }
  
    const signupButton = document.getElementById('signup-button');
    if (signupButton) {
        signupButton.addEventListener('click', () => {
            const signupUrl = `${cognitoDomain}/signup?client_id=${clientId}&redirect_uri=${encodeURIComponent(redirectUri)}&response_type=${responseType}&scope=${encodeURIComponent(scope)}`;
            window.location.href = signupUrl;
        });
    } else {
        console.error('Signup button not found');
    }
  
    // Parse access token after redirect
    const accessToken = parseAccessToken();
    if (accessToken) {
        // Store the access token or use it immediately
        localStorage.setItem('accessToken', accessToken);
        // Make API calls using the access token
        // ... (your API call logic here)
    }
  });