def plotter(df_m,new):
    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt
    from numpy import NaN
    sns.set_style("white")
    
    df_m['sqldate'] = pd.to_datetime(df_m['sqldate'])
    df_m.reset_index(inplace=True)
    
    plt.figure(tight_layout=True)
    ax = plt.subplot(2,1,1) 

    df_vol = df_m.groupby('globaleventid')['sqldate','huf', 'fox', 'ap', 'reu', 'was'].max()
    df_vol = df_vol.groupby('sqldate')['huf', 'fox', 'ap', 'reu', 'was'].sum()
    ax = df_vol['2016-07':].plot(kind='area',alpha=.7, ax = ax,
                          title='Number of stories about '+new)
    ax.set_axis_bgcolor('w')
    ax.set_xlabel('')
    ax.set(yticklabels=[])
    ax.set_ylabel('# of stories')
    
    plt.subplot(2,1,2)
    df_m.set_index('sqldate',inplace=True)
    df_m.index = pd.to_datetime(df_m.index)
    targets = ['huf', 'fox', 'ap', 'reu', 'was']
    df_kde = df_m['2016-07':].reset_index()[targets+['tone']]
    df_kde = df_kde.apply(lambda x: x*df_kde['tone'])
    df_kde.replace('0',NaN,inplace=True)
    
    for t in targets:
        ax2 = df_kde[df_kde[t].notnull()][t].plot(kind='kde', alpha=.7, legend=True,
                                            label=t,xlim=(-10,10))
    ax2.set_axis_bgcolor('w')
    ax2.set_xlabel('Tone')
    ax2.set_xticklabels(['Negative','','Neutral','','Positive'])
    ax2.set_ylabel('# of stories')
    ax2.set_yticklabels('')
    
    return(plt.gcf())