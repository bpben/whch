
#Script for making prediction plots
#Reads in list of prediction, creates dataframes, plots

def barplot(targs,preds):
    import seaborn as sns
    
    sns.set_style("white")
    p = sns.barplot(y=targs,x=preds)
    sns.despine(left=True, bottom=True, right=True)
    p.set(xticklabels=[])
    return(p)