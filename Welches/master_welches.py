# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 21:12:09 2021

Descripcion: El siguiente script tiene como objetvo centralizar la información de Facebook, Google Ads, Analytics

Jerarquía de ejecución:
    - Limpieza
    - Union reportes Plataformas

"""

from datetime import datetime
startTime = datetime.now()

#Paquetes 

import pandas as pd
import os
import glob
import re
import datetime
from datetime import datetime, timedelta 
import seaborn as sns
import matplotlib.pyplot as plt 
pd.set_option('display.float_format', lambda x: '%.2f' % x)

#Definimos la ruta para poder trabajar con los diferentes Scripts de apoyo
os.chdir('C:/Users/crf005r/Documents/3_GitHub/Marketing/Welches')
os.listdir()

from scrips_apoyo import google_sheets #importa y exporta la informacion en google sheets

#Función para depositar la información en el google sheets
os.chdir('C:/Users/crf005r/Documents/3_GitHub/Marketing/Welches')
os.listdir()

Base = pd.read_csv('Facebook.csv')

#Exportar los datos a Google Sheets
google_sheets.exportar_sheets(Base)

#0. Git-push en github y setear nuestro entorno de desarrollo

#1. Importar los datos desde Sheets
    #Update - API's

#2. Unir y limpiar 

#3. Exportar datos al Sheets
    #Update - GCP
