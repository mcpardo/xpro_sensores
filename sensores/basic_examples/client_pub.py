# publisher
import paho.mqtt.client as mqtt
import time
import sys

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conexion establecida con el broker")
    else:
        print(f"Fallo de la conexion con codigo {rc}")

client = mqtt.Client()
client.on_connect = on_connect

# create connection, the three parameters are broker address, 
# broker port number, and keep-alive time respectively
client.connect("192.168.2.203", 1883, 60)
#client.loop_start()

while True:
    client.publish('tests/test1', payload="on", qos=0, retain=False)
    print(f"send on to topic tests/test1")
    time.sleep(10)
    client.publish('tests/test1', payload="off", qos=0, retain=False)
    print(f"send off to tests/test1")
    time.sleep(10)

# set the network loop blocking, it will not actively end the 
# program before calling disconnect() or the program crash
client.loop_forever()