# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 15:53:41 2022

@author: Usuario
"""

from scipy.stats import bernoulli
import matplotlib as plt
import random
from scipy.stats import multinomial
import numpy as np
import json
import pandas as pd

def categorical(x):
    return np.random.multinomial(1, pvals=x)

def extract(locations, t):
    result = []
    
    for f in range(len(locations['features'])):
        
        if locations['features'][f]['properties']['type'] == t:
            result.append(locations['features'][f]['properties']['id'])
    
    return result

def assign_employ(employ, age):
    
    industry = extract(locations, t = 'industry')
    services = extract(locations, t = 'services')
    agriculture = extract(locations, t = 'agriculture')
    residences = extract(locations, t = 'residence')
    school = extract(locations, t = 'school')
    university = extract(locations, t = 'university')

    if age < 18:
        result = random.choice(school)
    elif age < 22:
        result = random.choice(university)
    else:
        e = list(np.apply_along_axis(categorical, axis=0, arr=list(employ.values()))).index(1)
        e = list(employ.keys())[e]
        
        if e == 'services':
            result = random.choice(services)
        elif e == 'industry':
            result = random.choice(industry)
        elif e == 'agriculture':
            result = random.choice(agriculture)
        elif e == 'construction':
            result = random.choice(residences)
        elif e == 'unemployed':
            result = -1
        else:
            print(e)
    
    return result

def assign_mobility(transport):
    metro = extract(locations, t = 'metro')

    m = list(np.apply_along_axis(categorical, axis=0, arr=list(transport.values()))).index(1)
    m = list(transport.keys())[m]
    
    if m == 'by foot':
        result = -1
    elif m == 'private car':
        result = -2
    elif m == 'metro':
        result = random.choice(metro)*100 + random.choice(metro)
    else:
        result = -3
    
    return result 

def assign_leissure(freeTime, employ):
    
    gym = extract(locations, t = 'gym')
    running = extract(locations, t = 'running')
    shopping = extract(locations, t = 'shopping')
    free = extract(locations, t = 'free time')
    library = extract(locations, t = 'library')

    if employ in [46,47]:
        result = random.choice(library)
    else:
        f = list(np.apply_along_axis(categorical, axis=0, arr=list(freeTime.values()))).index(1)
        f = list(freeTime.keys())[f]
        
        if f == 'gym':
            result = random.choice(gym)
        elif f == 'running':
            result = random.choice(running)
        elif f == 'shopping':
            result = random.choice(shopping)
        else:
            result = random.choice(free)
    
    return result 
    

def create_popultaion(poblacion, indice_masa_corporal, incidencia_enfermagees_cronicas, employ, transport, freeTine, locations):
    
    residences = extract(locations, t = 'residence')
    gym = extract(locations, t = 'gym')
    running = extract(locations, t = 'running')
    free = extract(locations, t = 'free time')
    library = extract(locations, t = 'library')
    university = extract(locations, t = 'university')       

    data = pd.DataFrame()

    for i in range(15795):
        result = {
                  'id': hex(random.randint(0, 10000000000000000000000000000000000)),
                  'sex': 0,
                  'age': 0,
                  'obesity': 0,
                  'diabetes': 0,
                  'asthma': 0,
                  'high blood pressure': 0,
                  'pulmonar disease': 0,
                  'heart disease': 0,
                  'anxiety': 0,
                  'smoke': 0,
                  'alcohol': 0,
                  'employ': 0,
                  'transport': 0,
                  'freeTime': 0,
                  'residence': 0
                  }
        
        result['sex'] = bernoulli.rvs(0.5, size=1)[0]
        result['age'] = list(np.apply_along_axis(categorical, axis=0, arr=poblacion['data'])).index(1)
        result['obesity'] = bernoulli.rvs(indice_masa_corporal[str(result['sex'])][str(result['age'])], size=1)[0]
        
        result['diabetes'] = bernoulli.rvs(incidencia_enfermagees_cronicas[str(result['sex'])]['diabetes'][str(result['age'])], size=1)[0]
        result['asthma'] = bernoulli.rvs(incidencia_enfermagees_cronicas[str(result['sex'])]['asthma'][str(result['age'])], size=1)[0]
        result['high blood pressure'] = bernoulli.rvs(incidencia_enfermagees_cronicas[str(result['sex'])]['high blood pressure'][str(result['age'])], size=1)[0]
        result['pulmonar disease'] = bernoulli.rvs(incidencia_enfermagees_cronicas[str(result['sex'])]['pulmonar disease'][str(result['age'])], size=1)[0]
        result['heart disease'] = bernoulli.rvs(incidencia_enfermagees_cronicas[str(result['sex'])]['heart disease'][str(result['age'])], size=1)[0]
        result['anxiety'] = bernoulli.rvs(incidencia_enfermagees_cronicas[str(result['sex'])]['anxiety'][str(result['age'])], size=1)[0]
        
        result['smoke'] = bernoulli.rvs(0.221, size=1)[0]
        result['alcohol'] = bernoulli.rvs(0.147, size=1)[0]
        
        result['age'] = result['age'] + 1 + result['age']*(random.randint(1,4))
        
        result['employ'] = assign_employ(employ, result['age'])
        result['transport'] = assign_mobility(transport)
        result['freeTime'] = assign_leissure(freeTime, result['employ'])
        
        
        
        result['residence'] = random.choice(residences)
        
        result = pd.DataFrame(result, index=[i])
        
        data = pd.concat([data,result])
    
    return data

with open('../config/population.json') as file:
    poblacion = json.load(file)

with open('../config/icm.json') as file:
    indice_masa_corporal = json.load(file)

with open('../config/incidencia.json') as file:
    incidencia_enfermagees_cronicas = json.load(file)

with open('../config/empleo.json') as file:
    employ = json.load(file)

with open('../config/transporte.json') as file:
    transport = json.load(file)

with open('../config/tiempoLibre.json') as file:
    freeTime = json.load(file)
    
with open('../config/localizaciones_processed_IO.json') as file:
    locations = json.load(file)

data = create_popultaion(poblacion, indice_masa_corporal, incidencia_enfermagees_cronicas, employ, transport, freeTime, locations)

data.to_csv('../data/population_data/sample_population_v8.csv')