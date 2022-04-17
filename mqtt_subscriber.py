import paho.mqtt.client as mqtt
import time
import re
import json
import notecard
import notecard_pseudo_sensor
from periphery import I2C

### HELPERS ###
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe([("esp32_tempval", 1)])#, ("esp32/topic2", 1), ("esp32/topic3", 1)])


def on_message(client, userdata, message):
    #print("Message received: " + message.topic + " : " + str(message.payload))
    msg = str(message.payload)
    msg = re.split('\W+', msg)
    #print(msg)
    temp = msg[-2]
    #with open('./mqtt_update.txt', 'a+') as f:
        #f.write(msg)
        #f.write('\n')
    # publish data to notehub
    req = {"req": "note.add"}
    req["file"] = "sensors.qo"
    req["sync"] = True # sync to Notehub immediately
    req["body"] = { message.topic: temp }#, "humidity": humidity }
    rsp = card.Transaction(req)
    print(rsp)

### GLOBALS ###
broker_address = "localhost"  # Broker address
port = 1883  # Broker port
# user = "yourUser"                    #Connection username
# password = "yourPassword"            #Connection password
productUID = "edu.cmu.andrew.tanvib:home_monitoring"

### INIT I2C AND NOTECARD ###
i2cPort = I2C("/dev/i2c-1")
card = notecard.OpenI2C(i2cPort, 0, 0)

req = {"req": "hub.set"}
req["product"] = productUID
req["mode"] = "continuous" # can set this to periodic, then set req["outbound"] and inbound to numbers (prob seconds)
print(json.dumps(req))
rsp = card.Transaction(req)
print(rsp)

### CLIENT CODE ###
client = mqtt.Client()  # create new instance
# client.username_pw_set(user, password=password)    #set username and password
client.on_connect = on_connect  # attach function to callback
client.on_message = on_message  # attach function to callback

client.connect(broker_address, port=port)  # connect to broker

client.loop_forever()
