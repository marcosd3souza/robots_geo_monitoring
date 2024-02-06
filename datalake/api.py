import json
from flask import Flask, request
from flask_pymongo import PyMongo
from bson import json_util#, ObjectId
from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, udf, col
from geopy import distance
import numpy as np

MONGODB_URI = 'mongodb://db-mongo:27017/datalake'
api = Flask(__name__)
api.config["MONGO_URI"] = MONGODB_URI
mongo = PyMongo(api)
spark = SparkSession.builder.appName("JsonData").getOrCreate()

def parse_json(data):
    return json.loads(json_util.dumps(data))

@api.route('/')
def check():
    return 'Its OK!'

# from pyspark.sql import SparkSession
# from pyspark.sql.functions import avg
# import requests
# import json
# data = requests.get('http://localhost:5000/messages').json()
# spark = SparkSession.builder.appName("JsonData").getOrCreate()
# raw_data = spark.read.json(spark.sparkContext.parallelize([json.dumps(data)]))
# position_df = raw_data[raw_data['topic']=='position']
# position_df.collect()[0].message
# position_df = position_df.withColumn("emp_id", udf(lambda x: int(x.split(' ')[1]))(col("message")))
# position_df = position_df.withColumn("lat", udf(lambda x: float(x.split(' ')[3]))(col("message")))
# position_df = position_df.withColumn("long", udf(lambda x: float(x.split(' ')[-1]))(col("message")))
# position_df_clean = position_df[['emp_id', 'lat', 'long']]
# result = position_df_clean.groupby('emp_id').agg(avg('lat').alias('Avg_lat'), avg('long').alias('Avg_long'))
# result.toJSON().collect()

@api.route('/positions', methods=['GET'])
def get_emp_positions():
    data = list(mongo.db.messages.find({"topic":'position'}))
    position_df = spark.read.json(spark.sparkContext.parallelize([json_util.dumps(data)]))

    position_df = position_df.withColumn("agent_id", udf(lambda x: int(x.split(' ')[1]))(col("message")))
    position_df = position_df.withColumn("lat", udf(lambda x: float(x.split(' ')[3]))(col("message")))
    position_df = position_df.withColumn("long", udf(lambda x: float(x.split(' ')[-1]))(col("message")))
    df = position_df[['agent_id', 'lat', 'long']]
    df_arr = np.array(df.collect(), dtype=float)

    result = df.groupby('agent_id').agg(avg('lat').alias('Avg_lat'), avg('long').alias('Avg_long'))
    res_arr = np.array(result.collect(), dtype=float)

    dist_avg = np.array([(lambda a: [a[0], np.mean([distance.distance(a[1:], b[1:]).meters for b in df_arr if a[0] == b[0]])])(a) for a in res_arr])
    dist_max = np.array([(lambda a: [a[0], np.max([distance.distance(a[1:], b[1:]).meters for b in df_arr if a[0] == b[0]])])(a) for a in res_arr])
    # result = result.toJSON().map(lambda j: json.loads(j)).collect()
    
    response = []
    for agent_idx in [r[0] for r in res_arr]:
        avg_lat = res_arr[[r[0] == agent_idx for r in  res_arr]][0][1]
        avg_lon = res_arr[[r[0] == agent_idx for r in  res_arr]][0][2]
        avg_dis = dist_avg[[a[0] == agent_idx for a in dist_avg]][0][1]
        max_dis = dist_max[[a[0] == agent_idx for a in dist_max]][0][1]

        response.append({
            "agent_id" : int(agent_idx),
            "avg_lat"  : np.round(avg_lat, 6),
            "avg_lon"  : np.round(avg_lon, 6),
            "avg_dis"  : np.round(avg_dis, 3),
            "max_dis"  : np.round(max_dis, 3)
        })
    
    return parse_json(response), 200

@api.route('/messages', methods=['GET'])
def get_all_items():
    messages = list(mongo.db.messages.find())
    return parse_json(messages), 200

@api.route('/messages', methods=['POST'])
def create_item():
    message = request.get_json()
    inserted_msg = mongo.db.messages.insert_one(message)
    return parse_json(inserted_msg.inserted_id), 201

if __name__ == "__main__":
    api.run(debug=True)