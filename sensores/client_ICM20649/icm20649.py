import time
import board
from adafruit_icm20x import ICM20649, AccelRange, GyroRange
import time
import sys
import threading

k = 0

###################################################################################
# Funcion: printNewMax(value, current_max, axis)
# Descripcion: Compara el nuevo valor medido con el maximo actual y lo actualiza
# en caso de que el nuevo valor sea mayor
###################################################################################
def printNewMax(value, current_max, axis):
    if value > current_max:
        current_max = value
        print(axis, "Max:", current_max)
        print("\n")
    return current_max

# Inicializacion de I2C y creacion de objeto ism
# pylint:disable=no-member
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

# Se inicializan los maximos de giroscopio y acelerometro a 0
ax_max = ay_max = az_max = 0
gx_max = gy_max = gz_max = 0

def icm20649_ISSR():
    global ax_max, ay_max, az_max, gx_max, gy_max, gz_max
    global k

    k = k+1

    # Actualizacion de los maximos de cada eje, en su caso
    ax_max = printNewMax(ism.acceleration[0], ax_max, "AX")
    ay_max = printNewMax(ism.acceleration[1], ay_max, "AY")
    az_max = printNewMax(ism.acceleration[2], az_max, "AZ")

    gx_max = printNewMax(ism.gyro[0], gx_max, "GX")
    gy_max = printNewMax(ism.gyro[1], gy_max, "GY")
    gz_max = printNewMax(ism.gyro[2], gz_max, "GZ")

    if k == 10:
        k = 0
        print("Accel X:%.2f Y:%.2f Z:%.2f ms^2 \nGyro X:%.2f Y:%.2f Z:%.2f degrees/s \n"
            % (ism.acceleration + ism.gyro))

    # timer que se cumple cada 1s
    timerObject = threading.Timer(1, icm20649_ISSR)  
    # Empieza a funcionar el timer
    timerObject.start()

icm20649_ISSR()














#################################################3
st = time.monotonic()
while time.monotonic() - st < 2:

    print(
        "Accel X:%.2f Y:%.2f Z:%.2f ms^2 \nGyro X:%.2f Y:%.2f Z:%.2f degrees/s \n"
        % (ism.acceleration + ism.gyro)
    )

    ax_max = printNewMax(ism.acceleration[0], ax_max, "AX")
    ay_max = printNewMax(ism.acceleration[1], ay_max, "AY")
    az_max = printNewMax(ism.acceleration[2], az_max, "AZ")

    gx_max = printNewMax(ism.gyro[0], gx_max, "GX")
    gy_max = printNewMax(ism.gyro[1], gy_max, "GY")
    gz_max = printNewMax(ism.gyro[2], gz_max, "GZ")