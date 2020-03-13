#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 11:00:06 2020

@author: carlos
"""

#########################################
#Escritura de los datos en Google Sheets#
#########################################
import os
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe #,get_as_dataframe

def Escritura(Base, hoja, header = False, Escribir = 'no'):
    
    Escribir = Escribir

    if Escribir == 'si':
        os.chdir('/home/carlos/Documentos/3_Adsocial')
        os.listdir()
        #Autentificacion con google cloud platform correo analytics.adsocial@gmail.com
        scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
        client = gspread.authorize(creds)

        Base['ultima_actualizacion'] = datetime.now()
    
        sh = client.open('Validación Nomeclatura Adsocial') #Recordar que el archivo que deseamos leer tiene que tener el correo de la api como persona compartida
        worksheet = sh.get_worksheet(hoja) #Base_master_python
        #sh.worksheets()
        
        filas = len(worksheet.get_all_values()) + 1
        set_with_dataframe(worksheet, Base, row = filas, include_column_header = header)

    else: 
        print("Ok!, No escribimos nada")    

#Validar lo que tenemos arriba de forma semanal
#import pandas as pd

#os.chdir('/home/carlos/Documentos/3_Adsocial')
#os.listdir()
#Autentificacion con google cloud platform correo analytics.adsocial@gmail.com
#scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
#creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
#client = gspread.authorize(creds)
    
#sh = client.open('Validación Nomeclatura Adsocial') #Recordar que el archivo que deseamos leer tiene que tener el correo de la api como persona compartida
#worksheet = sh.get_worksheet(8) #Base_master_python
    
#tmp = pd.DataFrame(worksheet.get_all_values())
#tmp_0 = tmp.iloc[2:,:]
#tmp_0.columns = tmp.iloc[1,:]

#Llave unica
#a = (tmp_0.llave_ventas + "-" + tmp_0.versión + "-" +  tmp_0.mes_plan + "_" + tmp_0.inicio_reporte + "_" + tmp_0.fin_reporte).value_counts()
#tmp_0['llave_unica'] = tmp_0.llave_ventas + "-" + tmp_0.versión + "-" +  tmp_0.mes_plan + "_" + tmp_0.inicio_reporte + "_" + tmp_0.fin_reporte




    


    
    
    
        