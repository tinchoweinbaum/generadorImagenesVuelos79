# generadorImagenesVuelos79
Toma un screenshot de la página aeropuertosargentina.com (o aeropuertobahiblanca.com, depende que branch estés) de las partidas y salidas y las guarda en un directorio determinado, para después generar una nueva imagen, utilizando una placa donde poner el screenshot.

Se pueden modificar parámetros del programa como la url de la página y el directorio donde guardar la imagen generada en un archivo "datosvuelos.txt". Este archivo se organiza de la siguiente manera:

1ra Línea: Directorio donde guardar el archivo, ej = "D:\Placas\MDQ" (sin comillas)
2da Línea: Url de la página de arribos de aeropuertosargentina.com, NO la landing page ni home de aeropuertosargentina.com, sí o sí la página de arribos.

Si no se especifica alguno de los dos datos, se toman por defecto los siguientes:

D:\placas\aire\HD
https://www.aeropuertosargentina.com/es/vuelos?movtp=partidas&idarpt=Mar%20del%20Plata%2C%20MDQ

Estos valores también se asumen si no existe datosvuelos.txt
