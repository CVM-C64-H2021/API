import paho.mqtt.client as mqtt
import os, urllib.parse, os.path
import json
import base64
from RESTAPI.SII_API.models import Sii_Api
from datetime import date

class connectionMQTT():

    def __init__(self, url, topic):
        self.mqttc = mqtt.Client()
        
        # Parse CLOUDMQTT_URL (or fallback to localhost)
        self.url_str = os.environ.get('CLOUDMQTT_URL', url)
        self.url = urllib.parse.urlparse(self.url_str)
        self.topic = self.url.path[1:] or topic

        self.connection()

    def on_message(self, client, obj, msg):
        message = json.dumps(msg)
        print(message) ##### string? 

        #on appelerait la classe venant de django.models pour saver le post dans la db
        
        post = Sii_Api.objects.create(
            m_date = date.today(),
            m_type = "image",
            m_value = str(message.payload.decode("utf-8")),
            m_alert = 1,
            m_msg = "Cette personne a voulu manger vos biscuits!!!"
        )
        post.save()
        
        transformJSON(message)

    def connection(self):
        # Connect
        self.mqttc.username_pw_set(self.url.username, self.url.password)
        self.mqttc.connect(self.url.hostname, self.url.port)

        # Start subscribe, with QoS level 0
        self.mqttc.subscribe(self.topic, 0)

    def transformJSON(message):
        with open('brooker/data.json', 'w') as outfile:
            json.dump(message, outfile)
    

    def publish(self, image, date):
        # Publish a message

        faceDict = {}
        faceDict["id"] = 123
        faceDict["m_date"] = "date"
        faceDict["m_type"] = "image"
        faceDict["m_valeur"] = "base64.b64encode(image).decode(utf-8)"
        faceDict["m_alerte"] = 1
        faceDict["m_messageAlerte"] = "Cette personne a voulu manger vos biscuits!!!"

        """ #test
        f = open("test.txt", "w")
        f.write(str(base64.b64encode(image).decode("utf-8")))
        f.close()
        """
        message = json.dumps(faceDict)

        self.mqttc.publish(self.topic, message)

        #methode pour reach mongo sur django

    # Continue the network loop, exit when an error occurs
    #rc = 0
    #while rc == 0:
    #    rc = mqttc.loop()
    #print("rc: " + str(rc)) 