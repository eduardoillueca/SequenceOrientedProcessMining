# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 19:32:39 2022

@author: Usuario
"""

import pandas as pd
import numpy as np
from math import exp
import plotly.graph_objects as go
import sys

##### Daily Mean Population Exposure    
##### Daily Mean Relative Risk

data = pd.read_csv(sys.argv[1])

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

population_exposure = round((data.resample('24H').mean()['exposure'])[0])
relative_risk = round(exp(5.91e-3*(population_exposure-10)),1)

high_risk = round(len(data[data.level == 4].index)/len(data.index)*100)
time = round(data[data.level == 4].Duration.sum()/(len(data.index)*60),1)

fig = go.Figure([go.Indicator(
    mode = "gauge+number+delta",
    value = high_risk,
    domain = {'x': [0, 0.4], 'y': [0, 0.4]},
    title = {'text': "Percentage of Risky Activities", 'font': {'size': 24}},
    delta = {'reference': 56, 'increasing': {'color': "RebeccaPurple"}},
    gauge = {
        'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
        'bar': {'color': "darkblue"},
        'bgcolor': "white",
        'borderwidth': 2,
        'bordercolor': "gray",
        'steps': [
            {'range': [0, 50], 'color': 'cyan'},
            {'range': [50, 100], 'color': 'royalblue'}]}),
    go.Indicator(
    mode = "gauge+number+delta",
    value = time,
    domain = {'x': [0.5, 0.9], 'y': [0, 0.4]},
    title = {'text': "Time Spent in Risky Activities (h)", 'font': {'size': 24}},
    delta = {'reference': 3.5, 'increasing': {'color': "RebeccaPurple"}},
    gauge = {
        'axis': {'range': [0, 4], 'tickwidth': 1, 'tickcolor': "darkblue"},
        'bar': {'color': "darkblue"},
        'bgcolor': "white",
        'borderwidth': 2,
        'bordercolor': "gray",
        'steps': [
            {'range': [0, 1], 'color': 'cyan'},
            {'range': [1, 4], 'color': 'royalblue'}]}),
    go.Indicator(
    mode = "gauge+number+delta",
    value = population_exposure,
    domain = {'x': [0, 0.4], 'y': [0.5, 0.9]},
    title = {'text': "24 h Popultaiotn Exposure", 'font': {'size': 24}},
    delta = {'reference': 119, 'increasing': {'color': "RebeccaPurple"}},
    gauge = {
        'axis': {'range': [0, 300], 'tickwidth': 1, 'tickcolor': "darkblue"},
        'bar': {'color': "darkblue"},
        'bgcolor': "white",
        'borderwidth': 2,
        'bordercolor': "gray",
        'steps': [
            {'range': [0, 100], 'color': 'cyan'},
            {'range': [100, 300], 'color': 'royalblue'}]}),
    go.Indicator(
    mode = "gauge+number+delta",
    value = relative_risk,
    domain = {'x': [0.5, 0.9], 'y': [0.5, 0.9]},
    title = {'text': "Mortality Relative Risk", 'font': {'size': 24}},
    delta = {'reference': 1.9, 'increasing': {'color': "RebeccaPurple"}},
    gauge = {
        'axis': {'range': [0, 5], 'tickwidth': 1, 'tickcolor': "darkblue"},
        'bar': {'color': "darkblue"},
        'bgcolor': "white",
        'borderwidth': 2,
        'bordercolor': "gray",
        'steps': [
            {'range': [0, 1], 'color': 'cyan'},
            {'range': [1, 5], 'color': 'royalblue'}]})])

fig.update_layout(paper_bgcolor = "lavender", font = {'color': "darkblue", 'family': "Arial"})
    
fig.show()


  

