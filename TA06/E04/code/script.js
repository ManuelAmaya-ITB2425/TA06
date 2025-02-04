document.addEventListener("DOMContentLoaded", function () {
    fetch('../../E03/summary_statistics.csv')
        .then(response => response.text())
        .then(csvText => {
            const rows = csvText.split('\n').map(row => row.split(','));
            let tableHTML = '<tr><th>Tipo</th><th>Dato</th></tr>';
            rows.forEach(row => {
                if (row.length > 1) {
                    tableHTML += `<tr><td>${row[0]}</td><td>${row[1]}</td></tr>`;
                } else if (row.length === 1 && row[0].trim() !== '') {
                    tableHTML += `<tr><th colspan='2'>${row[0]}</th></tr>`;
                }
            });
            document.getElementById('data-table').innerHTML = tableHTML;
        })
        .catch(error => console.error('Error cargando el archivo CSV:', error));
});
