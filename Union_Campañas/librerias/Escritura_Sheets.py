#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 11:00:06 2020

@author: carlos
"""

#########################################
#Escritura de los datos en Google Sheets#
#########################################
import pandas as pd
import os
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe #,get_as_dataframe

#Función para depositar la información en el google sheets

def Escritura(Base, hoja, header = False, Escribir = 'no', archivo_sheet = 'Validación Nomeclatura Adsocial'):
    
    """Escribe en google sheets los resultados finales, necesitamos tener las credenciales y el sheets debe tener el correo que vienen en las credenciales para tener acceso al sheets
    
    :Base: archivo que queremos exportar
    :hoja: donde queremos depositar la información
    :header: incluier los encabezados de los datos
    :Escribir:deseamos escribir los datos
    :return: no regresa nada, solo escribe los datos en google sheets
    
    >>> Escritura(Base_roas, hoja = 2, header = True, Escribir = 'si')
        
    """
    
    Escribir = Escribir

    if Escribir == 'si':
        os.chdir('/home/carlos/Documentos/3_Adsocial')
        os.listdir()
        #Autentificacion con google cloud platform correo analytics.adsocial@gmail.com
        scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
        client = gspread.authorize(creds)

        Base['ultima_actualizacion'] = datetime.now()
    
        sh = client.open(archivo_sheet) #Recordar que el archivo que deseamos leer tiene que tener el correo de la api como persona compartida
        worksheet = sh.get_worksheet(hoja) #Base_master_python
        #sh.worksheets()
        
        filas = len(worksheet.get_all_values()) + 1
        set_with_dataframe(worksheet, Base, row = filas, include_column_header = header)

    else: 
        print("Ok!, No escribimos nada")    

#Función para extraer los datos finales.

def archivos_finales(sheets = 'Base master Roas', hoja = 4, api_key_url = '/home/carlos/Documentos/3_Adsocial'):
    
    """ Recuperamos datos finales del google sheets, es necesario tener las credenciales (creds.json) y que el correo se encuentre en el google sheets.
    
    :sheets: archivo que queremos exportar
    :hoja: donde queremos depositar la información
    :api_key_url: incluier los encabezados de los datos
    
    :return: regresa los datos de una hoja de google sheets
    
    >>> archivos_finales(sheets = 'Validación Nomeclatura Adsocial', hoja = 2, api_key_url = '/home/carlos/Documentos/3_Adsocial')
        regresaría los datos del sheets validación nomenclatura adsocial hoja 2
    """
    
    os.chdir(api_key_url)
    os.listdir()
    #Autentificacion con google cloud platform correo analytics.adsocial@gmail.com
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)
    
    sh = client.open(sheets) #Recordar que el archivo que deseamos leer tiene que tener el correo de la api como persona compartida
    worksheet = sh.get_worksheet(hoja) #Base_master_python

    datos = pd.DataFrame(worksheet.get_all_values())

    col = list(datos.iloc[0,])

    datos = datos.iloc[1:,:]

    datos.columns = col
    
    return datos

############################################################
#Crear la función para remplazar la información
#

os.chdir('/home/carlos/Documentos/3_Adsocial')
os.listdir()
#Autentificacion con google cloud platform correo analytics.adsocial@gmail.com
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
    
sh = client.open('test') #Recordar que el archivo que deseamos leer tiene que tener el correo de la api como persona compartida

import re
hojas = pd.Series(sh.worksheets())
for hoja in hojas:
    print(re.findall(r".*analy", hoja))

r = re.compile(".*analy")
list(filter(r.match, hojas))

sh.del_worksheet(sh.worksheets()[2])
            
worksheet = sh.add_worksheet(title= "analy", rows="100", cols="20")













