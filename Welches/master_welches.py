# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 21:12:09 2021

Descripcion: El siguiente script tiene como objetvo centralizar la información de Facebook, Google Ads, Analytics

Jerarquía de ejecución:
    - Limpieza
    - Union reportes Plataformas

"""
#Paquetes 
import pandas as pd
import os

#Definimos la ruta para poder trabajar con los diferentes Scripts de apoyo
os.chdir('C:/Users/crf005r/Documents/3_GitHub/Marketing/Welches')
os.listdir()

from scrips_apoyo import facebook #importar y limpiar los datos de facebook
from scrips_apoyo import google_sheets #importa y exporta la informacion en google sheets

#Función para depositar la información en el google sheets
os.chdir('C:/Users/crf005r/Documents/3_GitHub/Marketing/Welches')
os.listdir()

#--Unir las bases de las plataformas

#facebook
df_facebook = facebook.datos_facebook()

base_master = pd.concat([df_facebook])

#--Exportar los datos a Google Sheets
google_sheets.exportar_sheets(base_master, hoja = 1)
