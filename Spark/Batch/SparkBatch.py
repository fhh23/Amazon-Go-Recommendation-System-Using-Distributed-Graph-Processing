from __future__ import print_function

import os
import pyspark
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import pprint
from pyspark import SparkContext, SparkConf
from operator import add
import sys
import boto

percentile_broadcast = None

def splitFunc(rdd):
    import Itemsets
    Itemsets.lineSplit(rdd)

sc = SparkContext(appName='ItemsetsBatch')

# Read in from S3
aws_access_key = os.getenv('AWS_ACCESS_KEY_ID', 'default')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY', 'default')

conn = boto.connect_s3(aws_access_key, aws_secret_access_key)
bucket = conn.get_bucket('fh-data-insight')
data = sc.testFile("s3n://fh-data-insight/*")
print(data.take(5)

bucket_path = "s3n://fh-data-insight/"
for f in bucket:
    rdd = sc.textFile(bucket_path + f.name)
#    print(rdd.take(5))



print("HI \n")
'''
body = data.map(lambda x: x[1])
lines = body.flatMap(lambda bodys: bodys.split("\r\n")) 
word = lines.map(splitFunc) \
            .map(lambda word: (word, 1)) \
            .reduceByKey(lambda a, b: a+b)
            
print_word = word.take(5)
numPartitions = 1 
s = .3
#count = lines.count()
count = 10
threshold = 2#s*count
#split string baskets into lists of items
baskets = lines.map(Itemsets.lineSplit2) \
               .map(lambda (a,b): (int(a), int(b))) \
               .groupByKey() \
               .mapValues(list) \
               .map(lambda x: sorted(x[1]))
print("RDD: \n")
'''
'''
#treat a basket as a set for fast check if candidate belongs
basketSets = baskets.map(set).cache()
#each worker calculates the itemsets of his partition
localItemSets = baskets.mapPartitions(lambda data: [x for y in get_frequent_items_sets(data, threshold/numPartitions).values() for x in y], True)

#for reducing by key later
allItemSets = localItemSets.map(lambda n_itemset: (n_itemset,1)).foreachRDD(lambda rdd: print(rdd.collect()))
#merge candidates that are equal, but generated by different workers


mergedCandidates = allItemSets.reduceByKey(lambda x,y: x).map(lambda (x,y): x).filter(lambda r: len(r) > 0).foreachRDD(lambda rdd: print(rdd.collect()))

#list2 = mergedCandidates.context().sparkContext.accumulator([], ListParam())
#rdd = sc.parallelize(range(10)).map(file_read1).collect()
mergedCandidates.foreachRDD(lambda x: x.map(file_read1))
print(list2.value)
#distribute global candidates to all workers
#candidates = sc.broadcast(mergedC)
f = open("lists.txt", 'r+')
mergedCandidates.filter(lambda r: len(r) > 0).foreachRDD(lambda rdd: print(rdd.collect(), f))
print("NEXT \n", f)
data = f.read().splitlines()#[line.strip() for line in f]
f.truncate()
f.seek(0)
print(data)
print("\n NEXT \n")
candidates = sc.broadcast(data)
'''
#mergedCandidates = mergedCandidates.filter(lambda r: len(r) > 0)
#count actual occurrence of candidates in document
#counts = mergedCandidates.filter(lambda r: len(r) > 0).flatMap(lambda line: (line,1)).foreachRDD(lambda rdd: print(rdd.collect()))    
#counts = basketSets.flatMap(lambda line: [(candidate,1) for candidate in candidates.value if line.issuperset(candidate)])
#filter finalists
'''
finalItemSets = counts.reduceByKey(lambda v1, v2: v1+v2).filter(lambda (i,v): v>=threshold)
#put into nice format
finalItemSets = finalItemSets.map(lambda (itemset, count): ", ".join([str(x) for x in itemset])+"\t("+str(count)+")")
finalItemSets.saveAsTextFiles("spark_out.txt")
#f = open('digest.txt', 'a')
#print(digest.percentile(50), file=f)
#print("\n", file=f)
'''
