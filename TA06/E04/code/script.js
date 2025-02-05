// Función para leer el archivo CSV y mostrarlo en la tabla
function leerCSV() {
    const archivoCSV = '../../E03/summary_statistics.csv'; // Ruta al archivo CSV
    fetch(archivoCSV)
        .then(response => response.text())
        .then(data => {
            const lines = data.split('\n');
            let resumen = {};
            let topPrecipitacion = [];
            let topSecos = [];
            let currentCategory = '';

            lines.forEach(line => {
                const row = line.split(',');

                if (row[0] === 'Percentage of valid files') {
                    resumen.valid_files = row[1];
                } else if (row[0] === 'Percentage of valid days') {
                    resumen.valid_days = row[1];
                } else if (row[0] === 'Number of processed data points') {
                    resumen.data_points = row[1];
                } else if (row[0] === 'Top 3 years with most precipitation') {
                    currentCategory = 'precipitation';
                } else if (row[0] === 'Top 3 driest years') {
                    currentCategory = 'dry';
                } else if (currentCategory === 'precipitation' && row[0].startsWith('Year')) {
                    topPrecipitacion.push({
                        year: row[1],
                        precipitation: row[3]
                    });
                } else if (currentCategory === 'dry' && row[0].startsWith('Year')) {
                    topSecos.push({
                        year: row[1],
                        precipitation: row[3]
                    });
                }
            });

            // Mostrar los datos en la tabla
            mostrarDatos(resumen, topPrecipitacion, topSecos);
        })
        .catch(error => console.error('Error leyendo el archivo CSV:', error));
}

function mostrarDatos(resumen, topPrecipitacion, topSecos) {
    const tabla = document.getElementById('estadisticas');

    // Mostrar el resumen de estadísticas
    const row1 = tabla.insertRow();
    row1.insertCell(0).innerText = 'Percentage of valid files';
    row1.insertCell(1).innerText = resumen.valid_files;

    const row2 = tabla.insertRow();
    row2.insertCell(0).innerText = 'Percentage of valid days';
    row2.insertCell(1).innerText = resumen.valid_days;

    const row3 = tabla.insertRow();
    row3.insertCell(0).innerText = 'Number of processed data points';
    row3.insertCell(1).innerText = resumen.data_points;

    // Mostrar los años con más precipitación
    const row4 = tabla.insertRow();
    row4.insertCell(0).innerText = 'Top 3 years with most precipitation';
    const cell4 = row4.insertCell(1);
    topPrecipitacion.forEach(item => {
        const li = document.createElement('li');
        li.innerText = `${item.year} - ${item.precipitation} liters`;
        cell4.appendChild(li);
    });

    // Mostrar los años más secos
    const row5 = tabla.insertRow();
    row5.insertCell(0).innerText = 'Top 3 driest years';
    const cell5 = row5.insertCell(1);
    topSecos.forEach(item => {
        const li = document.createElement('li');
        li.innerText = `${item.year} - ${item.precipitation} liters`;
        cell5.appendChild(li);
    });
}

// Llamar a la función para cargar el CSV al cargar la página
window.onload = leerCSV;
