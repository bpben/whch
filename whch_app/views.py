from flask import render_template
from whch_app import app
from flask import request
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import psycopg2
import tempfile

#User parsing functions
from format_input import format_input

#Output functions
import StringIO
import base64
from barplot import barplot

#Read in postgres
with open('postgres','rb') as f:
    login = []
    for line in f.readlines():
        print line
        login.append(line.strip('\n'))
user,host,pw,dbname = login
#user = 'B' #add your username here (same as previous postgreSQL)                      
#host = 'localhost'
#pw = 'postgres'
#dbname = 'gdelt'
db = create_engine('postgres://%s:%s@%s/%s'%(user,pw,host,dbname))

con = psycopg2.connect(database = dbname, user = user)

#Read in pickled prediction models
import cPickle
from glob import glob
targets = ['huf', 'fox', 'ap', 'reu', 'was']
target_m = {}
files = glob('/Users/B/gdelt/testing/*model.pkl')
for f in files:
    with open(f,'rb') as infile:
        target_m[f.split('/')[-1].split('_')[0]] = cPickle.load(infile)


@app.route('/')
def test():
    return render_template('index.html')

@app.route('/input')
def fancy_input():
    query = """
               SELECT * FROM gd_codebook;
                """
    choices = [x for x in pd.read_sql_query(query,con).values]
    return render_template("input.html", buttons=choices)

@app.route('/output')
def fancy_output():
    features = ['actor1code', 'actor1countrycode', 'actor1knowngroupcode', 'actor1ethniccode', 'actor1religion1code', 'actor1religion2code',
     'actor1type1code', 'actor1type2code', 'actor1type3code', 'actor2code', 'actor2countrycode', 'actor2knowngroupcode',
     'actor2ethniccode', 'actor2religion1code', 'actor2religion2code', 'actor2type1code', 'actor2type2code', 'actor2type3code',
     'isrootevent', 'eventcode', 'eventbasecode', 'eventrootcode', 'actor1geo_countrycode', 'actor2geo_countrycode',
     'actiongeo_countrycode']
    
    #new = {}
    #new['[0-9]type'] = 
    print request.args
    newRows = format_input(db, request.args.get('name').upper(),features)
    
    preds = []
    targs = []
    for t in target_m:
        targs.append(t)
        preds.append(np.mean(target_m[t].predict_proba(newRows)[:,1]))
    
    img = StringIO.StringIO()
    sns_plot = plt.figure()
    sns_plot = barplot(targs,preds)
    sns_plot.figure.savefig(img, format='png')

    img.seek(0)

    plot_url = base64.b64encode(img.getvalue())

    return render_template('output.html', plot_url=plot_url)