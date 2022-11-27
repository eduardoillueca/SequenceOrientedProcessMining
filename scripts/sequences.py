# -*- coding: utf-8 -*-
"""
Created on Tue May 24 11:09:53 2022

@author: Usuario
"""

import pandas as pd
import numpy as np
from scipy.stats import norm
import random
import json
from datetime import timedelta
from math import radians, sin, asin, sqrt, atan2
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from math import exp


def get_manhattan_distance(p,q):
    
    lat1, lon1, lat2, lon2 = map(radians, [p[0], p[1], q[0], q[1]])
    
    #haversine formula for delta_lat
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    r = 6371
    lat_d = c * r
    
    # haversine formula for delta_lon
    dlon = lon2 - lon1
    a = sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    r = 6371
    lon_d = c * r
    
    
    return lat_d + lon_d

def categorical(x):
    return np.random.multinomial(1, pvals=x)

def get_IO(activity, locations):
         
    if activity in ['stay at home', 'services', 'free time', 'university', 'library', 'residence', 'gym', 'school', 'industry', 'shopping', 'running', 'agriculture', 'metro']:
        
        if activity == 'stay at home':
            activity = 'residence'
        else:
            pass
        
        stop = False
        i = 0
        IO = 1
        
        while not(stop) and i < len(locations['features']):
            
            if locations['features'][i]['properties']['type'] == activity:
                IO = locations['features'][i]['properties']['IO']
                stop = True
            else:
                pass
            
            i = i + 1
            
    elif activity == 'by foot':
        IO = 1.75
    elif activity == 'private car':
        IO = 0.6
    else:
        IO = 1
    
    return IO
            
    
    
def find_cell(domain, coordinates):
    
    
    point = Point(coordinates)
    
    i = 0
    cell_id = -1
    flag = True
    
    while i < len(domain['features']) and flag:
        
        polygon = Polygon(domain['features'][i]['geometry']['coordinates'][0])
                
        if polygon.contains(point):
            cell_id = i
            flag = False
        
        i = i + 1
    
    return cell_id

    
def process_sequence(s, citizen, locations, domain):
    
    result = pd.DataFrame()
       
    full = s.split('-')
    activities = full[0:len(full):2]
    movements = full[1:len(full):2]
    
    
    
    residence_location = locations['features'][citizen.residence]['geometry']['coordinates']
    work_location = locations['features'][citizen.employ]['geometry']['coordinates']
    free_location = locations['features'][citizen.freeTime]['geometry']['coordinates']
    
    if residence_location == work_location:
        print('OJO')
        
    residence_cell = find_cell(domain,residence_location)
    work_cell = find_cell(domain,work_location)
    free_cell = find_cell(domain,free_location)
    
    l = []
    c = []
    
    o = 0
    
    for a in range(len(activities)):
        
        if activities[a] in ['school', 'university']:
            mu = norm.rvs(size=1, loc = 360, scale = 10)
            l.append(work_location)
            c.append(work_cell)
        elif activities[a] in ['services', 'industry', 'agriculture', 'residence']:
            mu = norm.rvs(size=1, loc = 480, scale = 10)
            l.append(work_location)
            c.append(work_cell)
        elif activities[a] in ['running', 'gym', 'free time', 'shopping', 'library']:
            mu = norm.rvs(size=1, loc = 240, scale = 10)
            l.append(free_location)
            c.append(free_cell)
        else:
            mu = norm.rvs(size=1, loc = 120, scale = 10)
            l.append(residence_location)
            c.append(residence_cell)
                
        r = {'id': citizen.id,
             'cell_id': c[a],
             'order': o,
             'Activity': activities[a],
             'Duration': mu,
             'DateStart': 0,
             'DateEnd': 0,
             'Sex': citizen.sex,
             'Age': citizen.age,
             'Asthma': citizen.asthma,
             'Diabetes': citizen.diabetes,
             'High Blood Pressure': citizen[7],
             'Pulmonar Disease': citizen[8],
             'Heart Disease': citizen[9],
             'Anxiety': citizen.anxiety,
             'Smoke': citizen.smoke,
             'Alcohol': citizen.alcohol}
        
        o = o + 2
        result = pd.concat([result,pd.DataFrame(r, index = [citizen.id])], axis = 0)
        
    o = 1
    
    for m in range(0,len(movements)):
        
        if movements == 'by foot':
            mu = (get_manhattan_distance(l[m],l[m+1])/5.7)*60 + random.randint(10,20)
        else:
            mu = (get_manhattan_distance(l[m],l[m+1])/40)*60 + random.randint(10,20)
        
        r = {'id': citizen.id,
             'cell_id': c[m]*100 + c[m+1],
             'order': o,
             'Activity': movements[m],
             'Duration': mu,
             'DateStart': 0,
             'DateEnd': 0,
             'Sex': citizen.sex,
             'Age': citizen.age,
             'Asthma': citizen.asthma,
             'Diabetes': citizen.diabetes,
             'High Blood Pressure': citizen[7],
             'Pulmonar Disease': citizen[8],
             'Heart Disease': citizen[9],
             'Anxiety': citizen.anxiety,
             'Smoke': citizen.smoke,
             'Alcohol': citizen.alcohol}
        
        o = o + 2
        result = pd.concat([result,pd.DataFrame(r, index = [citizen.id])], axis = 0) 
    
    result = result.sort_values(by = 'order')
    result.index = range(len(result.index))
    result = result.dropna()
    
    
    result.loc[0,'Duration'] = 8*60 + random.randint(-10, 10)
    result.loc[len(result.index)-1,'Duration'] = 24*60 - result.Duration[0:(len(result.index) -1)].sum()
    
    return result

