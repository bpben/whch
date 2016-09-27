
#Script for making volume plots

def volumeplot(df_m,new):
    import pandas as pd
    import seaborn as sns
    sns.set_style("white")
    
    df_m['sqldate'] = pd.to_datetime(df_m['sqldate'])
    df_m = df_m.reset_index().groupby('globaleventid')['sqldate','huf', 'fox', 'ap', 'reu', 'was'].max()
    df_m = df_m.groupby('sqldate')['huf', 'fox', 'ap', 'reu', 'was'].sum()
    ax = df_m['2016-07':].plot(kind='area',alpha=.7,
                          title='Number of stories about '+new)
    ax.set_axis_bgcolor('w')
    ax.set_xlabel('')
    ax.set(yticklabels=[])
    ax.set_ylabel('# of stories')
    
    sns.despine(left=True, bottom=True, right=True)
    #return(ax)