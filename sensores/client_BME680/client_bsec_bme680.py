################################################################################
# LIBRERIAS
################################################################################
import subprocess
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import json
from statistics import median
from datetime import datetime


################################################################################
# CONEXION MQTT
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
# LLAMADA Y LECTURA DE PROGRAMA EN C
################################################################################
bufferSize = 1

#Open C File
proc = subprocess.Popen(['bsec_bme680/bsec_bme680'], stdout=subprocess.PIPE)

listIAQ_Accuracy = []
listPressure = []
listGas = []
listTemperature = []
listIAQ = []
list_sIAQ = []
listHumidity  = []
listStatus = []

for line in iter(proc.stdout.readline, ''):
    lineJSON = json.loads(line.decode("utf-8")) # process line-by-line
    lineDict = dict(lineJSON)

    listIAQ_Accuracy.append(int(lineDict['IAQ_Accuracy']))
    listPressure.append(float(lineDict['Pressure']))
    listGas.append(int(lineDict['Gas']))
    listTemperature.append(float(lineDict['Temperature']))
    listIAQ.append(float(lineDict['IAQ']))
    list_sIAQ.append(float(lineDict['sIAQ']))
    listHumidity.append(float(lineDict['Humidity']))
    listStatus.append(int(lineDict['Status']))

    if len(listIAQ_Accuracy) == bufferSize:
        #generate the median for each value
        IAQ_Accuracy = median(listIAQ_Accuracy)
        Pressure = median(listPressure)
        Gas = median(listGas)
        Temperature = median(listTemperature)
        IAQ = median(listIAQ)
        sIAQ = median(list_sIAQ)
        Humidity = median(listHumidity)
        Status = median(listStatus)

        #clear lists
        listIAQ_Accuracy.clear()
        listPressure.clear()
        listGas.clear()
        listTemperature.clear()
        listIAQ.clear()
        list_sIAQ.clear()
        listHumidity.clear()
        listStatus.clear()

        #Temperature Offset
        #Temperature = Temperature + 2

        ################################################################################
        # PUBLICACION DE MEDIDAS
        ################################################################################
        payload = {"IAQ_Accuracy": IAQ_Accuracy,"IAQ": round(IAQ, 2),"sIAQ": round(sIAQ, 2),"Temperature (degC)": round(Temperature, 2),"Humidity (rH)": round(Humidity, 2),"Pressure (mbar)": round(Pressure, 2),"Gas (ohm)": Gas,"Status": Status}
        
        # Marca de tiempo
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        
        publish.single("bme680", json.dumps(payload), hostname=hostname)
        print("Published new BME680 data" + " (" + current_time + ")")
        # Para imprimir los datos por la consola:
        print(lineJSON)
        print("\n")