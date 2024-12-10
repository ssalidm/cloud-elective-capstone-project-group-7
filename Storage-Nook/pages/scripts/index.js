// Base URL of the API
const API_BASE_URL =
  "https://4gt9bjtqq1.execute-api.eu-west-1.amazonaws.com/dev";
const cognitoDomain =
  "https://storagenookapp.auth.eu-west-1.amazoncognito.com/";
const clientId = "46h9jukegvt1lk4bp4v5p4p029";
const redirectUri = "https://storage-nook-users.s3.eu-west-1.amazonaws.com/pages/dashboard.html";

// Check authentication status
function checkAuthStatus() {
  const urlParams = new URLSearchParams(window.location.hash.substring(1));
  const idToken = urlParams.get("id_token");

  if (idToken) {
    // Store token in localStorage for persistence
    localStorage.setItem("id_token", idToken);

    // Hide login and signup buttons
    document.getElementById("login-button").style.display = "none";
    document.getElementById("signup-button").style.display = "none";

    // Show logout button
    document.getElementById("logout-button").style.display = "inline";
  } else if (localStorage.getItem("id_token")) {
    // User is still logged in via localStorage
    document.getElementById("login-button").style.display = "none";
    document.getElementById("signup-button").style.display = "none";
    document.getElementById("logout-button").style.display = "inline";
  } else {
    // User is not authenticated
    document.getElementById("login-button").style.display = "inline";
    document.getElementById("signup-button").style.display = "inline";
    document.getElementById("logout-button").style.display = "none";
  }
}

// Redirect to Cognito UI for Login and Signup
document.getElementById("login-button").addEventListener("click", () => {
  const loginUrl = `https://storagenookapp.auth.eu-west-1.amazoncognito.com/login?client_id=${clientId}&response_type=token&scope=email+openid+profile&redirect_uri=${redirectUri}`;
  window.location.href = loginUrl;
});

// Redirect to Cognito UI for Signup
document.getElementById("signup-button").addEventListener("click", () => {
  const signupUrl = `${cognitoDomain}signup?client_id=${clientId}&response_type=token&scope=email+openid+profile&redirect_uri=${redirectUri}`;
  window.location.href = signupUrl;
});

// Logout functionality
document.getElementById("logout-button").addEventListener("click", () => {
  // Clear token from localStorage
  localStorage.removeItem("id_token");

  // Reload the page
  window.location.href = "/";
});

// Load Filters and Facilities on Page Load
window.onload = async () => {
  checkAuthStatus();
  await loadFilters();
  await loadFacilities();
};

// Load Filters Dynamically
async function loadFilters() {
  const locations = [
    { display: "Pretoria", value: "pta" },
    { display: "Cape Town", value: "cpt" },
    { display: "Johannesburg", value: "jhb" },
    { display: "Durban", value: "dbn" },
  ];
  const types = [
    { display: "Garage", value: "garage" },
    { display: "Locker", value: "locker" },
    { display: "Climate Controlled", value: "climate" },
    { display: "Warehouse", value: "warehouse" },
  ];
  const statuses = [
    { display: "Available", value: "Available" },
    { display: "Reserved", value: "Reserved" },
    { display: "Unavailable", value: "Unavailable" },
  ];

  populateDropdown("location-filter", locations);
  populateDropdown("type-filter", types);
  populateDropdown("status-filter", statuses);
}

// Populate Dropdowns
function populateDropdown(id, options) {
  const dropdown = document.getElementById(id);
  options.forEach((option) => {
    const optElement = document.createElement("option");
    optElement.value = option.value;
    optElement.textContent = option.display;
    dropdown.appendChild(optElement);
  });
}

// Load Facilities
async function loadFacilities(filters = {}) {
  try {
    let url = `${API_BASE_URL}/units`;
    const queryParams = new URLSearchParams(filters).toString();
    if (queryParams) url += `?${queryParams}`;

    const response = await fetch(url, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });
    const facilities = await response.json();

    renderFacilities(facilities);
  } catch (error) {
    console.error("Error loading facilities:", error);
  }
}

// Map statuses to FontAwesome icons
const statusIcons = {
  Available: '<i class="fas fa-check-circle" style="color: green;"></i> Available',
  Reserved: '<i class="fas fa-exclamation-circle" style="color: orange;"></i> Reserved',
  Unavailable: '<i class="fas fa-times-circle" style="color: red;"></i> Unavailable',
};

// Render Facilities Table
function renderFacilities(facilities) {
  const tableContainer = document.getElementById("facilities-table");
  tableContainer.innerHTML = `
        <table>
            <thead>
                <tr>
                    <th>Unit ID</th>
                    <th>Type</th>
                    <th>Location</th>
                    <th>Status</th>
                    <th>Price/Day</th>
                    <th>Price/Week</th>
                    <th>Price/Month</th>
                    <th>Price/Year</th>
                </tr>
            </thead>
            <tbody>
                ${facilities
                  .map(
                    (facility) => `
                        <tr>
                            <td>${facility.unitId.toUpperCase()}</td>
                            <td>${capitalize(facility.typeId)}</td>
                            <td>${convertLocation(facility.location)}</td>
                            <td>${statusIcons[facility.status] || facility.status}</td>
                            <td>R${facility.pricing.perDay || "N/A"}</td>
                            <td>R${facility.pricing.perWeek || "N/A"}</td>
                            <td>R${facility.pricing.perMonth || "N/A"}</td>
                            <td>R${facility.pricing.perYear || "N/A"}</td>
                        </tr>
                    `
                  )
                  .join("")}
            </tbody>
        </table>
    `;
}

// Convert location code to display name
function convertLocation(location) {
  const locationMapping = {
    pta: "Pretoria",
    cpt: "Cape Town",
    jhb: "Johannesburg",
    dbn: "Durban",
  };
  return locationMapping[location] || location;
}

// Capitalize typeId for display
function capitalize(text) {
  return text.charAt(0).toUpperCase() + text.slice(1);
}

// Filter Facilities
function filterFacilities() {
  const location = document.getElementById("location-filter").value;
  const type = document.getElementById("type-filter").value;
  const status = document.getElementById("status-filter").value;

  const filters = {};
  if (location) filters.location = location;
  if (type) filters.type = type;
  if (status) filters.status = status;

  loadFacilities(filters);
}
