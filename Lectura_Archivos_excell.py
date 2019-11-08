#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 13:20:36 2019

@author: carlos
"""
import os 
import datetime
import pandas as pd

os.getcwd()
os.chdir('/home/carlos/Documentos/Adsocial/Sheets/')
os.listdir()

####
#FB#
####
os.chdir('/home/carlos/Documentos/Adsocial/Sheets/Facebook')
Archivos = os.listdir()

#Leyendo todos los archivos e irlos guardando
Union_FB = []

for csv in Archivos:
    tmp = pd.read_csv(csv, parse_dates = ['Inicio','Finalización','Inicio del informe','Fin del informe'])
    tmp['Marca'] = csv.split("-",1)[0]
    Union_FB.append(tmp)

Union_FB = pd.concat(Union_FB)
#Se agrupan por campaña y se respentan las fechas maximas de la diferencia Fin - Inicio
#tmp = Union_FB[Union_FB.iloc[:,2] == '1910_OD _VENTA_MKT_NOCTURNA_2019']

Union_FB = Union_FB.groupby(['Nombre de la campaña','Inicio','Finalización','Marca'], as_index = False).sum() 
#tmp_1 = Union_FB[Union_FB.iloc[:,0] == '1910_OD _VENTA_MKT_NOCTURNA_2019']

Union_FB.columns = ['Nombre_Campaña','Fecha_inicio','Fecha_Fin','Marca','Impresiones','Clics','dinero_gastado']
Union_FB['Plataforma'] = 'Facebook'

#Colocación de Marcas
Union_FB.loc[Union_FB.Marca.str.contains('Radio'),'Marca'] = 'Radioshack'
Union_FB.loc[Union_FB.Marca.str.contains('Office'),'Marca'] = 'Office Depot MEX'
Union_FB.loc[(Union_FB.Nombre_Campaña.str.contains('CAM')) & (Union_FB.Nombre_Campaña.str.contains('CR')) ,'Marca'] = 'Office Depot CAM Costa Rica*'
Union_FB.loc[(Union_FB.Nombre_Campaña.str.contains('CAM')) & (Union_FB.Nombre_Campaña.str.contains('GT')) ,'Marca'] = 'Office Depot CAM Guatemala*'
Union_FB.loc[(Union_FB.Nombre_Campaña.str.contains('CAM')) & (Union_FB.Nombre_Campaña.str.contains('HN')) ,'Marca'] = 'Office Depot CAM Honduras*'
Union_FB.loc[(Union_FB.Nombre_Campaña.str.contains('CAM')) & (Union_FB.Nombre_Campaña.str.contains('PA')) ,'Marca'] = 'Office Depot CAM Panamá*'
Union_FB.loc[(Union_FB.Nombre_Campaña.str.contains('CAM')) & (Union_FB.Nombre_Campaña.str.contains('SV')) ,'Marca'] = 'Office Depot CAM El Salvador*'

Union_FB.Fecha_inicio = Union_FB.Fecha_inicio.apply(lambda x: x.date())
Union_FB.Fecha_Fin = Union_FB.Fecha_Fin.apply(lambda x: x.date())

#########
#Adwords#
#########
os.chdir('/home/carlos/Documentos/Adsocial/Sheets/Adwords')
Archivos = os.listdir()

Union_Ad = []

for csv in Archivos:
    tmp = pd.read_csv(csv, skiprows = 2, parse_dates = ['Fecha de inicio','Fecha de finalización'])
    Union_Ad.append(tmp)

Union_Ad = pd.concat(Union_Ad).reset_index(drop = True)

Union_Ad = Union_Ad.loc[:,('Campaña','Fecha de inicio','Fecha de finalización','Cuenta','Impresiones','Clics','Costo'),]
Union_Ad.columns = ['Nombre_Campaña','Fecha_inicio','Fecha_Fin','Marca','Impresiones','Clics','dinero_gastado']
Union_Ad['Plataforma'] = 'Adwords'

Union_Ad.Clics = Union_Ad.Clics.apply(lambda x : str(x).replace(',','')).astype('int')
Union_Ad.Impresiones = Union_Ad.Impresiones.apply(lambda x: str(x).replace(',','')).astype('int')
Union_Ad.dinero_gastado = Union_Ad.dinero_gastado.apply(lambda x: str(x).replace(',','')).astype('float')

Union_Ad.Fecha_inicio = Union_Ad.Fecha_inicio.apply(lambda x: x.date())

Union_Ad.loc[(Union_Ad.Marca.str.contains('Office') | Union_Ad.Marca.str.contains('OD')) & (~Union_Ad.Marca.str.contains('CAM')) , 'Marca'] = 'Office Depot MEX'
Union_Ad.loc[Union_Ad.Marca.str.contains('Petco'),'Marca'] = 'Petco'
Union_Ad.loc[Union_Ad.Marca.str.contains('RS'), 'Marca'] = 'Radioshack'

########
#Adform#
########
os.chdir('/home/carlos/Documentos/Adsocial/Sheets/Adform')
Archivos = os.listdir()

Union_Adf = []

for csv in Archivos:
    tmp = pd.read_csv(csv, skiprows = 1)
    tmp = tmp.iloc[:-2,:]
    Union_Adf.append(tmp)

#Puede existir diferencias en las columnas, revisar por si las dudas
#tmp_f = []

#for csv in Archivos:
#    tmp = pd.read_csv(csv, skiprows = 1,parse_dates = ['Fecha Inicio','Fecha Fin'])
#    tmp = tmp.iloc[:-2,:]
#    tmp = tmp.keys()
#    tmp_f.append(tmp)

#tmp_f = pd.DataFrame(tmp_f)

Union_Adf = pd.concat(Union_Adf).reset_index(drop = True)
Union_Adf['Plataforma'] = 'Adform'
#Antes de septiembre tomo impresiones de SAS
#De nomviembre para adelante tomo impresiones de Adform

#Colocación de la columna Marca
Union_Adf.loc[Union_Adf.Campaña.str.contains('Petco') | Union_Adf.Campaña.str.contains('PC'), 'Marca'] = 'Petco'
Union_Adf.loc[Union_Adf.Campaña.str.contains('Office') | Union_Adf.Campaña.str.contains('OD'), 'Marca'] = 'Office Depot MEX'
Union_Adf.loc[Union_Adf.Campaña.str.contains('RadioShack') | Union_Adf.Campaña.str.contains('RS'), 'Marca'] = 'Radioshack'

#Seleccion de columnas necesarios

Union_Adf = Union_Adf.loc[:,('Campaña','Fecha Inicio','Fecha Fin','Marca','KPI Entregado Adform','Clics Adform','$$ Planeada MXN','Plataforma')]

Union_Adf.columns = ['Nombre_Campaña','Fecha_inicio','Fecha_Fin','Marca','Impresiones','Clics','dinero_gastado','Plataforma'] 

#Formato adecuado para homologar datos
Union_Adf.Fecha_inicio = Union_Adf.Fecha_inicio.apply(lambda x: datetime.datetime.strptime(x,"%d/%m/%Y").strftime("%Y-%m-%d"))
Union_Adf.Fecha_Fin = Union_Adf.Fecha_Fin.apply(lambda x: datetime.datetime.strptime(x,"%d/%m/%Y").strftime("%Y-%m-%d"))

Union_Adf.Fecha_inicio = pd.to_datetime(Union_Adf.Fecha_inicio)
Union_Adf.Fecha_Fin = pd.to_datetime(Union_Adf.Fecha_Fin)

Union_Adf.Fecha_inicio = Union_Adf.Fecha_inicio.apply(lambda x: x.date())
Union_Adf.Fecha_Fin = Union_Adf.Fecha_Fin.apply(lambda x: x.date())

Union_Adf.Clics.fillna(0, inplace=True)
Union_Adf.Clics = Union_Adf.Clics.apply(lambda x : str(x).replace(',','')).astype('int')
Union_Adf.Impresiones = Union_Adf.Impresiones.apply(lambda x: str(x).replace(',','')).astype('int')
Union_Adf.dinero_gastado = Union_Adf.dinero_gastado.apply(lambda x: str(x).replace('$',''))
Union_Adf.dinero_gastado = Union_Adf.dinero_gastado.apply(lambda x: str(x).replace(',','')).astype('float')

#Lectura de un archivo de sheets hoja General

###################
#Union de Archivos#
###################

Base_master = pd.concat([Union_FB,Union_Ad,Union_Adf], axis = 0)
Base_master.Fecha_inicio = pd.to_datetime(Base_master.Fecha_inicio)

os.chdir('/home/carlos/Documentos/Adsocial/Sheets/')
Base_master.to_csv('Base_master.csv')
print("Adwords : " + str(Union_Ad.shape)) ; print("Adform : " + str(Union_Adf.shape)) ; print("Facebook : " + str(Union_FB.shape)) ; print("Total : " + str(Union_Ad.shape[0] + Union_Adf.shape[0] + Union_FB.shape[0]))
del Union_Ad, Union_Adf, Union_FB,tmp

###########
#Analytics#
###########
os.chdir('/home/carlos/Documentos/Adsocial/Sheets/Analytics/Office Depot')
Archivos = pd.Series(os.listdir())

#Conversiones Asistidas
tmp_conversiones = list(Archivos[Archivos.str.contains('Conver')])
tmp_conversiones = pd.read_csv(tmp_conversiones[0], skiprows = 6)
tmp_conversiones = tmp_conversiones.loc[:,('Fuente/Medio','Campaña','Conversiones asistidas','Valor de las conversiones asistidas')]
tmp_conversiones.columns = ['Fuente_Medio','Nombre_Campaña','Conversiones','Revenue']
tmp_conversiones = tmp_conversiones.iloc[:-3,:]
tmp_conversiones['Tipo'] = 'Asistida'

tmp_conversiones.Conversiones = tmp_conversiones.Conversiones.astype('int')

tmp_conversiones.Revenue = tmp_conversiones.Revenue.apply(lambda x : str(x).replace('.',''))
tmp_conversiones.Revenue = tmp_conversiones.Revenue.apply(lambda x : str(x).replace(',','.'))
tmp_conversiones.Revenue = tmp_conversiones.Revenue.apply(lambda x : str(x).replace('MXN','')).astype('float')

#Conversiones todo el trafico
tmp_trafico = list(Archivos[Archivos.str.contains('Todo el ')])
xls = pd.ExcelFile(tmp_trafico[0])
tmp_trafico = pd.read_excel(xls, 'Conjunto de datos1')
tmp_trafico = tmp_trafico.loc[:,('Fuente/Medio','Campaña','Transacciones','Ingresos')]
tmp_trafico.columns = ['Fuente_Medio','Nombre_Campaña','Conversiones','Revenue']
tmp_trafico['Tipo'] = 'Directa'
tmp_trafico = tmp_trafico.iloc[:-1,:]

tmp_trafico.Conversiones = tmp_trafico.Conversiones.astype('int')

#Union de los 2 tmp
Union_Analytics = pd.concat([tmp_conversiones,tmp_trafico])
Union_Analytics['Marca'] = 'Office Depot MEX'
del tmp_conversiones, tmp_trafico

#filtro = Union_Analytics[Union_Analytics.Fuente_Medio == 'Adsocial_FB / ANUNCIO_HYPERX_02_AL_31_OCTUBRE']
os.chdir('/home/carlos/Documentos/Adsocial/Sheets/')
Union_Analytics.to_csv('Union_Analytics.csv')

#Preguntas sobre Analytics

#Cruzar con un reporte de producto

#Api para poder leer de sheets, info de Adform
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

os.chdir('/home/carlos/Documentos/Adsocial')
os.listdir()

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

client = gspread.authorize(creds)

sh = client.open('Copy of DASHBOARD GG - Reporte ROAS MES A MES')
worksheet = sh.get_worksheet(1)
datos = worksheet.get_all_values()
datos = pd.DataFrame(datos)

worksheet.insert_row(Base_master)
####################