def assign_timestamp(r):
    
    start = [pd.to_datetime('2018-01-01 00:00:00')]
    end = [start[0] + timedelta(minutes = r.Duration[0])]
    
    for i in range(len(r.index)-1):
        
        start.append(end[i])
        end.append(end[i] + timedelta(minutes = r.Duration[i+1]))
    
    r.DateStart = start
    r.DateEnd = end
    
    return r
        
        
        
def generate_sequences(data, locations,domain):
    
    final_data = pd.DataFrame()
    
    end = norm.rvs(size=len(data['id']), loc = 1140, scale = 240)
    
    for i in range(len(data['id'])):
        
        if data.age[i] < 18:
            sequence = 1
        else:
            sequence = random.choice([1,2,3])
        
        if data.transport[i] == -1:
            
            if sequence == 1:
                s = f"stay at home-by foot-{locations['features'][data.employ[i]]['properties']['type']}-by foot-stay at home"
            elif sequence == 2:
                s = f"stay at home-by foot-{locations['features'][data.employ[i]]['properties']['type']}-by foot-{locations['features'][data.freeTime[i]]['properties']['type']}-by foot-stay at home"
            else:
                s = f"stay at home-by foot-{locations['features'][data.employ[i]]['properties']['type']}-by foot-stay at home-by foot-{locations['features'][data.freeTime[i]]['properties']['type']}-by foot-stay at home"
        
        elif data.transport[i] == -2:
            
            if sequence == 1:
                s = f"stay at home-private car-{locations['features'][data.employ[i]]['properties']['type']}-private car-stay at home"
            elif sequence == 2:
                s = f"stay at home-private car-{locations['features'][data.employ[i]]['properties']['type']}-private car-{locations['features'][data.freeTime[i]]['properties']['type']}-private car-stay at home"
            else:
                s = f"stay at home-private car-{locations['features'][data.employ[i]]['properties']['type']}-private car-stay at home-private car-{locations['features'][data.freeTime[i]]['properties']['type']}-private car-stay at home"
        
        else:
            
            if sequence == 1:
                s = f"stay at home-metro-{locations['features'][data.employ[i]]['properties']['type']}-metro-stay at home"
            elif sequence == 2:
                s = f"stay at home-metro-{locations['features'][data.employ[i]]['properties']['type']}-metro-{locations['features'][data.freeTime[i]]['properties']['type']}-metro-stay at home"
            else:
                s = f"stay at home-metro-{locations['features'][data.employ[i]]['properties']['type']}-metro-stay at home-metro-{locations['features'][data.freeTime[i]]['properties']['type']}-metro-stay at home"
                
        
        r = process_sequence(s, data.iloc[i,:], locations, domain)
        r = r.dropna()

        r = assign_timestamp(r)
        final_data = pd.concat([final_data,r])
    
    final_data.index = range(len(final_data.index))
    
    return final_data
        
        

