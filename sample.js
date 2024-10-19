document.getElementById('loanForm').addEventListener('submit', async (event) => {
    event.preventDefault(); // Prevent form submission

    // Collect form data
    const formData = {
        annual_inc: parseFloat(document.getElementById('annual_inc').value),
        short_emp: parseInt(document.getElementById('short_emp').value),
        emp_length_num: parseInt(document.getElementById('emp_length_num').value),
        dti: parseFloat(document.getElementById('dti').value),
        revol_util: parseFloat(document.getElementById('revol_util').value),
        total_rec_late_fee: parseInt(document.getElementById('total_rec_late_fee').value),
        od_ratio: parseFloat(document.getElementById('od_ratio').value),
        home_ownership_OWN: document.getElementById('home_ownership').value === 'OWN' ? 1 : 0,
        home_ownership_MORTGAGE: document.getElementById('home_ownership').value === 'MORTGAGE' ? 1 : 0,
        home_ownership_RENT: document.getElementById('home_ownership').value === 'RENT' ? 1 : 0
    };

    // Send POST request to the Flask API
    const response = await fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    });

    // Get the prediction result
    const result = await response.json();

    // Display the result
    document.getElementById('result').innerText = `Prediction: ${result[0] === 1 ? 'Loan Default' : 'No Default'}`;
});
