import paho.mqtt.client as mqttclient
import time

def on_connect(client,userdata,flags,rc):
    if rc==0:
        print("client is connected")
        global connected
        connected = True
    else:
        print("connection failed")

def on_message(client, userdata, message):
    print("Message received: " + str(message.payload.decode("utf-8")))
    print("Topic: " + str(message.topic))

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))


connected = False
messageReceived = False

broker_address = "broker.mqttdashboard.com" #adresse
port = 1883 #port
user = None #user si besoin
password = None #password si besoin

client = mqttclient.Client()
client.connect(broker_address, port)
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe
client.subscribe("c64/api/testzone", qos=1)
print("allo")

client.loop_start()

while connected != True:
    time.sleep(0.2)

client.publish("c64/api/testzone", "hello world")

while messageReceived != True:
    time.sleep(0.2)

client.loop_stop()