def assign_exposure(final_data, aq, RR, locations):
        
    concentration = []
    exposure = []
    level = []
    rr = []
    
    aq.index = aq.hourId
    
    for i in final_data.index:
                
        a = aq.loc[final_data.DateStart[i].hour:final_data.DateEnd[i].hour,:]
        
        IO = get_IO(final_data.Activity[i], locations)
        
        if len(a.index) == 0:
            a = aq.loc[final_data.DateStart[i].hour:,:]
        
        if final_data.cell_id[i]<1000:
            concentration.append((a[a.cell_id == final_data.cell_id[i]]['PM2.5'].iloc[0])*IO)
        else:
            concentration.append((a[a.cell_id.isin([final_data.cell_id[i]//100,final_data.cell_id[i]%100])]['PM2.5'].mean())*IO)
        
        exposure.append(concentration[i]*(final_data.Duration[i]/60))
        
        if exposure[i] < 5:
            level.append(0)
            rr.append(exp(5.91e-3*(exposure[i] - 10)) + RR['Diabetes']*final_data['Diabetes'][i] + RR['Asthma']*final_data['Asthma'][i] + RR['High Blood Pressure']*final_data['High Blood Pressure'][i] + RR['Pulmonar Disease']*final_data['Pulmonar Disease'][i] + RR['Heart Disease']*final_data['Heart Disease'][i] + RR['Anxiety']*final_data['Anxiety'][i] + RR['Smoke']*final_data['Smoke'][i] + RR['Alcohol']*final_data['Alcohol'][i])
        elif exposure[i] < 10 and exposure[i] >= 5:
            level.append(1)
            rr.append(exp(5.91e-3*(exposure[i] - 10)) + RR['Diabetes']*final_data['Diabetes'][i] + RR['Asthma']*final_data['Asthma'][i] + RR['High Blood Pressure']*final_data['High Blood Pressure'][i] + RR['Pulmonar Disease']*final_data['Pulmonar Disease'][i] + RR['Heart Disease']*final_data['Heart Disease'][i] + RR['Anxiety']*final_data['Anxiety'][i] + RR['Smoke']*final_data['Smoke'][i] + RR['Alcohol']*final_data['Alcohol'][i])
        elif exposure[i] < 15 and exposure[i] >= 10:
            level.append(2)
            rr.append(exp(5.91e-3*(exposure[i] - 10)) + RR['Diabetes']*final_data['Diabetes'][i] + RR['Asthma']*final_data['Asthma'][i] + RR['High Blood Pressure']*final_data['High Blood Pressure'][i] + RR['Pulmonar Disease']*final_data['Pulmonar Disease'][i] + RR['Heart Disease']*final_data['Heart Disease'][i] + RR['Anxiety']*final_data['Anxiety'][i] + RR['Smoke']*final_data['Smoke'][i] + RR['Alcohol']*final_data['Alcohol'][i])
        elif exposure[i] < 25 and exposure[i] >= 15:
            level.append(3)
            rr.append(exp(5.91e-3*(exposure[i] - 10)) + RR['Diabetes']*final_data['Diabetes'][i] + RR['Asthma']*final_data['Asthma'][i] + RR['High Blood Pressure']*final_data['High Blood Pressure'][i] + RR['Pulmonar Disease']*final_data['Pulmonar Disease'][i] + RR['Heart Disease']*final_data['Heart Disease'][i] + RR['Anxiety']*final_data['Anxiety'][i] + RR['Smoke']*final_data['Smoke'][i] + RR['Alcohol']*final_data['Alcohol'][i])
        elif exposure[i] < 1000 and exposure[i] >= 25:
            level.append(4)
            rr.append(exp(5.91e-3*(exposure[i] - 10)) + RR['Diabetes']*final_data['Diabetes'][i] + RR['Asthma']*final_data['Asthma'][i] + RR['High Blood Pressure']*final_data['High Blood Pressure'][i] + RR['Pulmonar Disease']*final_data['Pulmonar Disease'][i] + RR['Heart Disease']*final_data['Heart Disease'][i] + RR['Anxiety']*final_data['Anxiety'][i] + RR['Smoke']*final_data['Smoke'][i] + RR['Alcohol']*final_data['Alcohol'][i])
        else:
            level.append(-1)
            rr.append(-1)
        
    final_data['concentration'] = concentration
    final_data['exposure'] = exposure
    final_data['level'] = level
    final_data['mortality relative risk'] = rr
    
    return final_data

#### READ DATA ####
    
aq = pd.read_csv('/home/hopu/Descargas/PaperKarolinska/data/aq_data/valencia_aq_gridded_v2.csv')
aq = aq[aq['dayId'] == '2018-03-01']

data = pd.read_csv('/home/hopu/Descargas/PaperKarolinska/data/population_data/sample_population_v3.csv')

l = len(data['id'])

with open('/home/hopu/Descargas/PaperKarolinska/config/valencia.json') as file:
    domain = json.load(file)

with open('/home/hopu/Descargas/PaperKarolinska/config/localizaciones_processed_IO.json') as file:
    locations = json.load(file)
  
with open('/home/hopu/Descargas/PaperKarolinska/config/RR.json') as file:
    RR = json.load(file)

final_data = generate_sequences(data, locations, domain)
final_data = assign_exposure(final_data, aq, RR, locations)

final_data.to_csv('/home/hopu/Descargas/PaperKarolinska/data/sequence_data/sintetic_data_v6.csv')


