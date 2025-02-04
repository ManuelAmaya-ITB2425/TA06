// Función para leer y mostrar el archivo CSV
function loadCSVData() {
    // Ruta al archivo CSV
    const csvFile = '../../E03/summary_statistics.csv'; // Asegúrate de que esta ruta sea correcta

    // Usamos fetch para obtener el archivo CSV
    fetch(csvFile)
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al cargar el archivo CSV');
            }
            return response.text(); // Leer el archivo como texto
        })
        .then(data => {
            console.log("Datos CSV cargados:", data); // Verificar que los datos CSV se hayan cargado correctamente
            displayCSV(data); // Llamamos a la función para mostrar los datos
        })
        .catch(error => {
            console.error('Error al leer el archivo CSV:', error);
        });
}

// Función para convertir el CSV en una tabla HTML
function displayCSV(csvContent) {
    const rows = csvContent.split('\n');
    let html = '<table>';

    let isTopYearsSection = false;

    rows.forEach((row, index) => {
        const cells = row.split(',');

        // Ignorar filas vacías
        if (cells.length === 1 && !cells[0]) return;

        // Primer fila: encabezado de la tabla
        if (index === 0) {
            html += '<thead><tr>';
            cells.forEach(cell => {
                html += `<th>${cell.trim()}</th>`;
            });
            html += '</tr></thead><tbody>';
        } else {
            if (cells[0].includes("Top 3 years")) {
                // Añadir la sección de años con precipitación o más secos
                html += `<tr><td colspan="2"><strong>${cells[0]}</strong></td></tr>`;
                isTopYearsSection = true;
            } else if (cells[0].includes("Year")) {
                // Si es una fila de año
                if (isTopYearsSection) {
                    html += `<tr><td>${cells[0]}</td><td>${cells[1]}</td></tr>`;
                } else {
                    // Filas generales
                    html += `<tr><td>${cells[0]}</td><td>${cells[1]}</td></tr>`;
                }
            } else {
                // Filas de estadísticas generales
                html += `<tr><td>${cells[0]}</td><td>${cells[1]}</td></tr>`;
            }
        }
    });

    html += '</tbody></table>';
    document.getElementById('csv-data').innerHTML = html;
}

// Cargar y mostrar los datos al cargar la página
window.onload = loadCSVData;
