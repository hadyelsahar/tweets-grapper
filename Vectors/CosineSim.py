#!/usr/bin/env python
#encoding:utf-8 

import regex, math
from collections import Counter

'''
Created on Oct 31, 2013
python 2.7.3 
@author: hadyelsahar 
'''
class CosineSim:
  
  def get_cosine(self, text1, text2):
    
    vec1 = self.text_to_vector(text1)
    vec2 = self.text_to_vector(text2)  

    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
      return 0.0
    else:
      return float(numerator) / denominator

  @staticmethod
  def text_to_vector(text):
    words = text.strip().split(" ")
    return Counter(words)