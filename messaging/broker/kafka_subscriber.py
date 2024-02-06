from kafka import KafkaConsumer
import requests

consumer = KafkaConsumer(bootstrap_servers='kafka:29092', api_version=(5,4,0))
consumer.subscribe(['temperature', 'position'])

for message in consumer:
    if message is not None:
        msg = str(message.value, "UTF-8")
        # msg = int(msg.decode('utf8'), 16)
        print(f'Kafka topic: {message.topic} message: {msg}')
        obj = {'topic': message.topic, 'message': msg}
        req = requests.post(url='http://api:5000/messages', json=obj)
        print(req.text)