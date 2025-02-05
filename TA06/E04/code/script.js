// Función para leer y mostrar el archivo CSV seleccionado por el usuario
function handleFileSelect(event) {
    const file = event.target.files[0]; // Obtener el archivo seleccionado

    if (!file) {
        alert("Por favor, selecciona un archivo CSV.");
        return;
    }

    // Mostrar el nombre del archivo elegido
    document.getElementById('file-name-display').textContent = `Fichero elegido: ${file.name}`;

    const reader = new FileReader(); // Crear un lector de archivos

    // Cuando el archivo se haya cargado, procesarlo
    reader.onload = function (e) {
        const csvContent = e.target.result; // Contenido del archivo
        console.log("Datos CSV cargados:", csvContent); // Verificar en consola
        displayCSV(csvContent); // Llamamos a la función para mostrar los datos
    };

    reader.readAsText(file); // Leer el archivo como texto
}

// Función para convertir el CSV en una tabla HTML
function displayCSV(csvContent) {
    const rows = csvContent.trim().split('\n');
    let html = '<table border="1">';

    let isTopYearsSection = false;

    rows.forEach((row, index) => {
        const cells = row.split(',');

        // Ignorar filas vacías
        if (cells.length === 1 && !cells[0]) return;

        // Si la fila no tiene comas, es un encabezado
        if (cells.length === 1) {
            html += `<tr><th colspan="2">${cells[0]}</th></tr>`;
            isTopYearsSection = cells[0].includes("Top 3");
        } else {
            // Filas normales de datos
            html += '<tr>';
            cells.forEach(cell => {
                html += `<td>${cell.trim()}</td>`;
            });
            html += '</tr>';
        }
    });

    html += '</table>';
    document.getElementById('csv-data').innerHTML = html;
}

// Agregar evento al input para cargar archivos
document.getElementById('csvFileInput').addEventListener('change', handleFileSelect);
