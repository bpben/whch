#Script for making new observations for prediction
#Reads in dictionary input, outputs rows of every possible combination for prediction
import cPickle
import re
import pandas as pd
from datetime import datetime

def format_input(db,new,features,example=None):
    if example is not None:
        df = pd.read_sql('''
                SELECT * FROM {} 
                order by sqldate desc
                '''.format(example.lower()),db)
        df_m = pd.read_sql("""
                select globaleventid,sqldate,tone,
                            ap, huf, was, fox, reu from {}
                """.format(example.lower()+'_mention'),db)
        print len(df_m)
    else:
        location = 0
        df = pd.read_sql('''
                    SELECT * FROM {} 
                    where 
                    (actor1name like '{}' or actor2name like '{}')
                    order by sqldate desc
                    '''.format('gd_eventsb',new,new),db)
        #If it finds nothing for actor, try location
        if len(df)==0:
            location = 1
            new = '%{}%'.format(new)
            df = pd.read_sql('''
                    SELECT * FROM {} 
                    where 
                    (actor1geo_fullname ilike '%{}%' 
                    or 
                    actor2geo_fullname ilike '%{}%'
                    or
                    actiongeo_fullname ilike '%{}%')
                    order by sqldate desc
                    '''.format('gd_eventsb',new,new,new),db)
            if len(df)==0:
                return(None)
        print 'events done {}'.format(datetime.now())
        print df.head()
        df.globaleventid = df.globaleventid.astype('int64')
        eventids = tuple(str(x) for x in df.globaleventid.values)

        #Get mentions data
        #Check if search by location
        if location == 1:
            df_m = pd.read_sql("""
                    select globaleventid,sqldate,tone,
                            ap, huf, was, fox, reu from {} 
                    where 
                    (actor1geo_fullname ilike '%{}%' 
                    or 
                    actor2geo_fullname ilike '%{}%'
                    or
                    actiongeo_fullname ilike '%{}%')
                    """.format('mentions_plus',new,new,new),db)
        else:
            df_m = pd.read_sql("""
                    select globaleventid,sqldate,tone,
                            ap, huf, was, fox, reu from {} 
                    where 
                    (actor1name like '{}' or actor2name like '{}')
                    """.format('mentions_plus',new,new),db)
    print 'mentions done {}'.format(datetime.now())
    
    #Read in sklearn encoder
    with open('whch_app/sklearn_encoder.pkl','rb') as infile:
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
                
    #predict,visual sets
    print 'format done {}'.format(datetime.now())
    return(df[features].iloc[0:10],df_m)