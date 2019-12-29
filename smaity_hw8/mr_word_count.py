# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 14:47:10 2019

@author: Subha Maity
"""

from mrjob.job import MRJob
from mrjob.step import MRStep
import re
bad_char = '~!@#$%^&*()_+-'
rex = re.compile('[%s]' % bad_char)

class MRWordFrequencyCount(MRJob):
    
    def steps(self):
        return [
                MRStep(mapper = self.mapper_get_word,
                       combiner = self.combiner_count_words,
                       reducer = self.reducer_count_words)]
    
    def mapper_get_word(self, _ , line):
        for word in re.findall(r'\w+',line):
            words = re.split(rex,word)
            for s in words:
                if s !='':
                    yield (s.lower(),1)
    
    def combiner_count_words(self, word, count):
        yield (word, sum(count))
    
    def reducer_count_words(self, word, count):
        yield word, sum(count)
        
if __name__ == '__main__':
    MRWordFrequencyCount.run()
