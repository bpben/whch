
# coding: utf-8

# In[1]:

#Script for making new observations for prediction
#Reads in dictionary input, outputs rows of every possible combination for prediction
from copy import copy
import itertools
import cPickle
import re
import pandas as pd
import itertools

def format_input(new,features):
    #Read in sklearn encoder
    with open('/Users/B/gdelt/testing/sklearn_encoder.pkl','rb') as infile:
        encodes = cPickle.load(infile)
    outList = []
    possible = []
    for k in encodes:
        codecols = [x for x in features if re.search(k,x)is not None]
        if k in new:
            if new[k] is not None:
                for i in codecols:
                    out = {}
                    out[i] = encodes[k].transform(new[k])
                    possible.append(out)
    
    for comb in itertools.combinations(possible,3):
        #print comb
        row = {}
        for c in comb:
            print c
            row.update(c)
        for i in features:
            if i not in row:
                #print i
                row[i] = 0
        outList.append(row)
    return(pd.DataFrame(outList))