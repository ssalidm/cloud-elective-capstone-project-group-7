const COGNITO_DOMAIN =
  "https://storagenookapp.auth.eu-west-1.amazoncognito.com";
const CLIENT_ID = "46h9jukegvt1lk4bp4v5p4p029";
const REDIRECT_URI = "http://localhost:8000";
const API_URL =
  "https://4gt9bjtqq1.execute-api.eu-west-1.amazonaws.com/dev/units";

const API_BASE_URL =
  "https://4gt9bjtqq1.execute-api.eu-west-1.amazonaws.com/dev";

// Redirect to Cognito Sign-In and Sign-Up
document.getElementById("signin-btn").onclick = () => {
  window.location.href = `https://storagenookapp.auth.eu-west-1.amazoncognito.com/login?client_id=${CLIENT_ID}&response_type=token&scope=email+openid&redirect_uri=${REDIRECT_URI}`;
};
document.getElementById("signup-btn").onclick = () => {
  window.location.href = `https://storagenookapp.auth.eu-west-1.amazoncognito.com/signup?client_id=${CLIENT_ID}&response_type=token&scope=email+openid&redirect_uri=${REDIRECT_URI}`;
};

// Fetch Facilities
async function fetchFacilities() {
  const location = document.getElementById("location-filter").value;
  const type = document.getElementById("type-filter").value;
  const status = document.getElementById("status-filter").value;

  let url = `${API_BASE_URL}/units`;
  let queryParams = [];
  if (location) queryParams.push(`location=${location}`);
  if (type) queryParams.push(`type=${type}`);
  if (status) queryParams.push(`status=${status}`);
  if (queryParams.length) url += `?${queryParams.join("&")}`;

  try {
    const response = await fetch(url);
    const data = await response.json();
    populateFacilitiesTable(data);
  } catch (err) {
    console.error("Error fetching facilities:", err);
  }
}

function populateFacilitiesTable(units) {
  const tableBody = document
    .getElementById("facilities-table")
    .querySelector("tbody");
  tableBody.innerHTML = "";
  units.forEach((unit) => {
    const row = `<tr>
              <td>${unit.unitId}</td>
              <td>${unit.typeId}</td>
              <td>${unit.location}</td>
              <td>${unit.size}</td>
              <td>${unit.status}</td>
              <td>${unit.pricing?.perMonth || "N/A"}</td>
          </tr>`;
    tableBody.innerHTML += row;
  });
}

// Fetch Financial Analytics
async function fetchAnalytics() {
  try {
    const response = await fetch(`${API_BASE_URL}/admin/analytics`);
    const analytics = await response.json();
    document.getElementById(
      "total-revenue"
    ).textContent = `$${analytics.totalRevenue}`;
    document.getElementById("number-of-bookings").textContent =
      analytics.numberOfBookings;
    document.getElementById("occupancy-percentage").textContent =
      analytics.occupancyPercentage.toFixed(2);
  } catch (err) {
    console.error("Error fetching analytics:", err);
  }
}

// Event Listeners for Filters
document.getElementById("location-filter").onchange = fetchFacilities;
document.getElementById("type-filter").onchange = fetchFacilities;
document.getElementById("status-filter").onchange = fetchFacilities;

// Initial Data Load
fetchFacilities();
fetchAnalytics();
