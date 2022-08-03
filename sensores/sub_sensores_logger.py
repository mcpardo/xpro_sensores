# subscriber
import paho.mqtt.client as mqtt
import datetime
import time

hostname = "192.168.2.203"

# Funcion de conexion. 
# Al realizarse la conexion con el broker se imprime el return code (rc)
def on_connect(mqttc, obj, flags, rc):
    if rc == 0:
        print("Conexion establecida con el broker (rc:" + str(rc) + ")")
    else:
        print("Fallo de la conexion (rc:" + str(rc) + ")")

def on_disconnect(client, userdata, flags, rc):
    print("Desconexion del broker (rc:" + str(rc) + ")")

def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_message(mqttc, obj, msg):
    now = datetime.datetime.now()
    msg.payload = msg.payload.decode("utf-8")
    print(msg.topic + " " + str(msg.payload) + " (qos:" + str(msg.qos) + ")")
    # Guardado de datos en un archivo
    filename = (msg.topic.replace("/","_") + ".txt")
    file = open("loggers/" + filename, 'a+')
    file.write(now.strftime("%Y %m %d %H %M %S") + " | topic: " + msg.topic + " | mensaje: " + str(msg.payload) + "\n")
    file.close()

client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.on_subscribe = on_subscribe

# set the will message, when the Raspberry Pi is powered off, 
# or the network is interrupted abnormally, it will send the 
# will message to other clients
# client.will_set('ms5837/temp', '{"status": "Off"}')

# Create connection, the three parameters are broker address, 
# broker port number, and keep-alive time respectively
client.connect(hostname, 1883, 60)
client.subscribe("bme680")
client.subscribe("ms5837")
client.subscribe("icm20649")
client.subscribe("test/mc")

# client.loop_start()

# set the network loop blocking, it will not actively end the 
# program before calling disconnect() or the program crash
client.loop_forever()
#client.loop_stop()
# client.disconnect()