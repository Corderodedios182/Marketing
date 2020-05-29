#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 15 11:51:29 2020

@author: carlos
"""
import requests
import json
import pandas as pd
import os

os.chdir('/home/carlos/Documentos/3_Adsocial/Marketing/Union_Campañas')
os.listdir()

from librerias import Escritura_Sheets

# --- Extracción ---

headers = { 'apikey': 'a9ea2c80-9618-11ea-afa7-add3af318161' }

#Catalogo

params = (
   ("q","Laptop Gamer Acer Predator Triton 500"),
   ("tbm","shop"),
   ("device","desktop"),
   ("gl","MX"),
   ("hl","es-419"),
   ("location","Coyoacan,Mexico City,Mexico"),
   ("num","10"),
)

response = requests.get('https://app.zenserp.com/api/v2/search', headers=headers, params=params);

# --- Transformación --- 

tmp = json.loads(response.text)['shopping_results']

tmp[0]['product_id']

data = pd.DataFrame(tmp).reset_index()


# --- Limpieza --- #

data.keys()

data['search'] = params[0][1]

data = data.loc[:,['search','title', 'source', 'price', 'price_parsed','stars', 'reviews', 'description', 'extensions', 'thumbnail','product_id', 'link']]

precio = []

for i in range(0, data.shape[0]):
    precio.append(data.loc[:,'price_parsed'][i]['value'])
    
data['price'] = precio

data = data.fillna(0)

data = data.sort_values(['price',
                         'stars',
                         'reviews',
                         'source'], ascending = False)


# --- Exportación --- #

Escritura_Sheets.Escritura(data , 1, Escribir = 'si', header = True, archivo_sheet = 'Dashboard Competencias')
