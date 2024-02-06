import paho.mqtt.client as mqtt
from random import uniform
import numpy as np
import time

mqtt_broker = 'mqtt.eclipseprojects.io'
mqtt_client = mqtt.Client('MQTTProducer')
mqtt_client.connect(mqtt_broker)

while True:

    agents = [
                [-8.056767, -34.973094], # agent 1
                [-8.056868, -34.972864], # agent 2
                [-8.056836, -34.972440], # agent 3
                [-8.056448, -34.972236], # agent 4
                [-8.056576, -34.971968], # agent 5
                [-8.056469, -34.971657]  # agent 6
            ]
    agent_id = 1
    for agent in agents:
        lat = agent[0] - (np.random.randint(5, 10)/1000000)
        lon = agent[1] - (np.random.randint(5, 10)/1000000)
        position_msg = f'agent {agent_id} lat {lat} lon {lon}'

        mqtt_client.publish('position', position_msg)
        print(f'MQTT message: {position_msg}') 
        agent_id = agent_id + 1   
    
    factors = np.random.randint(1, [2, 2, 2, 3, 3, 2, 2, 3, 2, 2])
    normal = [np.round(np.random.uniform(20, 30), 0) for i in range(10)]

    rands = normal * factors

    for rand in rands:
        env = np.random.randint(1, 10)
        temperature_msg = f'env {env} value {rand}'

        mqtt_client.publish('temperature', temperature_msg)
        print(f'MQTT message: {temperature_msg}')
    time.sleep(1)