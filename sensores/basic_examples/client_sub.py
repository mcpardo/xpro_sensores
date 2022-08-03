# subscriber
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conexion establecida con el broker")
    else:
        print(f"Fallo de la conexion con codigo {rc}")
    # subscribe, which need to put into on_connect
    # if reconnect after losing the connection with the broker, 
    # it will continue to subscribe to the raspberry/topic topic
#    client.subscribe("vigilancia/cam_manual")
#    client.subscribe("vigilancia/presence")

# the callback function, it will be triggered when receiving messages
def on_message(client, userdata, msg):
    msg.payload = msg.payload.decode("utf-8")
    print(f"{msg.topic} {msg.payload}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# set the will message, when the Raspberry Pi is powered off, 
# or the network is interrupted abnormally, it will send the 
# will message to other clients
client.will_set('tests/test1', '{"status": "Off"}')

# create connection, the three parameters are broker address, 
#broker port number, and keep-alive time respectively
client.connect("192.168.2.203", 1883, 60)
client.loop_start()

client.subscribe("tests/test1")

# set the network loop blocking, it will not actively end the 
# program before calling disconnect() or the program crash
client.loop_forever()
#client.loop_stop()
client.disconnect()


