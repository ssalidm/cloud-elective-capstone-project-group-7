// Function to show/hide the "Add Unit" form
document.getElementById('add-unit-btn').addEventListener('click', function() {
    const form = document.getElementById('add-unit-form');
    form.style.display = form.style.display === 'none' ? 'block' : 'none';
  });
  
  // Function to handle adding a new unit to the table
  document.getElementById('unit-form').addEventListener('submit', function(event) {
    event.preventDefault();
  
    const unitId = document.getElementById('unit-id').value;
    const status = document.getElementById('status').value;
    const price = document.getElementById('price').value;
  
    // Create a new row for the unit
    const newRow = document.createElement('tr');
    newRow.innerHTML = `
      <td>${unitId}</td>
      <td>${status}</td>
      <td>${price}</td>
      <td>
        <button>Edit</button>
        <button>Remove</button>
      </td>
    `;
  
    // Append the new row to the table
    document.getElementById('unit-list').appendChild(newRow);
  
    // Clear the form and hide it
    document.getElementById('unit-id').value = '';
    document.getElementById('status').value = '';
    document.getElementById('price').value = '';
    document.getElementById('add-unit-form').style.display = 'none';
  });
  
  // Search Functionality
  function searchUnits() {
    const searchTerm = document.getElementById('search').value.toLowerCase();
    const rows = document.querySelectorAll('#unit-list tr');
  
    rows.forEach(row => {
      const unitId = row.cells[0].textContent.toLowerCase();
      const status = row.cells[1].textContent.toLowerCase();
      const price = row.cells[2].textContent.toLowerCase();
  
      if (unitId.includes(searchTerm) || status.includes(searchTerm) || price.includes(searchTerm)) {
        row.style.display = '';
      } else {
        row.style.display = 'none';
      }
    });
  }
  
  // Add event listener to search field
  document.getElementById('search').addEventListener('keyup', searchUnits);
  