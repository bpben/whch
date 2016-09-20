
# coding: utf-8

# In[1]:

#Script for making new observations for prediction
#Reads in dictionary input, outputs rows of every possible combination for prediction
from copy import copy
import itertools
import cPickle
import re
import pandas as pd

def format_input(new,features):
    #Read in sklearn encoder
    with open('/Users/B/gdelt/testing/sklearn_encoder.pkl','rb') as infile:
        encodes = cPickle.load(infile)
    outList = []
    for k in encodes:
        codecols = [x for x in features if re.search(k,x)is not None]
        if k in new:
            if new[k] is not None:
                out = {}
                for i in codecols:
                    out[i] = encodes[k].transform(new[k])
                    outList.append(copy(out))
    for i in features:
        for row in outList:
            if i not in row:
                row[i] = 0
    return(pd.DataFrame(outList))

