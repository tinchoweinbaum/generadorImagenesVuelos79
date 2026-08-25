# generadorImagenesVuelos79

Toma un screenshot de la lista de vuelos (arribos y partidas) y la pega sobre placas listas para salir al aire.

La configuracion vive en `datosvuelos.txt`, al lado del `.exe` (o en la carpeta del proyecto si corres el script). Formato `clave=valor`:

```
dir=C:\Placas\aire\HD
url=https://www.aeropuertosargentina.com/es/vuelos?movtp=partidas&idarpt=Mar%20del%20Plata%2C%20MDQ
clase=.flex.flex-col.space-5.mb-6.xl\:mb-8.w-full
clase_arribos=.group.inline-flex.items-center.border-b-2.py-2.xl\:py-2.px-3.lg\:px-4.font-open.text-sm.font-semibold.leading-4.space-3.cursor-pointer.border-transparent.text-gray-500
clase_cerrar=.fill-none.stroke-white
```

- `dir`: carpeta donde se guardan `arribos.bmp` y `partidas.bmp`
- `url`: pagina de **partidas** (no el home). El programa abre esa URL y despues cambia al tab de arribos
- `clase`: selector CSS de la lista de vuelos a fotografiar
- `clase_arribos`: selector CSS del tab de arribos
- `clase_cerrar`: selector del boton para cerrar popups (opcional)

Tambien se acepta el formato viejo por lineas, sin claves:

1. directorio de salida
2. url
3. clase de la lista (opcional)
4. clase del tab arribos (opcional)
5. clase del boton cerrar (opcional)

Si falta el archivo o alguna clave, se usan estos valores por defecto:

```
C:\Placas\aire\HD
https://www.aeropuertosargentina.com/es/vuelos?movtp=partidas&idarpt=Mar%20del%20Plata%2C%20MDQ
.flex.flex-col.space-5.mb-6.xl\:mb-8.w-full
```

Si no hay vuelos (lista ausente, vacia, sin horarios, o la pagina muestra "No hay resultados"), no se publica el screenshot roto: se usa la placa **No hay vuelos** (`placas/placaArribosSinVuelos.png` y `placas/placaPartidasSinVuelos.png`). Si la pagina no responde, o hay vuelos pero no se encuentra la clase configurada, se deja la placa anterior para no mandar basura al aire.
