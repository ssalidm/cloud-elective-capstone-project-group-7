function openBookingModal() {
    document.getElementById('bookingModal').style.display = 'block';
}

function closeBookingModal() {
    document.getElementById('bookingModal').style.display = 'none';
}

function confirmBooking() {
    const unitSelection = document.getElementById("unit-selection").value;
    const storageSize = document.getElementById("storage-size").value;
    const locationSelection = document.getElementById("location-selection").value;
    const recurringPayment = document.getElementById("recurring-payment").value;
    const paymentMethod = document.getElementById("payment-method").value;
    const customerEmail = document.getElementById("customer-email").value;

    if (!customerEmail) {
        alert("Please enter a valid email.");
        return;
    }

    const bookingDetails = {
        unit: unitSelection,
        storageSize: storageSize,
        location: locationSelection,
        recurringPeriod: recurringPayment,
        paymentMethod: paymentMethod,
        email: customerEmail,
    };

    fetch('/generate-invoice', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(bookingDetails),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Invoice has been sent to your email.');
            closeBookingModal();
        } else {
            alert('There was an issue processing your payment.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error processing the request. Please try again later.');
    });
}

window.onclick = function(event) {
    const modal = document.getElementById('bookingModal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
};
