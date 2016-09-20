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

user = 'B' #add your username here (same as previous postgreSQL)                      
host = 'localhost'
pw = 'postgres'
dbname = 'gdelt'
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
@app.route('/index')
def index():
    return render_template("index.html",
       title = 'Home', user = { 'nickname': 'Miguel' },
       )

@app.route('/db')
def tester():
    sql_query = """
		SELECT * FROM gd_events limit 10;                                                                       
                """
    query_results = pd.read_sql_query(sql_query,con)
    item = ""
    for i in range(0,10):
        item += str(query_results.iloc[i])
        item += "<br>"
    return item

@app.route('/db_fancy')
def fancy():
    sql_query = """
               SELECT globaleventid, sourceurl, numarticles FROM gd_events limit 10;
                """
    query_results=pd.read_sql_query(sql_query,con)
    rows = []
    for i in range(0,query_results.shape[0]):
        rows.append(dict(globaleventid=query_results.iloc[i]['globaleventid'], sourceurl=query_results.iloc[i]['sourceurl'], numarticles=query_results.iloc[i]['numarticles']))
    return render_template('test.html',rows=rows)

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

'''
@app.route('/output')
def fancy_output():
    #pull 'birth_month' from input field and store it
    event = request.args.get('groupid').upper()
    #just select the events that the user inputs
    query = """
               SELECT * FROM gd_events where actor1code = '%s' limit 100;
                """ % event
    print query
    query_results=pd.read_sql_query(query,con)
    print query_results
    rows = []
    for i in range(0,query_results.shape[0]):
        rows.append(dict(actor=query_results.iloc[i]['actor1name'], sourceurl=query_results.iloc[i]['sourceurl'], group=query_results.iloc[i]['actor1code']))
        the_result = ''
    return render_template("output.html", rows = rows, the_result = the_result)
'''