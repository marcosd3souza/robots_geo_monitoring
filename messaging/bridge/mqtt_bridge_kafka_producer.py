import paho.mqtt.client as mqtt
# from pykafka import KafkaClient
from kafka import KafkaProducer
import time

mqtt_broker = 'mqtt.eclipseprojects.io'
mqtt_client = mqtt.Client('MQTTBridge')
mqtt_client.connect(mqtt_broker)

producer = KafkaProducer(bootstrap_servers='kafka:29092', api_version=(5,4,0))
# kafka_topic_temperature = kafka_client.topics['temperature']
# kafka_producer_temperature = kafka_topic_temperature.get_sync_producer()

# kafka_topic_position = kafka_client.topics['position']
# kafka_producer_position = kafka_topic_position.get_sync_producer()


def on_message(client, userdata, message):

    msg = message.payload
    
    if message.topic == 'temperature':
        # send to Kafka
        producer.send('temperature', msg)
        print(f'Kafka: published message: {msg}')
    elif message.topic == 'position':
        # send to Kafka
        producer.send('position', msg)
        print(f'Kafka: published message: {msg}')

    producer.flush()
    

# mqtt_client.loop_start()
mqtt_client.subscribe('temperature')
mqtt_client.subscribe('position')
mqtt_client.on_message = on_message
# time.sleep(300)
# mqtt_client.loop_stop()
mqtt_client.loop_forever()