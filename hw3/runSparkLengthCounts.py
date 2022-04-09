import findspark
findspark.init()

import pyspark
import sys


inputUri="/home/chiachi102/WAR_AND_PEACE.txt"
outputUri="/home/chiachi102/output"


def myMapFunc(x):
  return (len(x), 1)
  
def myReduceFunc(v1, v2):
  return v1 + v2


sc = pyspark.SparkContext()
print("Spark Context initialized.")

lines = sc.textFile(inputUri)
lengthCounts = lines.map(myMapFunc).reduceByKey(myReduceFunc)
print("Operations complete.")

lengthCounts.saveAsTextFile(outputUri)
print("Output saved as text file.")