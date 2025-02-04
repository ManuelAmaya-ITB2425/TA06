// Función para leer y mostrar el archivo CSV
function loadCSVData() {
    // Ruta al archivo CSV
    const csvFile = '../../E03/summary_statistics.csv'; // Ruta ajustada

    // Usamos fetch para obtener el archivo CSV
    fetch(csvFile)
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al cargar el archivo CSV');
            }
            return response.text(); // Leer el archivo como textooo
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

    // Procesar cada fila
    let isTopYearsSection = false; // Variable para manejar las secciones de "Top 3 years"
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
            // Comprobar si la fila contiene los encabezados de las secciones
            if (cells[0].includes("Top 3 years")) {
                // Añadir el título para la sección de años con mayor precipitación
                if (cells[0].includes("most precipitation")) {
                    html += `<tr><td colspan="2"><strong>${cells[0]}</strong></td></tr>`;
                } else if (cells[0].includes("driest years")) {
                    html += `<tr><td colspan="2"><strong>${cells[0]}</strong></td></tr>`;
                }
            } else if (cells[0].includes("Year")) {
                // Filas de años con precipitación o años secos
                html += '<tr>';
                html += `<td>${cells[0]}</td><td>${cells[1]}</td>`;
                html += '</tr>';
            } else {
                // Filas de estadísticas generales
                html += '<tr>';
                html += `<td>${cells[0]}</td><td>${cells[1]}</td>`;
                html += '</tr>';
            }
        }
    });

    html += '</tbody></table>';
    document.getElementById('csv-data').innerHTML = html;
}

// Cargar y mostrar los datos al cargar la página
window.onload = loadCSVData;
