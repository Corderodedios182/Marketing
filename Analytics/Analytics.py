#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 11:30:53 2019

@author: carlos
"""
import pandas as pd
import glob
import re
import datetime

###########
#Analytics#
###########
#Aquí descargo el nuevo archivo de KPIS
def archivos_plataformas(mes = 'Enero', tipo_union = 'Semanal'):
    if tipo_union == 'Semanal':
        Archivos_csv = glob.glob('/home/carlos/Dropbox/ROAS 2020/' + mes + '/Semanal/**/*.csv')
        Archivos_xlsx = glob.glob('/home/carlos/Dropbox/ROAS 2020/' + mes + '/Semanal/**/*.xlsx')
    else:
        Archivos_csv = glob.glob('/home/carlos/Dropbox/ROAS 2020/' + mes + '/Mensual/*.csv')
        Archivos_xlsx = glob.glob('/home/carlos/Dropbox/ROAS 2020/' + mes + '/Mensual/*.xlsx')
    return Archivos_csv, Archivos_xlsx

#Funcion que arroja conversiones asistidas y trafico al sitio
def Analytics(mes = 'Enero'):
    
    csv, xlsx = archivos_plataformas(mes = mes)

    analytics_asistidas = [x for x in csv if "Analytics" in x]

    union_conversiones = []
    
    #Trabaja solo los archivos de conversiones
    for csv in analytics_asistidas:
        tmp = pd.read_csv(csv, skiprows = 6)
        tmp = tmp.iloc[:-3,:]
        tmp['archivo'] = csv
        tmp['fecha_reporte'] = [re.findall(r"\d{8}-\d{8}", i) for i in list(tmp.archivo)]
        
        fechas = [re.findall(r"\d{8}|d{8}", i) for i in list(tmp.archivo)]
        fechas = pd.DataFrame(fechas)
        fechas.columns = ['inicio_reporte','fin_reporte']
        
        
        
        pd.to_datetime(fechas.inicio_reporte, errors = 'coerce',format='yyyymmdd')
        
        tmp = pd.concat([tmp.reset_index(drop = True), pd.DataFrame(fechas)], axis = 1)
        union_conversiones.append(tmp)

    union_conversiones = pd.concat(union_conversiones)
    
    union_conversiones = union_conversiones.loc[:,('archivo','inicio_reporte','fin_reporte','Fuente/Medio','Campaña','Conversiones asistidas','Valor de las conversiones asistidas')]
    union_conversiones.columns = ['archivo','inicio_reporte','fin_reporte','Fuente_Medio','Nombre_Campaña','Conversiones','Revenue']
    
    union_conversiones['Tipo'] = 'Asistida'
    union_conversiones['mes'] = mes
    
    union_conversiones.Conversiones = union_conversiones.Conversiones.astype('int')
    
    union_conversiones.Revenue = union_conversiones.Revenue.apply(lambda x : str(x).replace('.',''))
    union_conversiones.Revenue = union_conversiones.Revenue.apply(lambda x : str(x).replace(',','.'))
    union_conversiones.Revenue = union_conversiones.Revenue.apply(lambda x : str(x).replace('MXN','')).astype('float')
    
    #Conversiones todo el trafico
    analytics_trafico = [x for x in xlsx if "Analytics" in x]
    
    union_trafico = []
    
    #Trabaja los archivos de trafico al sitio
    for xls in analytics_trafico:
        tmp = pd.ExcelFile(xls)
        tmp = pd.read_excel(tmp, 'Conjunto de datos1')
        tmp = tmp.iloc[:-1,:]
        tmp['archivo'] = xls
        tmp['fecha_reporte'] = [re.findall(r"\d{8}-\d{8}", i) for i in list(tmp.archivo)]
        
        fechas = [re.findall(r"\d{8}|d{8}", i) for i in list(tmp.archivo)]
        fechas = pd.DataFrame(fechas)
        fechas.columns = ['inicio_reporte','fin_reporte']
        
        tmp = pd.concat([tmp.reset_index(drop = True), pd.DataFrame(fechas)], axis = 1)

        union_trafico.append(tmp)
        
    union_trafico = pd.concat(union_trafico)
        
    union_trafico = union_trafico.loc[:,('archivo','inicio_reporte','fin_reporte','Fuente/Medio','Campaña','Transacciones','Ingresos')]
    union_trafico.columns = ['archivo','inicio_reporte','fin_reporte','Fuente_Medio','Nombre_Campaña','Conversiones','Revenue']
    union_trafico['Tipo'] = 'Directa'
    union_trafico['mes'] = mes
        
    union_trafico.Conversiones = union_trafico.Conversiones.astype('int')
        
        #Union de los 2 tmp
    union_analytics = pd.concat([union_conversiones,union_trafico])
    
    return union_analytics

analytics = pd.concat([Analytics(mes = 'Enero'), Analytics(mes = 'Febrero')])

#########################################
#Escritura de los datos en Google Sheets#
#########################################
import os
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

Escritura(analytics, 9,header = True , Escribir = 'no')



