#!/usr/bin/env python3
################################################################################
# LIBRERIAS
################################################################################
import serial
import time
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
# COMUNICACION SERIE
################################################################################
if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0', 115200 , timeout=1)
    ser.reset_input_buffer()
    while True:
        if ser.in_waiting > 100:            # La funcion devuelve el numero de bytes que le llegan por puerto serie.
                                            # Para reducir la cantidad de datos mostrados, se usa un numero mas elevado que 0.
            line = ser.readline().decode('utf-8').rstrip()
            ser.reset_input_buffer()
            x,y,z = line.split()

            x_int = (int(x)-131072)/131072   # Se convierte la medida en Gauss (unidad de densidad de flujo magnetico)
            y_int = (int(y)-131072)/131072
            z_int = (int(z)-131072)/131072
            print(line)
            ################################################################################
            # PUBLICACION DE MEDIDAS
            ################################################################################   
            payload = {"x (G)": x_int, "y (G)": y_int, "z (G)": z_int}
            publish.single("magneto", json.dumps(payload), hostname=hostname)

