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
const checkinField = form.elements['checkInInput'];
const helperText = document.getElementById('helperText');

$('#checkInInput').on('change', function() {
    const selectedDate = this.value;
    var checkOutMinDate = new Date(selectedDate);
    checkOutMinDate.setDate(checkOutMinDate.getDate() + 1);
    var checkOutMaxDate = new Date(selectedDate);
    checkOutMaxDate.setDate(checkOutMaxDate.getDate() + 30);
    for (var i = 0; i < unavailableDates.length; i++) {
        var unavailableDate = new Date(unavailableDates[i]);
        if (unavailableDate > checkOutMinDate && unavailableDate < checkOutMaxDate) {
            checkOutMaxDate = unavailableDate;
        }
    }
    $('#checkOutInput').datepicker("option", "minDate", checkOutMinDate);
    checkOutMaxDate.setDate(checkOutMaxDate.getDate() - 1);
    $('#checkOutInput').datepicker("option", "maxDate", checkOutMaxDate);
    helperText.textContent = checkOutMaxDate;
});

$(document).ready(function() {
    $(function() {
        $('#checkInInput').datepicker({
            defaultDate:"2026-03-29",
            dateFormat: "yy-mm-dd",
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
            defaultDate:"2026-03-29",
            dateFormat: "yy-mm-dd",
            firstDay: 1,
        });
    });

});

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const name = form.elements['nameInput'].value;
    const date = form.elements['checkInInput'].value;
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