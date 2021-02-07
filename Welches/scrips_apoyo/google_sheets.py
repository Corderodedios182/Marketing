# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 21:12:09 2021

Descripcion: Se tienen 2 funciones para exportar e importar la infomacion

    1.- exportar_sheets()
    2.- importar_sheets()

"""

#######################################
#Trabajando con datos en Google Sheets#
#######################################

import pandas as pd
import os
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe #,get_as_dataframe

def exportar_sheets(base, hoja = 1, header = False, Escribir = 'si', archivo_sheet = 'Master Welchs', api_key_url = 'C:/Users/crf005r/Documents/3_GitHub/Marketing/Welches/scrips_apoyo'):
    
    """Exportamos datos a google sheets, es necesario tener las credenciales (creds.json) y que el correo se encuentre en el google sheets.
    
    :base: datos que queremos mandar al sheets
    :hoja: hoja del sheets al que mandaremos la informacion
    :header: incluye los encabezados
    :Escribir: se coloca si se quieren escribir los datos o no
    :archivos_sheets: nombre de la hoja del sheets
    
    :return: escribira los datos en google sheets
    
    >>> exportar_sheets(base_master, hoja = 'base_master', header = False, Escribir = 'si', archivo_sheet = 'Master Welchs')
        escribira la base_master en la hoja base master sin los encabezados en el sheets llamado Master Welchs

    """

    Escribir = Escribir

    if Escribir == 'si':
        os.chdir(api_key_url)
        os.listdir()
        #Autentificacion con google cloud platform correo analytics.adsocial@gmail.com
        scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("welches-5291fb1d6517.json", scope)
        client = gspread.authorize(creds)

        sh = client.open(archivo_sheet) #Recordar que el archivo que deseamos leer tiene que tener el correo de la api como persona compartida
                
        worksheet = sh.get_worksheet(hoja) #Base_master_python
        sh.worksheets()
        
        filas = len(worksheet.get_all_values()) + 1
        set_with_dataframe(worksheet, base, row = filas)

    else: 
        print("Ok!, No escribimos nada")    

#Función para extraer los datos.

def importar_sheets(sheets = 'Master Welchs', hoja = 1, api_key_url = 'C:/Users/crf005r/Documents/3_GitHub/Marketing/Welches/scrips_apoyo'):
    
    """ Recuperamos datos finales del google sheets, es necesario tener las credenciales (creds.json) y que el correo se encuentre en el google sheets.
    
    :sheets: archivo al que queremos exportar
    :hoja: donde queremos depositar la información
    :api_key_url: carpeta de credenciales .json para la API de Sheets
    
    :return: regresa los datos de una hoja de google sheets
    
    >>> archivos_finales(sheets = 'Master Welchs', hoja = 1, api_key_url = 'C:/Users/crf005r/Documents/3_GitHub/Marketing/Welches/scrips_apoyo')
        importaría los datos en el Sheets Master Welchs
    """
    
    os.chdir(api_key_url)
    os.listdir()
    #Autentificacion con google cloud platform correo analytics.adsocial@gmail.com
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("welches-5291fb1d6517.json", scope)
    client = gspread.authorize(creds)
    
    sh = client.open(sheets) #Recordar que el archivo que deseamos leer tiene que tener el correo de la api como persona compartida
    worksheet = sh.get_worksheet(hoja) #Base_master_python

    datos = pd.DataFrame(worksheet.get_all_values())
    col = list(datos.iloc[0,])
    datos = datos.iloc[1:,:]
    datos.columns = col
    
    return datos
