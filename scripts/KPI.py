# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 19:32:39 2022

@author: Usuario
"""

import pandas as pd
import numpy as np
from math import exp
import plotly.graph_objects as go

##### Daily Mean Population Exposure    
##### Daily Mean Relative Risk

data = pd.read_csv('./sintetic data/sintetic_data_v6_car.csv')

data.index = data.id
data = data[data.Duration > 10]

selection = []

for i in data.index:
    
    if data['exposure'][i].mean() > 400 or data['mortality relative risk'][i].mean() > 10:
        selection.append(1)
    else:
        selection.append(0)

data['selection'] = selection
data.index = pd.to_datetime(data.DateStart)

population_exposure = (data.resample('24H').mean()['exposure'])[0]
relative_risk = exp(5.91e-3*(population_exposure-10))

high_risk = round(len(data[data.level == 4].index)/len(data.index)*100)
time = data[data.level == 4].Duration.sum()/(len(data.index)*60)


  

