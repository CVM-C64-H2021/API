from brooker import fileBrooker

mqtt = fileBrooker.connectionMQTT('mqtt://ghhtzpps:MwVNHJbYYirC@driver-01.cloudmqtt.com:18760', '/C64/Projet/Equipe1/Capteur')

mqtt.client.loop_start()