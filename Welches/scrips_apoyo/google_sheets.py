# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 21:12:09 2021

Descripcion: Escribir los Archivos en google Sheets.

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

def exportar_sheets(Base, hoja = 'Master', header = False, Escribir = 'si', archivo_sheet = 'Master Welchs'):
    
    Escribir = Escribir

    if Escribir == 'si':
        os.chdir('C:/Users/crf005r/Documents/3_GitHub/Marketing/Welches/scrips_apoyo')
        os.listdir()
        #Autentificacion con google cloud platform correo analytics.adsocial@gmail.com
        scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("welches-5291fb1d6517.json", scope)
        client = gspread.authorize(creds)

        sh = client.open(archivo_sheet) #Recordar que el archivo que deseamos leer tiene que tener el correo de la api como persona compartida
                
        worksheet = sh.get_worksheet(3) #Base_master_python
        sh.worksheets()
        
        filas = len(worksheet.get_all_values()) + 1
        set_with_dataframe(worksheet, Base, row = filas)

    else: 
        print("Ok!, No escribimos nada")    

#Función para extraer los datos.

def importar_sheets(sheets = 'Base master Roas', hoja = 4, api_key_url = '/home/carlos/Documentos/3_Adsocial'):
    
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

#os.chdir('/home/carlos/Documentos/3_Adsocial')
#os.listdir()
#Autentificacion con google cloud platform correo analytics.adsocial@gmail.com
#scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
#creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
#client = gspread.authorize(creds)
    
#sh = client.open('test') #Recordar que el archivo que deseamos leer tiene que tener el correo de la api como persona compartida

#import re
#hojas = pd.Series(sh.worksheets())
#for hoja in hojas:
    #print(re.findall(r".*analy", hoja))

#r = re.compile(".*analy")
#list(filter(r.match, hojas))

#sh.del_worksheet(sh.worksheets()[2])
            
#worksheet = sh.add_worksheet(title= "analy", rows="100", cols="20")
