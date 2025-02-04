# DOCUMENTACION DE LA PRACTICA TA06
_Hecho por Manuel Amaya, Rodrigo Montoya, Abel Aymami y Diego Cornelles_

[Ejercicio 1](#Ejercicio-1)

[Ejercicio 2](#Ejercicio-2)

[Ejercicio 3](#Ejercicio-3)

[Ejercicio 4](#Ejercicio-4)

[Ejercicio 5](#Ejercicio-5)



## Ejercicio 1:
Primero de todo debíamos de **obtener los datos**, para ello debíamos entrar en AEMET (Agencia Estatal de Meteorología) para descargarnos los datos. Pero para poder descargarlos debíamos de conseguir la API-key, para ello buscamos obtención de api-key AEMET en el buscador y la primera opción será el enlace en el que la podremos obtener, entramos y rellenamos el formulario:

![ImagenAPI](./Caps/Cap_API.png)

Ahora, una vez obtenido la API-key, entramos a la página de AEMET por el enlace directo que nos ofreció el profesor, pegamos la API-key y buscamos el que era el archivo correcto a descargar:

![ImagenDescarga](./Caps/Cap_ArchDownload.png)

Luego se deberán de subir los datos al PyCharm para poder procesarlas y organizarlas.

![ImagenPyCHarm](./Caps/Cap_PyCharm.png)

## Ejercicio 2
Una vez obtenidos los datos, deberemos de organizarlos y procesarlos. Para ello utilizamos la aplicación de PyCharm y con el apoyo de Copilot, en la que crearemos un archivo y utilizaremos el lenguaje Python.

Para ello el código debe de poder leer los ficheros; saber que estén delimitados a los datos especificados (Espacios, comas, separar cabecera de los datos, que todos los archivos tengan el mismo formato y asegurando que no tengan ningún error, según los delimitadores especificados. 

Después hay que calcular el porcentaje de datos que faltan (-999), las estadisticas de los datos procesados:

- **Medianas totales y anuales**
- **Tendencia de cambio**
- **Extremos (Años con mas y menos precipitaciones)**

Todos los datos que tenemos hay que extraerlos, por lo tanto hay que crear un fichero log, para poder ver las estadisticas que pedimos.

![resultatScript](./Caps/resultatScript.png)

Ademas habrá que analizar los datos, de manera que tengamos que pensar que estadisticas podemos hacer.

Para poder obtener todas las estadisticas necesarias necesitaremos un script:

![codi1](./Caps/codi1.png)
![codi2](./Caps/codi2.png)
![codi3](./Caps/codi3.png)
![codi4](./Caps/codi4.png)

A veces los codigos o los datos pueden tener error, por lo tanto hay que tener un fichero de errores, que indique que errores tenemos.

![ficheroError](./Caps/ficheroError.png)

## Ejercicio 3

Una vez hemos obtenido todos los datos necesarios hay que crear resumenes estadisticos y graficos estadisticos, para que sea mucho mas facil de entender.

![graficos](./TA06/E03/statistics_plot.png)

Después hay que exportar esos resumenes estadisticos a un fichero csv.

## Ejercicio 4

Ahora que ya tenemeos los datos necesarios, necesitamos publicarlas y para eso usaremos una web.

## Ejercicio 5
