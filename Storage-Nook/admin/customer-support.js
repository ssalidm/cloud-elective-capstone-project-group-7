document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('search');
    const searchButton = document.querySelector('.search-btn');
    const tableBody = document.querySelector('tbody');
  
    // Mock data (replace with an API call to fetch real data)
    const supportRequests = [
      { unitId: 'U001', customerName: 'John Doe', status: 'Reserved' },
      { unitId: 'U002', customerName: 'Jane Smith', status: 'Unavailable' },
    ];
  
    // Populate table
    function populateTable(data) {
      tableBody.innerHTML = ''; // Clear existing rows
      data.forEach((request) => {
        const row = document.createElement('tr');
        row.innerHTML = `
          <td>${request.unitId}</td>
          <td>${request.customerName}</td>
          <td>${request.status}</td>
          <td>
            <button class="resolve-btn" data-unit-id="${request.unitId}">Resolve Issue</button>
          </td>
        `;
        tableBody.appendChild(row);
      });
  
      // Add event listeners to resolve buttons
      document.querySelectorAll('.resolve-btn').forEach((btn) => {
        btn.addEventListener('click', resolveIssue);
      });
    }
  
    // Search functionality
    searchButton.addEventListener('click', () => {
      const query = searchInput.value.toLowerCase();
      const filteredData = supportRequests.filter(
        (request) =>
          request.unitId.toLowerCase().includes(query) ||
          request.customerName.toLowerCase().includes(query)
      );
      populateTable(filteredData);
    });
  
    // Resolve issue functionality
    function resolveIssue(event) {
      const unitId = event.target.getAttribute('data-unit-id');
      const request = supportRequests.find((req) => req.unitId === unitId);
      if (request) {
        request.status = 'Resolved';
        alert(`Issue for Unit ID: ${unitId} resolved.`);
        populateTable(supportRequests);
      }
    }
  
    // Initial population
    populateTable(supportRequests);
  });
  