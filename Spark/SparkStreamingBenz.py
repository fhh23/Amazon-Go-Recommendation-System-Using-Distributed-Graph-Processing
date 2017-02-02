#!/usr/bin/env pyspark

from __future__ import print_function

import os
import pyspark
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from tdigest import TDigest
import pprint
from pyspark import SparkContext, SparkConf

def digest_partitions(values):
    digest = TDigest()
    digest.batch_update(values)
    return [digest]

sc = SparkContext(appName='streamingFromKafka')
ssc = StreamingContext(sc, 2)
# Set the Kafka topic
topic = 'fh-topic'

# List the Kafka Brokers
broker_file = open('brokers.txt', 'r')
kafka_brokers = broker_file.read()[:-1]
broker_file.close()
kafkaBrokers = {"metadata.broker.list": "ec2-35-166-31-140.us-west-2.compute.amazonaws.com:9092"}

# Create input stream that pull messages from Kafka Brokers (DStream object)
trans = KafkaUtils.createDirectStream(ssc, [topic], kafkaBrokers)
counts = trans.map(lambda x: x[1]).foreachRDD(lambda RDD: print(RDD.collect()))
counts = trans.flatMap(lambda line: line.split(","))
#[-4]) \
 #       .map(lambda word: (word, 1)) \
  #      .reduceByKey(lambda a, b: a+b)
		
# Printing kafkastream content 
counts.pprint()

ssc.start()
ssc.awaitTermination()