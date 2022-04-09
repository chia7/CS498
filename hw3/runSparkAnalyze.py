import findspark
findspark.init()

import pyspark
import sys
import json


if len(sys.argv) != 3:
  raise Exception("Exactly 2 arguments are required: <wordList> <charWeight>")


inputUri="/home/chiachi102/WAR_AND_PEACE.txt"
outputUri="/home/chiachi102/output.txt"


wordList=json.loads(sys.argv[1])
charWeight=json.loads(sys.argv[2])

def myTestFunc(line):
  lineLower = line.strip().lower()
  if len(lineLower) == 0:
    return []

  lineWords = lineLower.split()

  score = 0
  for ch in lineLower:
    if ch in charWeight:
      score += charWeight[ch]
  return [(word, (score, line)) for word in wordList if word in lineWords]

  
def myReduceFunc(v1, v2):
  return max(v1, v2)

sc = pyspark.SparkContext()
lines = sc.textFile(inputUri)

lineScore = lines.flatMap(myTestFunc)

bestLine = lineScore.reduceByKey(myReduceFunc)
results = bestLine.take(len(wordList))

output = {}
for w, (s, l) in results:
  output[w] = l

with open(outputUri, 'w', encoding='utf8') as json_file:
  json.dump(output, json_file, ensure_ascii=False)