document.getElementById('upload-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    formData.append('keywords', document.getElementById('keywords').value);

    const response = await fetch('/upload', {
        method: 'POST',
        body: formData
    });

    const result = await response.json();

    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '';  // Clear previous results

    if (result.filtered_results) {
        resultsDiv.innerHTML = '<h2 class="text-xl font-bold mb-2">Filtered Results:</h2>';
        result.filtered_results.forEach(line => {
            const p = document.createElement('p');
            p.textContent = line;
            p.className = 'mb-1';
            resultsDiv.appendChild(p);
        });
    } else {
        resultsDiv.textContent = result.error;
    }
});
