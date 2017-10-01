# Import SDK packages
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json
import RPi.GPIO as GPIO

def onInputCallback(client, userdata, message):
    print "received message "
    print client
    print userdata
    onMessage(message)
    
def onMessage(message):
    print "received message "
    print message
    print "topic: "
    print message.topic
    payload = json.loads(message.payload)

    print "payload: "
    print payload
    if (payload['command'] == 'on'):
        print 'Lights ON'
        GPIO.setup(16, GPIO.OUT, initial = GPIO.HIGH)
    elif (payload['command'] == 'off'):
        print 'Lights OFF'
        GPIO.setup(16, GPIO.OUT, initial = GPIO.LOW)
    else:
        print "Unknown command: " + payload['command']
    

# For certificate based connection
myMQTTClient = AWSIoTMQTTClient("myClientID")
# For Websocket connection
# myMQTTClient = AWSIoTMQTTClient("myClientID", useWebsocket=True)
# Configurations
# For TLS mutual authentication
myMQTTClient.configureEndpoint("a1kai14uhgd0p5.iot.eu-west-1.amazonaws.com", 8883)
# For Websocket
# myMQTTClient.configureEndpoint("YOUR.ENDPOINT", 443)
myMQTTClient.configureCredentials("./credentials/public.cert.pem", "./credentials/private.key", "./credentials/cert.pem")
# For Websocket, we only need to configure the root CA
# myMQTTClient.configureCredentials("YOUR/ROOT/CA/PATH")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(3600)  # (seconds)
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

myMQTTClient.connect()
myMQTTClient.publish("smartlight/device-1/out", '{"message": "Connected!"}', 0)
myMQTTClient.subscribe("smartlight/device-1/in", 1, onInputCallback)
#myMQTTClient.onMessage(onMessage)
#myMQTTClient.unsubscribe("myTopic")
#myMQTTClient.disconnect()

input("Press enter to exit")
