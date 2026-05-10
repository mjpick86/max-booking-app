let unavailableDates = [];

window.onload = async function() {
    await fetchUnavailableDates();
    form.reset();
}

async function fetchUnavailableDates() {
    const response = await fetch('http://localhost:8000/all_dates');
    const data = await response.json();
    unavailableDates = data.dates;
}

function dateFromDMY(dateStr){
    let dateArray = dateStr.split("/");
    let newDateStr = `${dateArray[2]}-${dateArray[1]}-${dateArray[0]}`;
    return new Date(newDateStr);
}

function DMYToYMD(dateStr){
    let dateArray = dateStr.split("/");
    return `${dateArray[2]}-${dateArray[1]}-${dateArray[0]}`;
}

function checkInDateValid(dateStr){
    let newDate = dateFromDMY(dateStr);
    if (isNaN(newDate)) return false;
    return !unavailableDates.includes(DMYToYMD(dateStr)) && newDate > new Date();
}

const form = document.querySelector('form');
const checkInField = form.elements['checkInInput'];
const nameField = form.elements['nameInput'];
const commentsField = form.elements['commentsInput'];
const checkOutField = form.elements['checkOutInput'];
const helperText = document.getElementById('helperText');

$('#checkInInput').on('change', function() {
    if (checkInDateValid(checkInField.value)) {
        const selectedDate = this.value.split('/').reverse().join('-');
        var checkOutMinDate = new Date(selectedDate);
        checkOutMinDate.setDate(checkOutMinDate.getDate() + 1);
        var checkOutMaxDate = new Date(selectedDate);
        checkOutMaxDate.setDate(checkOutMaxDate.getDate() + 30);
        for (var i = 0; i < unavailableDates.length; i++) {
            var unavailableDate = new Date(unavailableDates[i]);
            if (unavailableDate >= checkOutMinDate && unavailableDate < checkOutMaxDate) {
                checkOutMaxDate = unavailableDate;
            }
        }
        $('#checkOutInput').datepicker("option", "minDate", checkOutMinDate);
        $('#checkOutInput').datepicker("option", "maxDate", checkOutMaxDate);
        $('#pCheckOut').show();
    } else {
        $('#pCheckOut').hide();
    }
});

$(document).ready(function() {
    $(function() {
        $('#checkInInput').datepicker({
            defaultDate: 1,
            dateFormat: "dd/mm/yy",
            minDate: 1,
            firstDay: 1,
            beforeShowDay: my_check_in,
            onselect: function() {
                $(this).change();
            }
        });
    });
    
    function getShortDate(date) {
        var dd = date.getDate();
        var mm = date.getMonth()+1;
        var yyyy = date.getFullYear();
        var shortDate = yyyy+"-"+(mm<10 ? "0" : "")+mm+"-"+(dd<10 ? "0" : "")+dd;
        return shortDate;
    }
    function my_check_in(date) {
        var shortDate = getShortDate(date);
        if (unavailableDates.includes(shortDate)) {
            return [false, "notav", "Unavailable"];
        } else {
            return [true, "av", shortDate];
        }
    }
    $(function() {
        $('#checkOutInput').datepicker({
            defaultDate: 1,
            dateFormat: "dd/mm/yy",
            firstDay: 1,
        });
    });

});

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const name = form.elements['nameInput'].value;
    const checkInDate = form.elements['checkInInput'].value;
    const checkOutDate = form.elements['checkOutInput'].value;
    const comments = form.elements['commentsInput'].value;

    const response = await fetch('http://localhost:8000/place_booking_range', {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({name, start_date: checkInDate, end_date: checkOutDate, comments}),
    });
    const data = await response.json();
    if (data["message"] == "Booking placed successfully"){
        alert("Your booking has successfully been placed!");
        form.reset();
        fetchUnavailableDates();
    } else {
        alert("An error occurred when processing your booking. Please try again.");
    }
});