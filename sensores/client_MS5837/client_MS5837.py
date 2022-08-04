#!/usr/bin/python

################################################################################
# LIBRERIAS
################################################################################

import ms5837
import time
import sys
import threading
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json

################################################################################
# CONFIGURACION Y CONEXION MQTT
################################################################################
hostname = "192.168.2.203"
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conexion establecida con el broker")
    else:
        print(f"Fallo de la conexion con codigo {rc}")

client = mqtt.Client()
client.on_connect = on_connect

# create connection, the three parameters are broker address, 
# broker port number, and keep-alive time respectively
client.connect(hostname, 1883, 60)
client.loop_start()

################################################################################
# CONFIGURACION SENSOR
################################################################################

# Se crea una clase para el sensor de presion
# se puede elegir entre distintos modelos:
#sensor = ms5837.MS5837_30BA()
#sensor = ms5837.MS5837_30BA(0)
sensor = ms5837.MS5837_02BA()      # Como argumento se puede espefificar el bus de I2C a usar
#sensor = ms5837.MS5837_02BA(0)
#sensor = ms5837.MS5837(model=ms5837.MS5837_MODEL_30BA, bus=0) # Specify model and bus

# Inicializacion del sensor
if not sensor.init():
        print("Sensor could not be initialized")
        exit(1)

# Se leen valores del sensor para actualizar la presion y la temperatura
if not sensor.read():
    print("Sensor read failed!")
    exit(1)

# Se establece la densidad del liquido donde podria estar sumergido el sensor
#   - Se usara para el calculo de la profundidad de inmersion (depth)
#   - No afecta al cálculo de altura (altitude) porque ese se hace usando la densidad del aire MSL (Mean Sea Level)
sensor.setFluidDensity(ms5837.DENSITY_FRESHWATER)  # Agua dulce = 997kg/m3 (valor por defecto)
#sensor.setFluidDensity(ms5837.DENSITY_SALTWATER)  # Agua salada = 1029kg/m3


################################################################################
# LOOP INFINITO
################################################################################

def ms5837_ISSR():
    if sensor.read():
        temp = round(sensor.temperature(),2);
        press = round(sensor.pressure(),2);
        altitude = round(sensor.altitude(),2);

        payload = {"Temperature": temp, "Pressure": press, "Altitude": altitude}
        publish.single("ms5837", json.dumps(payload), hostname=hostname)
        print("Temp: %0.2f degC, Pressure: %0.2f mbar, Altitude: %0.2f m" % (temp, press, altitude))
        
    else:
        print("Sensor read failed!")
        exit(1)

    # timer que se cumple cada ¿5s?
    timerObject = threading.Timer(5, ms5837_ISSR)  
    # Empieza a funcionar el timer
    timerObject.start()

ms5837_ISSR()

# set the network loop blocking, it will not actively end the 
# program before calling disconnect() or the program crash
# client.loop_forever()