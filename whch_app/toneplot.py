
#Script for making tone plots

def toneplot(df_m,new):
    import pandas as pd
    import seaborn as sns
    #import matplotlib.pyplot as plt
    from numpy import NaN
    
    sns.set_style("white")
    
    df_m.reset_index(inplace=True)
    df_m.set_index('sqldate',inplace=True)
    df_m.index = pd.to_datetime(df_m.index)
    
    targets = ['huf', 'fox', 'ap', 'reu', 'was']
    df_kde = df_m['2016-07':].reset_index()[targets+['tone']]
    df_kde = df_kde.apply(lambda x: x*df_kde['tone'])
    df_kde.replace('0',NaN,inplace=True)
    
    #fig,ax = plt.subplots()
    for t in targets:
        ax2 = df_kde[df_kde[t].notnull()][t].plot(kind='kde', alpha=.7, legend=True,
                                            label=t,xlim=(-10,10))

    ax2.set_axis_bgcolor('w')
    ax2.set_xlabel('Tone')
    ax2.set_xticklabels(['Negative','','Neutral','','Positive'])
    ax2.set_ylabel('# of stories')
    ax2.set_yticklabels('')
    
    #sns.despine(left=True, bottom=True, right=True)
    #return(ax)