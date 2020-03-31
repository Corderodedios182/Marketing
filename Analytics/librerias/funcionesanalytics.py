#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 13:51:42 2020

@author: carlos
"""


#Paqueterías
import os 
import re 
import pandas as pd
import plotly.offline as pyo
import plotly.express as px
import plotly.graph_objects as go
import glob
import random

pd.set_option('display.float_format', lambda x: '%.f' % x)

#--          UNION DE LOS DIFERENTES ARCHIVOS DE GOOGLE ANALYTICS       --#

#Une todos los archivos de productos de las cuentas.
def Union_Archivos(Cuenta, analysis):
    
    analytics_union = []
    
    for i in range(len(Cuenta)):
        archivos = glob.glob("/home/carlos/Dropbox/Históricos GG/Históricos GG/" + Cuenta[i] + "/G Analytics/Productos/" + analysis + "/*.xlsx")
        
        # Productos por Campaña #
        for xls in archivos:
                tmp = pd.ExcelFile(xls)
                tmp = pd.read_excel(xls, 'Conjunto de datos1')
                tmp['archivo'] = xls
                tmp = tmp.iloc[:-1]
                tmp['cuenta'] = Cuenta[i]
                analytics_union.append(tmp)

    analytics_union = pd.concat(analytics_union)

    analytics_union['fechas'] = [ re.findall( r"\d{8}-\d{8}" ,i) for i in analytics_union.archivo ]
    
    return analytics_union