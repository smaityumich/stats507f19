# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 19:35:27 2019

@author: Subha Maity
"""

from mrjob.job import MRJob
from mrjob.step import MRStep
import re
import functools

class MRSummaryStat(MRJob):

    def steps(self):
        return [
	    MRStep(mapper=self.mapper_map,
		   combiner=self.combiner_combine,
		   reducer=self.reducer_reduce)]
    
    def mysum(self, x, y):
        if len(x) != len(y):
	        raise ValueError('Length of arrays are not same')
        else:
	        return [x[i]+y[i] for i in range(len(x))]

    def mapper_map(self, _, line):
        pair = re.split(r'\s',line)
        x = float(pair[1])
        yield int(pair[0]), x
        
    def combiner_combine(self, key, value):
        y = list(value)
        yield key, [sum(y), sum([x**2 for x in y]), len(y)]
        
    def reducer_reduce(self, key, value):
        values = list(value)
        summary = functools.reduce(self.mysum, values, [0,0,0])
        n = summary[2]
        mean = summary[0]/n
        variance = summary[1]/n - mean**2 ##denominator n
        yield key, [n, mean, variance]
        
if __name__ == '__main__':
    MRSummaryStat.run()
