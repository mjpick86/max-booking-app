const numberInput = document.getElementById('numberInput');
const squareButton = document.getElementById('squareButton');
const resultNumber = document.getElementById('resultNumber');

squareButton.addEventListener('click', async () => {
    const number = numberInput.value;

    if (!number) {
        return;
    }

    const response = await fetch('https://max-booking-app.onrender.com/square', {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({number: parseInt(number)}),
    });

    const data = await response.json();
    resultNumber.textContent = `Result: ${data.result}`;
});