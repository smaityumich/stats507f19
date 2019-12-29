# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 09:37:30 2019

@author: Subha Maity
"""

import re
import itertools


from pyspark import SparkConf, SparkContext
import sys

def map_neighbors(line):
    x = re.findall(r'\d+',line)
    x = [int(y) for y in x]
    if len(x) > 1:
        return x[0], x[1:]
    else:
        return []

def map_two_paths(x):
    y = x[1]
    if len(y)>1:
        z = list(itertools.combinations(y,2))
        return [(x[0],u) for u in z]
    else:
        return []


def sort_tp(x):
    y = [x[0],x[1][0],x[1][1]]
    y.sort()
    return tuple(y), 1




# This script takes two args an input an output

if len(sys.argv) != 3:
    print('Usage: ' + sys.argv[0] + '<in><out>')
    sys.exit(1)
    
inputLoc = sys.argv[1]
outputLoc = sys.argv[2]

conf = SparkConf().setAppName('Triangle Counting')
sc = SparkContext(conf=conf)
#inputloc = hdfs:/var/stats507f19/fof/friends.simple
data = sc.textFile(inputLoc)
neighbors = data.map(map_neighbors)
tp = neighbors.map(map_two_paths)
tp = tp.flatMap(lambda x:x)
tp = tp.map(sort_tp)
tp = tp.reduceByKey(lambda x, y: x+y)
triangle = tp.filter(lambda x: x[1] > 1).map(lambda x: x[0]).map(lambda x: str(x[0])+' '+str(x[1])+' '+str(x[2]))
triangle.saveAsTextFile(outputLoc)
sc.stop()
