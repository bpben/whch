
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

def format_input(db,new,features):
    df = pd.read_sql('''
                SELECT * FROM {} TABLESAMPLE SYSTEM (10)
                where 
                (actor1name like '{}' or actor2name like '{}'
                )
                '''.format('gd_eventsb',new,new),db)
    
    #Read in sklearn encoder
    with open('/Users/B/gdelt/testing/sklearn_encoder.pkl','rb') as infile:
        encodes = cPickle.load(infile)
    
    #Ensure all observations mention a country/type that's in the codebook
    drops = []
    for k in encodes:
        for i in df.filter(regex=k).columns:
            drops += list(df[~df[i].isin(encodes[k].classes_)].index)
    drops = set(drops)
    df.drop(list(drops),inplace=True)
    
    #List of colnames, by category
    col2code = {}
    for k in encodes:
        for i in list(df.filter(regex=k).columns):
            col2code[i] = k
    
    #Encode variables
    print "Encoding"
    remove = []
    for f in features:
        if df[f].dtype not in ('int64', 'float64'):
            if re.search('act',f) is not None:
                #If one of our categories, use label encoder
                if f in col2code:
                    df[f] = encodes[col2code[f]].transform(df[f])
                #Otherwise, Just do cat codes
                else:
                    df[f] = 0
            else:
                df[f] = df[f].astype('float64')
                
    return(df[features])