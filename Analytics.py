#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 11:30:53 2019

@author: carlos
"""
import os 
import re 
#import datetime
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe #,get_as_dataframe

###########
#Analytics#
###########

Todo_Analytics = []

#Este for va entrando en cada carpeta para solo trabajar con los arhivos de cada Marca
for Analytics in os.listdir('/home/carlos/Documentos/Adsocial/Sheets/Analytics/'):

    os.chdir('/home/carlos/Documentos/Adsocial/Sheets/Analytics/' + str(Analytics))
    Archivos = pd.Series(os.listdir())
    
    #Conversiones Asistidas
    tmp_conversiones = list(Archivos[Archivos.str.contains('Conver')])

    Union_conversiones = []
    
    #Trabaja solo los archivos de conversiones
    for csv in tmp_conversiones:
        tmp = pd.read_csv(csv, skiprows = 6)
        tmp = tmp.iloc[:-3,:]
        tmp['archivo'] = csv
        Union_conversiones.append(tmp)

    Union_conversiones = pd.concat(Union_conversiones)

    Union_conversiones = Union_conversiones.loc[:,('archivo','Fuente/Medio','Campaña','Conversiones asistidas','Valor de las conversiones asistidas')]
    Union_conversiones.columns = ['archivo','Fuente_Medio','Nombre_Campaña','Conversiones','Revenue']

    Union_conversiones['Tipo'] = 'Asistida'

    Union_conversiones.Conversiones = Union_conversiones.Conversiones.astype('int')

    Union_conversiones.Revenue = Union_conversiones.Revenue.apply(lambda x : str(x).replace('.',''))
    Union_conversiones.Revenue = Union_conversiones.Revenue.apply(lambda x : str(x).replace(',','.'))
    Union_conversiones.Revenue = Union_conversiones.Revenue.apply(lambda x : str(x).replace('MXN','')).astype('float')

    #Conversiones todo el trafico
    tmp_trafico = list(Archivos[Archivos.str.contains('Todo el ')])

    Union_trafico = []

    #Trabaja los archivos de trafico al sitio
    for xls in tmp_trafico:
        tmp = pd.ExcelFile(xls)
        tmp = pd.read_excel(tmp, 'Conjunto de datos1')
        tmp = tmp.iloc[:-1,:]
        tmp['archivo'] = xls
        Union_trafico.append(tmp)

    Union_trafico = pd.concat(Union_trafico)

    Union_trafico = Union_trafico.loc[:,('archivo','Fuente/Medio','Campaña','Transacciones','Ingresos')]
    Union_trafico.columns = ['archivo','Fuente_Medio','Nombre_Campaña','Conversiones','Revenue']
    Union_trafico['Tipo'] = 'Directa'

    Union_trafico.Conversiones = Union_trafico.Conversiones.astype('int')
    
    #Union de los 2 tmp
    Union_Analytics = pd.concat([Union_conversiones,Union_trafico])
    Union_Analytics['Marca'] = Analytics
    
    #Una vez que tenemos todos los archivos de cada Marca los almacenamos en un archivo final
    Todo_Analytics.append(Union_Analytics)
    del tmp_conversiones, tmp_trafico, csv, xls, tmp

#Terminación del primer for
Todo_Analytics = pd.concat(Todo_Analytics)

Todo_Analytics['fechas'] = [ re.findall( r"\d{8}-\d{8}" ,i) for i in Todo_Analytics.archivo ]
#Validaciones

#Todo_Analytics.keys()
#a = Todo_Analytics.groupby(['Marca','Tipo','archivo']).count()
#Todo_Analytics.Marca.value_counts()
#Trabajar las fechas para conocer el Mes

####################################################FIN ANALYTICS#############################################################


#filtro = Union_Analytics[Union_Analytics.Fuente_Medio == 'Adsocial_FB / ANUNCIO_HYPERX_02_AL_31_OCTUBRE']

#Cruzar con un reporte de producto

#Conexion con Google Sheets, usando las paqueterias gspread, oauth2client, gspread_dataframe
#Credenciales cred.json
#os.chdir('/home/carlos/Documentos/Adsocial')
#os.listdir()
#Autentificacion con google cloud platform correo analytics.adsocial@gmail.com
#scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
#creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
#client = gspread.authorize(creds)

#Exportacion de la informacion
#sh = client.open('Copy of DASHBOARD GG - Reporte ROAS MES A MES') #Recordar que el archivo que deseamos leer tiene que tener el correo de la api como persona compartida
#worksheet = sh.get_worksheet(1) #Base_master_python


#worksheet = sh.get_worksheet(2) #Union_Analytics_python
#set_with_dataframe(worksheet, Todo_Analytics)

#Extraccion de datos sheets
#datos = worksheet.get_all_values()
#datos = pd.DataFrame(datos)

#Extraccion con get_as_dataframe
#df2 = get_as_dataframe(worksheet)
#df = get_as_dataframe(worksheet, parse_dates=True, usecols=[0,2], skiprows=1, header=None)

Todo_Analytics.to_csv('/home/carlos/Documentos/Adsocial/Sheets/Informacion_final/Todo_Analytics.csv')


