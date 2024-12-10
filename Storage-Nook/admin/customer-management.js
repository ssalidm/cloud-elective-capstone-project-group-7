document.addEventListener('DOMContentLoaded', async () => {
  await fetchCustomerData(); // Fetch and display customer data on page load

  document.getElementById('add-customer-btn').addEventListener('click', function () {
    const form = document.getElementById('add-customer-form');
    form.style.display = form.style.display === 'none' ? 'block' : 'none';
  });

  document.getElementById('add-customer-form').addEventListener('submit', async function (event) {
    event.preventDefault();

    const name = document.getElementById('customer-name').value;
    const email = document.getElementById('email').value;
    const bookingHistory = document.getElementById('booking-history').value;

    // Call the API to add a new customer
    try {
      await addCustomer({ name, email, bookingHistory });
      await fetchCustomerData(); // Refresh customer list
      alert("Customer added successfully!");
    } catch (error) {
      console.error("Error adding customer:", error);
      alert("Failed to add customer. Please try again.");
    }

    // Clear and hide the form
    document.getElementById('add-customer-form').reset();
    document.getElementById('add-customer-form').style.display = 'none';
  });
});

// Fetch customer data from the API
async function fetchCustomerData() {
  try {
    // Mock the ID Token temporarily until the authorized user list is added
    const idToken = "mocked-valid-id-token"; // Replace with Cognito token function later

    const response = await fetch("https://4gt9bjtqq1.execute-api.eu-west-1.amazonaws.com/dev/user/profile", {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${idToken}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch customers: ${response.statusText}`);
    }

    const customers = await response.json();
    populateCustomerTable(customers);
  } catch (error) {
    console.error("Error fetching customer data:", error);
    alert("Failed to fetch customer data.");
  }
}

// Add a new customer using the API
async function addCustomer(customer) {
  const idToken = "mocked-valid-id-token"; // Replace with Cognito token function later

  const response = await fetch("https://4gt9bjtqq1.execute-api.eu-west-1.amazonaws.com/dev/user/profile", {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${idToken}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(customer),
  });

  if (!response.ok) {
    throw new Error(`Failed to add customer: ${response.statusText}`);
  }
}

// Populate the customer table
function populateCustomerTable(customers) {
  const customerList = document.getElementById('customer-list');
  customerList.innerHTML = ''; // Clear existing rows

  customers.forEach((customer) => {
    const newRow = document.createElement('tr');
    newRow.innerHTML = `
      <td>${customer.name || 'N/A'}</td>
      <td>${customer.email || 'N/A'}</td>
      <td>${customer.bookingHistory || 'N/A'}</td>
      <td>
        <button class="notify-btn">Notify</button>
        <button class="view-details-btn">View Details</button>
      </td>
    `;
    customerList.appendChild(newRow);
  });
}
