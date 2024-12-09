const COGNITO_DOMAIN = "https://storagenookapp.auth.eu-west-1.amazoncognito.com";
const CLIENT_ID = "46h9jukegvt1lk4bp4v5p4p029";
const REDIRECT_URI = "http://localhost:8000";
const API_URL = "https://4gt9bjtqq1.execute-api.eu-west-1.amazonaws.com/dev/units";

// Redirect to Cognito Login Page
document.getElementById("login-button").addEventListener("click", () => {
  const loginUrl = `${COGNITO_DOMAIN}/login?client_id=${CLIENT_ID}&response_type=token&scope=email+openid+profile&redirect_uri=${REDIRECT_URI}`;
  window.location.href = loginUrl;
});

// Parse Token After Redirect
function parseAccessToken() {
  const hash = window.location.hash;
  if (!hash) return null;

  const params = new URLSearchParams(hash.substring(1));
  return params.get("id_token");
}

// Fetch Facilities
async function fetchFacilities(token) {
  try {
    const response = await fetch(API_URL, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      throw new Error("Failed to fetch facilities");
    }

    const facilities = await response.json();
    displayFacilities(facilities);
  } catch (err) {
    console.error(err);
  }
}

// Display Facilities on the Page
function displayFacilities(facilities) {
  document.getElementById("login-container").classList.add("hidden");
  document.getElementById("facilities").classList.remove("hidden");

  const list = document.getElementById("facilities-list");
  list.innerHTML = "";

  facilities.forEach((facility) => {
    const listItem = document.createElement("li");
    listItem.textContent = `${facility.typeId.toUpperCase()} - ${facility.unitId.toUpperCase()} - ${facility.location.toUpperCase()} - ${facility.size}`;
    list.appendChild(listItem);
  });
}

// Main Logic
document.addEventListener("DOMContentLoaded", () => {
  const token = parseAccessToken();
  if (token) {
    fetchFacilities(token);
  }
});
