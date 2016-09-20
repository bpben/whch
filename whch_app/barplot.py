
#Script for making prediction plots
#Reads in list of prediction, creates dataframes, plots

def barplot(targs,preds):
    import seaborn as sns
    
    sns.set_style("white")
    
    return(sns.barplot(y=targs,x=preds))

