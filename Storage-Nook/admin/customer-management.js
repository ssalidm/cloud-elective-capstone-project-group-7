document.getElementById('add-customer-btn').addEventListener('click', function() {
    const form = document.getElementById('add-customer-form');
    form.style.display = form.style.display === 'none' ? 'block' : 'none';
  });

  document.getElementById('add-customer-form').addEventListener('submit', function(event) {
    event.preventDefault();
  
    const name = document.getElementById('customer-name').value;
    const email = document.getElementById('email').value;
    const bookingHistory = document.getElementById('booking-history').value;
  
    // Mock customer data to append to the table )will replace with api when endpoint is available)
    const newCustomer = { name, email, bookingHistory };
  
    // Add the new customer to the table
    const newRow = document.createElement('tr');
    newRow.innerHTML = `
      <td>${newCustomer.name}</td>
      <td>${newCustomer.email}</td>
      <td>${newCustomer.bookingHistory}</td>
      <td>
        <button class="notify-btn">Notify</button>
        <button class="view-details-btn">View Details</button>
      </td>
    `;
  
    document.getElementById('customer-list').appendChild(newRow);
  
    // Clear and hide the form
    document.getElementById('add-customer-form').reset();
    document.getElementById('add-customer-form').style.display = 'none';
  });
  