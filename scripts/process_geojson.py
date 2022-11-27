# -*- coding: utf-8 -*-
"""
Created on Wed May 25 22:19:21 2022

@author: Usuario
"""
 

import json
import random

def add_residence(data, n_viviendas):
    
    n_features = len(data['features'])
    
    
    for i in range(n_viviendas):
        
        feature = {'type': 'Feature',
         'id': 2835,
         'properties': {'id': n_features + i + 1,
         'type': 'residence',
         'marker-color': "#ffffff",
         'marker-size': 'small',
         'marker-symbol': ''},
         'geometry': {'type': 'Point', 'coordinates': [random.uniform(-0.40546635605879244, -0.322382251354997), 
                                                       random.uniform(39.44867308677154, 39.49995332060239)]}}  ## -0.40546635605879244, -0.322382251354997
                                                                            ## 39.44867308677154, 39.49995332060239
        data['features'].append(feature)

def add_IO(data):
    n_features = len(data['features'])

    for i in range(n_features):
        
        if data['features'][i]['properties']['type'] == 'residence':
            data['features'][i]['properties']['IO'] = 0.6
        elif data['features'][i]['properties']['type'] == 'services':
            data['features'][i]['properties']['IO'] = 0.6
        elif data['features'][i]['properties']['type'] == 'running':
            data['features'][i]['properties']['IO'] = 1
        elif data['features'][i]['properties']['type'] == 'gym':
            data['features'][i]['properties']['IO'] = 0.6
        elif data['features'][i]['properties']['type'] == 'free time':
            data['features'][i]['properties']['IO'] = 0.9
        elif data['features'][i]['properties']['type'] == 'school':
            data['features'][i]['properties']['IO'] = 0.6
        elif data['features'][i]['properties']['type'] == 'running':
            data['features'][i]['properties']['IO'] = 0.6
        elif data['features'][i]['properties']['type'] == 'agriculture':
            data['features'][i]['properties']['IO'] = 1
        elif data['features'][i]['properties']['type'] == 'shopping':
            data['features'][i]['properties']['IO'] = 0.7
        elif data['features'][i]['properties']['type'] == 'industry':
            data['features'][i]['properties']['IO'] = 0.6
        elif data['features'][i]['properties']['type'] == 'bus':
            data['features'][i]['properties']['IO'] = 0.8
        elif data['features'][i]['properties']['type'] == 'metro':
            data['features'][i]['properties']['IO'] = 0.5
        elif data['features'][i]['properties']['type'] == 'university':
            data['features'][i]['properties']['IO'] = 0.6
        elif data['features'][i]['properties']['type'] == 'library':
            data['features'][i]['properties']['IO'] = 0.6
        elif data['features'][i]['properties']['type'] == 'aq':
            data['features'][i]['properties']['IO'] = 1
        else:
            raise Exception(f"type {data['features'][i]['properties']['type']} not found")
            
def add_cells():
    pass
    
with open('localizaciones_processed.json') as json_file:
    data = json.load(json_file)

add_IO(data)

with open('localizaciones_processed_IO.json', 'w') as outfile:
    json.dump(data, outfile)