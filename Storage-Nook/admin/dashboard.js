document.addEventListener('DOMContentLoaded', () => {
  // Check if the access token is in the URL (from Cognito redirect)
  const accessToken = parseAccessToken();
  if (accessToken) {
    // Store the access token in localStorage for later use
    localStorage.setItem('accessToken', accessToken);
    console.log('Access token stored successfully:', accessToken);
  }

  fetchDashboardData();

  const refreshButton = document.getElementById('refresh-dashboard');
  if (refreshButton) {
    refreshButton.addEventListener('click', fetchDashboardData);
  }
});

function parseAccessToken() {
  const hash = window.location.hash;
  if (!hash) {
    return null;
  }
  const params = new URLSearchParams(hash.substring(1));
  return params.get('access_token');
}

async function fetchDashboardData() {
  try {
    // Get the actual access token from localStorage
    const accessToken = localStorage.getItem('accessToken');
    if (!accessToken) {
      alert("User is not authenticated.");
      return;
    }

    // fetch data from the actual API endpoint
    const response = await fetch("https://4gt9bjtqq1.execute-api.eu-west-1.amazonaws.com/dev/admin/analytics", {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${accessToken}`,  // Use the access token in the Authorization header
        'Content-Type': 'application/json'
      }
    });

    // If API returns an error, handle it
    if (response.status === 401) {
      alert("You are not authorized to view this data.");
      return;  // Stop the function if not authorized
    } else if (!response.ok) {
      alert(`Error fetching data: ${response.statusText}`);
      return;  // Stop the function if there's an error
    }

    const data = await response.json();

    // Process the data to calculate revenue, bookings, and occupancy
    const revenue = calculateRevenue(data);
    const bookings = data.length; 
    const occupancy = calculateOccupancy(data);

    // Update the dashboard tiles with real data
    updateDashboard({ revenue, bookings, occupancy });

  } catch (error) {
    console.error("Error fetching dashboard data:", error);

    // Use mock data in case of an error
    alert("An error occurred while fetching the data, using mock data.");

    // Mock data for testing purposes
    const mockData = [
      { rent: 100, status: "Occupied" },
      { rent: 200, status: "Available" },
      { rent: 150, status: "Occupied" }
    ];

    // Process mock data
    const revenue = calculateRevenue(mockData);
    const bookings = mockData.length; // Assuming each unit in the response is a booking
    const occupancy = calculateOccupancy(mockData);

    // Update the dashboard tiles with mock data
    updateDashboard({ revenue, bookings, occupancy });
  }
}

function calculateRevenue(data) {
  // Calculate the total revenue by summing up the rent values
  return `R${data.reduce((total, unit) => total + (unit.rent || 0), 0)}`;
}

function calculateOccupancy(data) {
  // Calculate the percentage of occupied units
  const totalUnits = data.length;
  const occupiedUnits = data.filter(unit => unit.status === "Occupied").length;
  return totalUnits ? `${((occupiedUnits / totalUnits) * 100).toFixed(2)}%` : "0%";
}

function updateDashboard({ revenue, bookings, occupancy }) {
  // Update the DOM with the mock data or real data values
  document.querySelector('.tile:nth-child(1) p').textContent = revenue;
  document.querySelector('.tile:nth-child(2) p').textContent = bookings;
  document.querySelector('.tile:nth-child(3) p').textContent = occupancy;
}

const refreshButton = document.getElementById('refresh-dashboard');
if (refreshButton) {
  refreshButton.addEventListener('click', fetchDashboardData);
}
