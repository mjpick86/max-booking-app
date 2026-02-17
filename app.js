const numberInput = document.getElementById('numberInput');
const squareButton = document.getElementById('squareButton');
const resultNumber = document.getElementById('resultNumber');

squareButton.addEventListener('click', async () => {
    
    const number = numberInput.value;

    if (!number) {
        return;
    }
    resultNumber.textContent = `Calculating...`;
    await fetch('http://localhost:8000/square', {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({number: parseInt(number)}),
    });

    const response = await fetch('http://localhost:8000/last_squares');
    const data = await response.json();
    resultNumber.textContent = `Result: ${data.result}`;

});