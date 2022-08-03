# XPRO Sensores
Este proyecto está dirigido a guardar los archivos y versiones correspondientes a la plataforma de pruebas de sensores.

## Librerías
Las librerías de terceros (open-source) implementadas en el proyecto son las siguientes:
- [Paho MQTT for Python](https://github.com/eclipse/paho.mqtt.python)
- [BSEC BME680 for Linux](https://github.com/alexh-name/bsec_bme680_linux)
- [MS5837 for Python](https://github.com/bluerobotics/ms5837-python)

## Directorios
La explicación del contenido y función de los distintos directorios se encuentra a continuación:

### docker
Incluye el archivo de configuración de docker (docker-compose.yml) y
carpetas correspondientes a cada uno de los contenedores (i.e. mosquitto).
Cada carpeta incluye la configuración específica del contenedor.

### sensores
- Subdirectorios:
  1. "client_X": contiene los archivos relacionados con el cliente X.
  2. "libs": contiene librerias de distintos sensores. Algunas de ellas no se implementan.
  3. "loggers": contiene un archivo ".txt" para cada sensor donde se registran los mensajes de los sensores.
  4. "basic_examples": contiene archivos de implementación de clientes básicos de MQTT en Python.
- Archivos de código de ejemplo:
  1. "client_pub.py" y "client_sub.py" son ejemplos básicos de clientes MQTT para publicación y suscripción, respectivamente. 	
  2. "client_pub_timer.py" es igual que  "client_pub.py" pero los intervalos de publicación están controlados por una interrupción de un timer.
  3. "sub_sensores.py" es el cliente que se suscribe a todos los sensores publicadores.



