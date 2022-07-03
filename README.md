# LCD84x48_Adapter

Programa para adaptar una imagen de tamaño cualquiera a un formato compatible con la pantalla Nokia LCD 5110 de resolución 84x48. Redimensiona la imagen, la pasa a monocromática y proporciona un arreglo en formato hexadecimal para copiar en un código de arduino que controle la pantalla

## Uso

Para correr el programa, ejecutar el archivo bash exec.sh que ejecutará las funciones en asm, C y la función filters_main.py enlazando todo. Se leera un archivo dentro de la carpeta Photos, y el resultado se guardará como PNG en Results y en formato array para LCD en Arrays.

Finalmente, para pasarlo a una pantalla Nokia LCD 5110 subir el código en display_img a un Arduino reemplazando el bitmapArray[504] por los arreglos que se desean visualizar. 

## Archivos adicionales
Las funciones intensity_main.py y sobel_main.py sirven para ejectuar únicamente los métodos respectivos por separado. También se incluye el archivo filters_main_tests.py que describe los tests de tiempos medios aplicados para comparar la rapidez de cada método y speedups. Por otro lado, se adjunta la versión convertida en Jupyter Notebook para pruebas rápidas. 
