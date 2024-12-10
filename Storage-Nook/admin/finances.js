document.addEventListener('DOMContentLoaded', () => {
  // Fetch and display financial overview
  fetchFinancialOverview();

  // Fetch and display transaction records
  fetchTransactions();

  // Fetch and display analytics data
  fetchAnalytics();
});

// Function to fetch financial overview
function fetchFinancialOverview() {
  fetch('https://4gt9bjtqq1.execute-api.eu-west-1.amazonaws.com/dev/finances/overview')
      .then(response => response.json())
      .then(data => {
          document.querySelector('.card:nth-child(1) p').textContent = `R${data.totalRevenue}`;
          document.querySelector('.card:nth-child(2) p').textContent = `R${data.totalExpenses}`;
          document.querySelector('.card:nth-child(3) p').textContent = `R${data.netProfit}`;
      })
      .catch(error => {
          console.error('Error fetching financial overview:', error);
          alert('Failed to load financial overview. Please try again later.');
      });
}

// Function to fetch transaction records
function fetchTransactions() {
  fetch('https://4gt9bjtqq1.execute-api.eu-west-1.amazonaws.com/dev/finances/transactions')
      .then(response => response.json())
      .then(data => {
          const tbody = document.querySelector('.transactions-table tbody');
          tbody.innerHTML = ''; // Clear existing rows

          data.transactions.forEach(transaction => {
              const row = document.createElement('tr');
              row.innerHTML = `
                  <td>${transaction.date}</td>
                  <td>${transaction.customerName}</td>
                  <td>${transaction.unit}</td>
                  <td>R${transaction.amount}</td>
                  <td>
                      <span>${transaction.status}</span>
                      <button class="update-status" data-id="${transaction.id}">Update</button>
                  </td>
              `;
              tbody.appendChild(row);
          });

          // Add event listeners for update buttons
          document.querySelectorAll('.update-status').forEach(button => {
              button.addEventListener('click', updatePaymentStatus);
          });
      })
      .catch(error => {
          console.error('Error fetching transactions:', error);
          alert('Failed to load transactions. Please try again later.');
      });
}

// Function to fetch analytics data
function fetchAnalytics() {
  const baseUrl = 'https://4gt9bjtqq1.execute-api.eu-west-1.amazonaws.com/dev`';  // Replace with the actual base URL
  const analyticsUrl = `${baseUrl}/admin/analytics`;  // Full endpoint URL
  const authToken = localStorage.getItem('accessToken', accessToken);

  fetch(analyticsUrl, {  // Use the full URL here
      method: 'GET',
      headers: {
          'Authorization': `Bearer ${authToken}`,  // Replace with the actual token
      }
  })
  .then(response => response.json())
  .then(data => {
      // Assuming the response contains analytics data that you want to display
      document.querySelector('.finance-summary').innerHTML += `
          <h3>Analytics Overview</h3>
          <div class="analytics-data">
              <p>Total Units Rented: ${data.totalUnitsRented}</p>
              <p>Top Customer: ${data.topCustomer}</p>
              <p>Revenue by Category: R${data.revenueByCategory}</p>
          </div>
      `;
  })
  .catch(error => {
      console.error('Error fetching analytics data:', error);
      alert('Failed to load analytics data. Please try again later.');
  });
}

// Function to update payment status
function updatePaymentStatus(event) {
  const transactionId = event.target.dataset.id;
  const newStatus = prompt('Enter new payment status (Paid/Overdue):');
  
  if (newStatus) {
      fetch(`https://4gt9bjtqq1.execute-api.eu-west-1.amazonaws.com/dev/finances/transactions/${transactionId}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ status: newStatus })
      })
      .then(response => response.json())
      .then(data => {
          if (data.success) {
              alert('Payment status updated successfully!');
              fetchTransactions(); // Refresh transaction table
          } else {
              alert('Failed to update payment status. Please try again.');
          }
      })
      .catch(error => {
          console.error('Error updating payment status:', error);
          alert('Failed to update payment status. Please try again.');
      });
  }
}
