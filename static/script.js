let selectedSeat = null;

// GET ELEMENTS
const seatsContainer = document.getElementById("seats");

// CREATE SEATS
for (let i = 1; i <= 20; i++) {
    let s = document.createElement("div");
    s.classList.add("seat");
    s.innerText = i;

    s.onclick = () => {
        if (s.classList.contains("booked")) return;

        document.querySelectorAll(".seat").forEach(x => x.classList.remove("selected"));
        s.classList.add("selected");
        selectedSeat = i;
    };

    seatsContainer.appendChild(s);
}

// BOOK FUNCTION
function bookTicket() {
    let movie = document.getElementById("movie").value;
    let customer = document.getElementById("customer").value;
    let timing = document.getElementById("timing").value; // ✅ FIXED

    // VALIDATION
    if (!customer) {
        alert("Enter customer name");
        return;
    }

    if (!selectedSeat) {
        alert("Select seat first");
        return;
    }

    // API CALL
    fetch('/book', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            movie: movie,
            seat: selectedSeat,
            customer: customer,
            timing: timing
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === "success") {
            alert("Booking Success 🎉");

            // ✅ ONLY HERE PDF SHOULD OPEN
            window.location.href = `/receipt?movie=${movie}&seat=${selectedSeat}&customer=${customer}&timing=${timing}`;
        } else {
            alert(data.message);
        }
    });
}
function loadBookedSeats() {
    let movie = document.getElementById("movie").value;

    fetch(`/get_booked?movie=${movie}`)
    .then(res => res.json())
    .then(data => {
        document.querySelectorAll(".seat").forEach(seat => {
            seat.classList.remove("booked");
        });

        data.forEach(seatNo => {
            let seat = [...document.querySelectorAll(".seat")]
                .find(s => s.innerText == seatNo);

            if (seat) {
                seat.classList.add("booked");
            }
        });
    });
}
window.onload = loadBookedSeats;
document.getElementById("movie").onchange = loadBookedSeats;