let unavailableDates = [];

window.onload = async function() {
    await fetchUnavailableDates();
}

async function fetchUnavailableDates() {
    const response = await fetch('http://localhost:8000/all_dates');
    const data = await response.json();
    unavailableDates = data.dates;
}

const form = document.querySelector('form');
const dateField = form.elements['dateInput'];
const helperText = document.getElementById('helperText');

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const name = form.elements['nameInput'].value;
    const date = form.elements['dateInput'].value;
    const comments = form.elements['commentsInput'].value;

    await fetch('http://localhost:8000/place_booking', {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({name, date, comments}),
    });
    await fetchUnavailableDates();
    helperText.textContent = unavailableDates;

});

$(document).ready(function() {
    $(function() {
        $('#dateInput').datepicker({
            defaultDate:"2026-03-29",
            dateFormat: "yy-mm-dd",
            firstDay: 1,
            beforeShowDay: my_check,
        });
    });
    
    function my_check(date) {
        var dd = date.getDate();
        var mm = date.getMonth()+1;
        var yyyy = date.getFullYear();
        var shortDate = yyyy+"-"+(mm<10 ? "0" : "")+mm+"-"+(dd<10 ? "0" : "")+dd;
        if (unavailableDates.includes(shortDate)) {
            return [false, "notav", "Unavailable"];
        } else {
            return [true, "av", shortDate];
        }
    }

});