document.getElementById("bookingForm").addEventListener("submit", function(event) {
    event.preventDefault();
    const checkInTime = new Date(document.getElementById("checkInTime").value);
    const checkOutTime = new Date(document.getElementById("checkOutTime").value);
    
    if (checkInTime.getTime() < Date.now() + 24 * 60 * 60 * 1000) {
        alert("Check-in time must be at least 1 days after the current time.");
        return;
    }
    
    if (checkOutTime.getTime() < checkInTime.getTime() + 12 * 60 * 60 * 1000) {
        alert("Check-out time must be at least 12 hours after the check-in.");
        return;
    }

    if (checkInTime.getTime() + 30 * 24 * 60 * 60 * 1000 < checkOutTime.getTime()) {
        alert("Hotel stay must be within 30 days. If a longer stay is required, please make separate bookings.");
        return;
    }
    
    const formInputs = document.querySelectorAll("#bookingForm input");
    let isFormValid = true;
    let firstEmptyInput = null;
    
    formInputs.forEach(input => {
        if (input.value === "") {
            if (!firstEmptyInput) {
                firstEmptyInput = input;
            }
            isFormValid = false;
        }
    });
    
    if (!isFormValid) {
        if (firstEmptyInput) {
            alert(`Please fill in ${firstEmptyInput.previousElementSibling.textContent}`);
        }
    } else {
        if (confirm("Are you sure you want to make the booking?")) {
            alert("Booking successful!");
        }
    }
})


