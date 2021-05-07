import paho.mqtt.client as mqtt
import os, urllib.parse, os.path
import json
import base64
from datetime import date

class connectionMQTT():

    def __init__(self, url, topic):
        self.mqttc = mqtt.Client()
        
        # Parse CLOUDMQTT_URL (or fallback to localhost)
        #self.url_str = os.environ.get('CLOUDMQTT_URL', url)
        self.url = urllib.parse.urlparse(url)
        self.topic = topic

        self.connection()
        print('init')

    def on_message(self, client, obj, msg):

        from .models import Sii_Api
        from rest_framework.parsers import JSONParser

        udata = json.loads(msg.payload.decode("utf-8"))

        print(type(udata), udata)

        self.updateDB(udata)
        #asciidata = udata.encode("latin1")
        #print(type(udata), udata)
        #udata = asciidata.decode("utf-8")
        #message = json.dumps(udata)
        #print(message) ##### string? 

        #self.transformJSON(message)
        #on appelerait la classe venant de django.models pour saver le post dans la db
        '''
        post = Sii_Api.objects.create(
            date = date.today(),
            type = "image",
            m_value = str(message.payload.decode("utf-8")),
            m_alert = 1,
            m_msg = "Cette personne a voulu manger vos biscuits!!!"
        )
        post.save()
        
        transformJSON(message)
        '''

    def updateDB(self, msg):

        from SII_API.serializers import ApiSerializer
        from rest_framework.parsers import JSONParser
        from django.http.response import JsonResponse
        from rest_framework import status

        serial = ApiSerializer(data=msg)
        #data=json.dumps(msg)
        #data = JSONParser().parse(msg)

        #data = SII_API.objects.all()
        #data = data.filter(idApp == msg["idApp"])
        data = None

        print(serial.is_valid())
        if serial.is_valid():
            if(data == None):
                serial.save()
            else:
                pass
                #serial.put() pour update
            print('yessir miller')
        else:
            print('pas possible')
            print(serial.errors)



    def connection(self):
        # Connect
        print('je me connecte')
        self.mqttc.username_pw_set(self.url.username, self.url.password)
        self.mqttc.connect(self.url.hostname, self.url.port)

        # Start subscribe, with QoS level 0
        self.mqttc.subscribe(self.topic, 0)
        self.mqttc.on_message = self.on_message

    def transformJSON(message):
        with open('brooker/data.json', 'w') as outfile:
            json.dump(message, outfile)
    
    '''
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
    '''