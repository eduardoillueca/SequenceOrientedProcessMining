# -*- coding: utf-8 -*-
"""
Created on Mon May 16 11:25:37 2022

@author: Usuario
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.stats.multicomp as mc
import scipy.stats as stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
import numpy as np

def read_csv(path):
    
    data_activity = pd.read_csv(path, sep = ",")
    return data_activity 

def plot_heatmap(post_hoc_res, groups):
    means = post_hoc_res._multicomp.groupstats.groupmean
    h  = np.random.rand(len(means), len(means))


    for i in range(len(means)):
        for j in range(len(means)):
            h[i,j] = abs(means[i] - means[j])

    h = pd.DataFrame(h)

    h.columns = groups
    h.index = groups

    f, ax = plt.subplots(figsize=(10, 10))
    ax = sns.heatmap(h, cmap="YlGnBu")
    
    return f

def anova_workflow(ecsv, target = 'EXPOSURE'):
    
    data = read_csv(ecsv)
    data['RR'] = data['mortality relative risk']
    print(data.columns)
    print('######### ANOVA RESULTS #########')
    model = ols(f'{target} ~ Activity', data=data).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)
    print(anova_table)
    
    print('######### TUKEY RESULTS #########')
    comp = mc.MultiComparison(data[f'{target}'],data['Activity'])
    post_hoc_res = comp.tukeyhsd()
    print(post_hoc_res.summary())
    

    plot_heatmap(post_hoc_res, groups = data['Activity'].unique())
    post_hoc_res.plot_simultaneous(ylabel= "Activity", xlabel= "Difference")
    
    return(post_hoc_res)

rest = anova_workflow('/home/hopu/Descargas/PaperKarolinska-main/data/sequence_data/sintetic_data_v6.csv', target = 'exposure')
