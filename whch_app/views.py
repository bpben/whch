from flask import render_template
from whch_app import app
from flask import request
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import psycopg2
import tempfile
import gzip
from datetime import datetime

#User parsing functions
from format_input import format_input

#Output functions
import StringIO
import base64
from plotter import plotter

#Read in postgres details
with open('postgres','rb') as f:
    login = []
    for line in f.readlines():
        login.append(line.strip('\n'))
user,host,pw,dbname = login
db = create_engine('postgres://%s:%s@%s/%s'%(user,pw,host,dbname))

#Read in pickled prediction models
import cPickle
from glob import glob
targetsTrans = {'huf':'HuffingtonPost', 
                'fox':'FoxNews', 
                'ap':'AssociatedPress', 
                'reu':'Reuters', 
                'was':'WashingtonPost'}
targetsCol = {'huf':'#4878CF', 
                'fox':'#6ACC65', 
                'ap':'#D65F5F', 
                'reu':'#B47CC7', 
                'was':'#C4AD66'}
target_m = {}
files = glob('whch_app/*model.pkl')


@app.route('/')
def test():
    return render_template('index.html')

@app.route('/louisiana')
def louisiana():
    features = ['actor1code', 'actor1countrycode', 'actor1knowngroupcode', 'actor1ethniccode', 'actor1religion1code', 'actor1religion2code',
     'actor1type1code', 'actor1type2code', 'actor1type3code', 'actor2code', 'actor2countrycode', 'actor2knowngroupcode',
     'actor2ethniccode', 'actor2religion1code', 'actor2religion2code', 'actor2type1code', 'actor2type2code', 'actor2type3code',
     'isrootevent', 'eventcode', 'eventbasecode', 'eventrootcode', 'actor1geo_countrycode', 'actor2geo_countrycode',
     'actiongeo_countrycode']

    #formatted = format_input(db, '',features,example='LOUISIANA')
    
    #newRows,df_m = formatted
    #Pre-defined estimates, for fast example
    pre_def = ['fox','was','huf','ap','reu']
    preds = [5,4,3,2,1]
    targs = []
    targs_c = []
    for p in pre_def:
        targs.append(targetsTrans[p])
        targs_c.append(targetsCol[p])
    #Create ranking list
    ranks = sorted(zip(preds,targs,targs_c),reverse=True)
    
    #img = StringIO.StringIO()
    #plots = plotter(df_m,'Louisiana')
    #print plots
    #plots.savefig('/Users/B/Documents/whch/louisiana', format='png', transparent=True)
    
    #img.seek(0)
    with open('louisiana','rb') as png:
        plot_url = base64.b64encode(png.read())
    return render_template('output.html', plot_url=plot_url, 
                           name='Louisiana',
                          ranks = ranks)

@app.route('/syria')
def syria():
    features = ['actor1code', 'actor1countrycode', 'actor1knowngroupcode', 'actor1ethniccode', 'actor1religion1code', 'actor1religion2code',
     'actor1type1code', 'actor1type2code', 'actor1type3code', 'actor2code', 'actor2countrycode', 'actor2knowngroupcode',
     'actor2ethniccode', 'actor2religion1code', 'actor2religion2code', 'actor2type1code', 'actor2type2code', 'actor2type3code',
     'isrootevent', 'eventcode', 'eventbasecode', 'eventrootcode', 'actor1geo_countrycode', 'actor2geo_countrycode',
     'actiongeo_countrycode']

    #formatted = format_input(db, '',features,example='SYRIA')
    
    #newRows,df_m = formatted
    #Pre-defined estimates, for fast example
    pre_def = ['reu','ap','was','huf','fox']
    preds = [5,4,3,2,1]
    targs = []
    targs_c = []
    for p in pre_def:
        targs.append(targetsTrans[p])
        targs_c.append(targetsCol[p])
    #Create ranking list
    ranks = sorted(zip(preds,targs,targs_c),reverse=True)
    
    #img = StringIO.StringIO()
    #plots = plotter(df_m,'Syria')
    #print plots
    #plots.savefig('/Users/B/Documents/whch/syria', format='png', transparent=True)
    
    #img.seek(0)
    with open('syria','rb') as png:
        plot_url = base64.b64encode(png.read())
    return render_template('output.html', plot_url=plot_url, 
                           name='Syria',
                          ranks = ranks)

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
    formatted = format_input(db, request.args.get('name').upper(),features)
    
    if formatted is None:
        return render_template('index.html', error="No results found for {}, try searching something else".format(request.args.get('name')))
    
    newRows,df_m = formatted
    preds = []
    targs = []
    targs_c = []
    for f in files:
        print f
        targ = f.split('/')[-1].split('_')[0]
        targs.append(targetsTrans[targ])
        targs_c.append(targetsCol[targ])
        with open(f, 'rb') as infile:
            target_m = cPickle.load(infile)
        preds.append(np.mean(target_m.predict_proba(newRows)[:,1]))
    #Create ranking list
    ranks = sorted(zip(preds,targs,targs_c),reverse=True)
    
    img = StringIO.StringIO()
    #vplot = plt.figure(tight_layout=True)
    plots = plotter(df_m,request.args.get('name'))
    plots.savefig(img, format='png', transparent=True)
    
    img.seek(0)

    plot_url = base64.b64encode(img.getvalue())
    
    
    #img = StringIO.StringIO()
    #tplot = plt.figure(tight_layout=True)
    #tplot = toneplot(df_m, request.args.get('name'))
    #tplot.figure.savefig(img, format='png', transparent=True)

    #img.seek(0)

    #tplot_url = base64.b64encode(img.getvalue())

    return render_template('output.html', plot_url=plot_url, 
                           name=request.args.get('name'),
                          ranks = ranks)