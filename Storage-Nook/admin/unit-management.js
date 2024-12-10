// Function to show/hide the "Add Unit" form
document.getElementById('add-unit-btn').addEventListener('click', function() {
  const form = document.getElementById('add-unit-form');
  form.style.display = form.style.display === 'none' ? 'block' : 'none';
});

// Function to handle adding a new unit to the table and API
document.getElementById('unit-form').addEventListener('submit', function(event) {
  event.preventDefault();
  const address = document.getElementById('address').value;
  const size = document.getElementById('size').value ;
  const status= document.getElementById('status').value ;
  const location = document.getElementById('location').value ;
  const ppd = document.getElementById('price-per-day').value ;
  const ppw = document.getElementById('price-per-week').value ;
  const ppm= document.getElementById('price-per-month').value ;
  const ppy = document.getElementById('price-per-year').value ;



  // Prepare data for API
  const unitData = {
      address: address,
      status: status,
      location : location,
      size : size,
      pricing :{
        perYear: ppy,
        perMonth: ppm,
        perWeek: ppw,
        perDay: ppd 

      }
    
      
  }

  // Make API call to add a new unit
  fetch('https://4gt9bjtqq1.execute-api.eu-west-1.amazonaws.com/dev/storage-type/locker/units', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify(unitData)
  })
  .then(response => response.json())
  .then(data => {
      console.log("API response:", data); // Log the response for debugging

      // Check if the unit was successfully added
      if (data && data.unitId) {
          // Create a new row for the unit
          const newRow = document.createElement('tr');
          newRow.innerHTML = `
              <td> ${data.unitId}</td>
              <td>${data.status}</td>
              <td>${data.price}</td>
              <td>
                  <button>Edit</button>
                  <button>Remove</button>
              </td>
          `;

          // Append the new row to the table
          document.getElementById('unit-list').appendChild(newRow);

          // Clear the form and hide it
          document.getElementById('address').value = '';
          document.getElementById('size').value = '';
          document.getElementById('status').value = '';
          document.getElementById('location').value = '';
          document.getElementById('price-per-day').value = '';
          document.getElementById('price-per-week').value = '';
          document.getElementById('price-per-month').value = '';
          document.getElementById('price-per-year').value = '';


          document.getElementById('add-unit-form').style.display = 'none';
      } else {
          alert("Failed to add unit. Please try again.");
      }
  })
  .catch(error => {
      console.error("Error adding unit:", error); // Log the error for debugging
      alert("Error adding unit. Please try again.");
  });
});


// Edit Unit functionality
document.getElementById('unit-list').addEventListener('click', function(event) {
  if (event.target && event.target.classList.contains('edit-btn')) {
    const row = event.target.closest('tr');
    const unitId = row.cells[0].textContent;
    const status = row.cells[1].textContent;
    const price = row.cells[2].textContent;

    document.getElementById('unit-id').value = unitId;
    document.getElementById('status').value = status;
    document.getElementById('price').value = price;

    document.getElementById('unit-form').onsubmit = function(event) {
      event.preventDefault();

      const updatedStatus = document.getElementById('status').value;
      const updatedPrice = document.getElementById('price').value;

      const updatedData = {
        unitId: unitId,  // Same unit ID for update
        status: updatedStatus,
        price: updatedPrice
      };

      // Make API call to update the unit
      fetch(`https://4gt9bjtqq1.execute-api.eu-west-1.amazonaws.com/dev/units/${unitId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(updatedData)
      })
      .then(response => response.json())
      .then(data => {
        if (data && data.unitId) {
          // Update the row in the table with new values
          row.cells[1].textContent = updatedStatus;
          row.cells[2].textContent = updatedPrice;

          // Clear the form and hide it
          document.getElementById('unit-id').value = '';
          document.getElementById('status').value = '';
          document.getElementById('price').value = '';
          document.getElementById('add-unit-form').style.display = 'none';
        } else {
          alert("Failed to update unit. Please try again.");
        }
      })
      .catch(error => {
        console.error("Error updating unit:", error);
        alert("Error updating unit. Please try again.");
      });
    };
  }
});

// Remove Unit functionality
document.getElementById('unit-list').addEventListener('click', function(event) {
  if (event.target && event.target.classList.contains('remove-btn')) {
    const row = event.target.closest('tr');
    const unitId = row.cells[0].textContent;

    // API call to delete the unit
    fetch(`https://4gt9bjtqq1.execute-api.eu-west-1.amazonaws.com/dev/units/${unitId}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(response => response.json())
    .then(data => {
      if (data && data.unitId) {
        // Remove the row from the table
        row.remove();
      } else {
        alert("Failed to remove unit. Please try again.");
      }
    })
    .catch(error => {
      console.error("Error removing unit:", error);
      alert("Error removing unit. Please try again.");
    });
  }
});

// Search Functionality
// function searchUnits() {
//   const searchTerm = document.getElementById('search').value.toLowerCase();
//   const rows = document.querySelectorAll('#unit-list tr');

//   rows.forEach(row => {
//       const unitId = row.cells[0].textContent.toLowerCase();
//       const status = row.cells[1].textContent.toLowerCase();
//       const price = row.cells[2].textContent.toLowerCase();

//       if (unitId.includes(searchTerm) || status.includes(searchTerm) || price.includes(searchTerm)) {
//           row.style.display = '';
//       } else {
//           row.style.display = 'none';
//       }
//   });
// }

// Add event listener to search field
// document.getElementById('search').addEventListener('keyup', searchUnits);
