# subscriber
import paho.mqtt.client as mqtt

# Funcion de conexion. 
# Al realizarse la conexion con el broker se imprime el return code (rc)
def on_connect(mqttc, obj, flags, rc):
    if rc == 0:
        print("Conexion establecida con el broker (rc:" + str(rc) + ")")
    else:
        print("Fallo de la conexion (rc:" + str(rc) + ")")

def on_message(mqttc, obj, msg):
    msg.payload = msg.payload.decode("utf-8")
    print(msg.topic + " " + str(msg.payload) + " (qos:" + str(msg.qos) + ")")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Create connection, the three parameters are broker address, 
# broker port number, and keep-alive time respectively
client.connect("192.168.2.203", 1883, 60)
client.subscribe("ms5837/temp")
client.subscribe("ms5837/press")

# set the will message, when the Raspberry Pi is powered off, 
# or the network is interrupted abnormally, it will send the 
# will message to other clients
# client.will_set('ms5837/temp', '{"status": "Off"}')


# client.loop_start()

# set the network loop blocking, it will not actively end the 
# program before calling disconnect() or the program crash
client.loop_forever()
#client.loop_stop()
# client.disconnect()