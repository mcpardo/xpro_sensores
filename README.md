# XPRO Sensores
Este proyecto está dirigido al uso y desarrollo de software para la implementación de una plataforma de evaluación para distintos sensores: temperatura, presión, calidad del aires, inerciales, etc. El repositorio contiene "forks" de librerías de software libre de terceros, que se modificaron convenientemente y que se incluyen como submódulos de git de tal forma que existe vinculación con los repositorios originales para permitir la actualización de los mismos cuando se desee. También se han creado otros ficheros desde el inicio, que implementan la función requerida para cada sensor.

## Librerías
Las librerías utilizadas en el proyecto son las siguientes:
- [Paho MQTT for Python](https://github.com/eclipse/paho.mqtt.python)
- [BSEC BME680 for Linux](https://github.com/alexh-name/bsec_bme680_linux)
- [Bluerobotics MS5837 for Python](https://github.com/bluerobotics/ms5837-python)
- [Adafruit CircuitPython ICM20X](https://github.com/adafruit/Adafruit_CircuitPython_ICM20X)
- [Adafruit CircuitPython LSM6DS](https://github.com/adafruit/Adafruit_CircuitPython_LSM6DS)
- [Sparkfun Magnetometer for Arduino](https://github.com/sparkfun/SparkFun_MMC5983MA_Magnetometer_Arduino_Library)

## Directorios
La explicación del contenido y función de los distintos directorios se encuentra a continuación:

### docker
Incluye el archivo de configuración de docker (docker-compose.yml) y las
carpetas correspondientes a cada uno de los contenedores (i.e. mosquitto).
Cada carpeta incluye la configuración específica del contenedor.

### sensores
- "client_X": contiene los archivos relacionados con el cliente X.
- "sub_sensores.py" y "sub_sensores_logger.py": archivo de Python que implementa el cliente suscrito a los distintos topics de MQTT. El segundo archivo, además, funciona como logger, registrando las salidas de los sensores a los que se suscribe en un fichero .txt.
- "libs": contiene librerias de distintos sensores (ignorada en .gitignore, ver en el repositorio local).
- "loggers": contiene un archivo ".txt" para cada sensor donde se registran los mensajes de los sensores.
- "basic_examples": contiene archivos de implementación de clientes básicos de MQTT en Python.




