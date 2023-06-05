document.querySelector('input[name="client_price"]').addEventListener('change', (event) => {
    let value = parseFloat(event.target.value);
    event.target.value = value.toFixed(2);
});
document.querySelector('input[name="vendor_price"]').addEventListener('change', (event) => {
    let value = parseFloat(event.target.value);
    event.target.value = value.toFixed(2);
});