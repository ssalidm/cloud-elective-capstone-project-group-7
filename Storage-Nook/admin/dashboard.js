document.addEventListener('DOMContentLoaded', () => {
    fetchDashboardData();
  });
  
  function fetchDashboardData() {
    // Mock API call 
    setTimeout(() => {
      const mockData = {
        revenue: 'R15,000',
        bookings: 120,
        occupancy: '85%'
      };
  
      updateDashboard(mockData);
    }, 1000); // Simulates a network delay
  }
  
  function updateDashboard(data) {
    document.querySelector('.tile:nth-child(1) p').textContent = data.revenue;
    document.querySelector('.tile:nth-child(2) p').textContent = data.bookings;
    document.querySelector('.tile:nth-child(3) p').textContent = data.occupancy;
  }
  
  const refreshButton = document.getElementById('refresh-dashboard');
  if (refreshButton) {
    refreshButton.addEventListener('click', fetchDashboardData);
  }
  