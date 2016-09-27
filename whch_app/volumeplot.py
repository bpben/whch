
#Script for making volume plots

def volumeplot(df_m,new):
    import pandas as pd
    import seaborn as sns
    sns.set_style("white")
    
    #fig,ax = plt.subplots(facecolor='white')
    df_m['sqldate'] = pd.to_datetime(df_m['sqldate'])
    df_m = df_m.reset_index().groupby('globaleventid')['sqldate','huf', 'fox', 'ap', 'reu', 'was'].max()
    #df_m = df_m.groupby('sqldate')['huf', 'fox', 'ap', 'reu', 'was'].mean()
    df_m = df_m.groupby('sqldate')['huf', 'fox', 'ap', 'reu', 'was'].sum()
    p = df_m['2016-07':].plot(kind='area',alpha=.7,title='Number of stories about '+new)
    p.set_axis_bgcolor('w')
    p.set_xlabel('')
    p.set(yticklabels=[])
    p.set_ylabel('# of stories')
    
    #p = sns.barplot(y=targs,x=preds)
    sns.despine(left=True, bottom=True, right=True)
    #p.set(xticklabels=[])
    return(p)