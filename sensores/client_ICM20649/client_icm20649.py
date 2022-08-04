################################################################################
# LIBRERIAS
################################################################################
import time
import board
from adafruit_icm20x import ICM20649, AccelRange, GyroRange
import time
import sys
import threading
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json

################################################################################
# VARIABLES GLOBALES
################################################################################
k = 0
# Se inicializan los maximos de giroscopio y acelerometro a 0
ax_max = ay_max = az_max = 0
gx_max = gy_max = gz_max = 0

###################################################################################
# Funcion: printNewMax(value, current_max, axis)
# Descripcion: Compara el nuevo valor medido con el maximo actual y lo actualiza
# en caso de que el nuevo valor sea mayor
###################################################################################
def printNewMax(value, current_max, axis, hostname):
    if value > current_max:
        old_max = current_max
        current_max = value
        if old_max != 0:         # Evita que se imprima el primer valor cuando aún no hay maximo
            print(axis, "Max:", current_max)
            print("\n")
            payload = {axis: current_max}
            publish.single("icm20649", json.dumps(payload), hostname=hostname)
    return current_max


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
# Inicializacion de I2C y creacion de objeto ism
i2c = board.I2C()  # uses board.SCL and board.SDA
ism = ICM20649(i2c)

# Se establecen los rangos de medida
ism.accelerometer_range = AccelRange.RANGE_30G
print("Accelerometer range set to: %d g" % AccelRange.string[ism.accelerometer_range])
ism.gyro_range = GyroRange.RANGE_500_DPS
print("Gyro range set to: %d DPS" % GyroRange.string[ism.gyro_range])

# Se establecen las tasas de salida de datos
ism.gyro_data_rate = 5                # Tasa a la que se toman medidas del giroscopio en Hz -> Puede ir de 4.4 a 1125 Hz
ism.accelerometer_data_rate = 5       # Tasa a la que se toman medidas del acelerometro en Hz -> Puede ir de 0.27 a 1125 Hz


################################################################################
# LOOP INFINITO
################################################################################
# En este blucle pasan dos cosas a frecuencias distintas:
#   1. Los maximos se comprueban cada t_max_update (segundos), y se publican al detectarse, asincronamente.
#   2. Las medidas actuales se publican cada k_max*t_max_update (segundos).

def icm20649_ISSR():
    global ax_max, ay_max, az_max, gx_max, gy_max, gz_max
    global k

    t_max_update = 1 # Tiempo de actualizacion de los maximos, en segundos
    k_max = 10       # Iteraciones de t_max_update para publicar en MQTT

    k = k+1 # Aumento de las iteraciones

    # Actualizacion de los maximos de cada eje, en su caso
    ax_max = printNewMax(ism.acceleration[0], ax_max, "max_ax", hostname)
    ay_max = printNewMax(ism.acceleration[1], ay_max, "max_ay", hostname)
    az_max = printNewMax(ism.acceleration[2], az_max, "max_az", hostname)

    gx_max = printNewMax(ism.gyro[0], gx_max, "max_gx", hostname)
    gy_max = printNewMax(ism.gyro[1], gy_max, "max_gy", hostname)
    gz_max = printNewMax(ism.gyro[2], gz_max, "max_gz", hostname)

    if k == k_max:  
        k = 0   # Se resetean las iteraciones
        print("Accel X:%.2f Y:%.2f Z:%.2f ms^2 \nGyro X:%.2f Y:%.2f Z:%.2f degrees/s \n"
            % (ism.acceleration + ism.gyro))

        ################################################################################
        # PUBLICACION DE MEDIDAS
        ################################################################################   
        payload = {"ax (m/s2)": ism.acceleration[0], "ay (m/s2)": ism.acceleration[1], "az (m/s2)": ism.acceleration[2], 
                   "gx": ism.gyro[0], "gy": ism.gyro[1], "gz": ism.gyro[2]}
        publish.single("icm20649", json.dumps(payload), hostname=hostname)

    # timer que se cumple cada 1s
    timerObject = threading.Timer(t_max_update, icm20649_ISSR)  
    # Empieza a funcionar el timer
    timerObject.start()

icm20649_ISSR()