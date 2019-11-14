#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 13:20:36 2019

@author: carlos

El siguiente script une la iformación de varias fuentes, al final crea 2 bases. bases_master, Todo_Analytics

Facebook: Se descargan reportes mensuales por Marca de las plataformas
Adwords: Solo se descarga un reporte al Mes KPI
Adform: Se extraen de los sheets de los Operadores

Analytics: Se divide el reporte por Conversiones y trafico por Marca

"""

###Paqueterias

import os 
import datetime
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe #,get_as_dataframe

###Rutas

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
filas = []
archivo = []
columnas = []

for csv in Archivos:
    
    tmp = pd.read_csv(csv, parse_dates = ['Inicio','Finalización','Inicio del informe','Fin del informe'])
    tmp['Marca'] = csv.split("-",1)[0]
    tmp['Archivo'] = csv
    
    filas.append(tmp.shape[0])
    columnas.append(tmp.shape[1])
    archivo.append(csv)
    Union_FB.append(tmp)

Union_FB = pd.concat(Union_FB)

#Funcion para Informacion de los archivos
def lists2dict(list1, list2):
    """list1 devuelve las llaves y list2 los elementos"""

    # Unimos con la funcion zip()
    zipped_lists = zip(list1, list2)

    # Lo volvemos diccionario
    rs_dict = dict(zipped_lists)

    return rs_dict

Informacion_Facebook = pd.DataFrame([lists2dict(['Archivo','columnas','filas'],sublista) for sublista in zip(archivo,columnas,filas)])
del filas, columnas, archivo, csv, tmp, Archivos

if Union_FB.shape[0] == Informacion_Facebook.filas.sum():
    print("La union Facebook es correcta el numero de filas por cada archivo corresponde al concatenado")
else:
    print("Hubo un error al concatenar Facebook")

#Se agrupan por campaña y se respentan las fechas maximas de la diferencia Fin - Inicio
#tmp = Union_FB[Union_FB.loc[:,'Archivo'] == 'Office-Depot-Campañas-1-nov-2018-30-nov-2018.csv']

Union_FB = Union_FB.groupby(['Nombre de la campaña','Inicio','Finalización','Marca','Archivo'], as_index = False).sum()
#tmp_1 = Union_FB[Union_FB.iloc[:,0] == '1910_OD _VENTA_MKT_NOCTURNA_2019']

Union_FB.columns = ['Nombre_Campaña','Fecha_inicio','Fecha_Fin','Marca','Archivo','Impresiones','Clics','dinero_gastado']
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

Informacion_Facebook = pd.merge(Informacion_Facebook,Union_FB.groupby(['Archivo'], as_index = False).sum(),how = 'left', on = 'Archivo')

####Validaciones para las fechas agrupaciones por Mes
#a = Union_FB.Nombre_Campaña.value_counts()
#b = Union_FB[Union_FB.Nombre_Campaña == '1811_PETCO_Fulltrust_FB']

#########
#Adwords#
#########

#Ruta
os.chdir('/home/carlos/Documentos/Adsocial/Sheets/Adwords')
Archivos = pd.Series(os.listdir())

#Union de Archivos
Union_Ad = []
fallas = []

for csv in Archivos:
    try:
        tmp = pd.read_csv(csv, sep = ',', skiprows = 2)
        tmp['Archivo'] = csv
        Union_Ad.append(tmp)
    except:
        fallas.append(csv)

Union_Ad = pd.concat(Union_Ad).reset_index(drop = True)

Union_Ad.Archivo.value_counts()
print("Archivo que fallaron: " + str(fallas))

#Formato para la union con las demás bases

Union_Ad = Union_Ad.loc[:,('Archivo','Campaña','Fecha de inicio','Fecha de finalización','Cuenta','Impresiones','Clics','Costo'),]
Union_Ad.columns = ['Archivo','Nombre_Campaña','Fecha_inicio','Fecha_Fin','Marca','Impresiones','Clics','dinero_gastado']
Union_Ad['Plataforma'] = 'Adwords'

Union_Ad.Clics = Union_Ad.Clics.apply(lambda x : str(x).replace(',','')).astype('int')
Union_Ad.Impresiones = Union_Ad.Impresiones.apply(lambda x: str(x).replace(',','')).astype('int')
Union_Ad.dinero_gastado = Union_Ad.dinero_gastado.apply(lambda x: str(x).replace(',','')).astype('float')

Union_Ad.loc[(Union_Ad.Marca.str.contains('Office') | Union_Ad.Marca.str.contains('OD')) & (~Union_Ad.Marca.str.contains('CAM')) , 'Marca'] = 'Office Depot MEX'
Union_Ad.loc[Union_Ad.Marca.str.contains('Petco') | Union_Ad.Marca.str.contains('PETCO'),'Marca'] = 'Petco'
Union_Ad.loc[Union_Ad.Marca.str.contains('RS') | Union_Ad.Marca.str.contains('Radioshack') | Union_Ad.Marca.str.contains('RadioShack'), 'Marca'] = 'Radioshack'

#Validaciones
#Union_Ad.Marca.value_counts()

#########################
#Adform/Sizmek (display)#
#########################

os.chdir('/home/carlos/Documentos/Adsocial/Sheets/Adform/Bitácoras AdOps')
Archivos = os.listdir()

#Archivos = Archivos[:5]

columnas = []

for data in Archivos:
    xls = pd.ExcelFile(data) #Conexion con el archivo
    base = pd.read_excel(xls, sheet_name = 'GENERAL', skiprows = 1) #Lectura del arhivo
    try:
        tmp = [i for i, x in enumerate(base.iloc[:,0] == 'Total') if x][0] #Si non tengo el total informo el archivo
    except IndexError:
        print(data)
    
    columnas.append(base.keys())
    #base.loc[:,('Campaña','Fecha Inicio','Fecha Fin','Marca','KPI Entregado Adform','Clics Adform','$$ Planeada MXN','Plataforma')]

tmp = pd.DataFrame(columnas)

#Puede existir diferencias en las columnas, revisar por si las dudas
Union_FB = []
filas = []
archivo = []
columnas = []

for csv in Archivos:
    tmp = pd.read_csv(csv, parse_dates = ['Inicio','Finalización','Inicio del informe','Fin del informe'])
    tmp['Marca'] = csv.split("-",1)[0]
    tmp['Archivo'] = csv
    filas.append(tmp.shape[0])
    columnas.append(tmp.shape[1])
    archivo.append(csv)
    Union_FB.append(tmp)

Union_FB = pd.concat(Union_FB)
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

Base_master = pd.concat([Union_FB,Union_Ad], axis = 0)
Base_master.Fecha_inicio = pd.to_datetime(Base_master.Fecha_inicio)

print("Adwords : " + str(Union_Ad.shape)) ; print("Facebook : " + str(Union_FB.shape)) ; print("Total : " + str(Union_Ad.shape[0] + Union_FB.shape[0]))
del Union_Ad, Union_Adf, Union_FB,tmp

####################################################FIN ARCHIVOS CAMPAÑAS###########################################################

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

#Validaciones

#Todo_Analytics.keys()
#a = Todo_Analytics.groupby(['Marca','Tipo','archivo']).count()
#Todo_Analytics.Marca.value_counts()
#Trabajar las fechas para conocer el Mes

####################################################FIN ANALYTICS#############################################################


#filtro = Union_Analytics[Union_Analytics.Fuente_Medio == 'Adsocial_FB / ANUNCIO_HYPERX_02_AL_31_OCTUBRE']
os.chdir('/home/carlos/Documentos/Adsocial/Sheets/')
Union_Analytics.to_csv('Union_Analytics.csv')


#Cruzar con un reporte de producto

#Conexion con Google Sheets, usando las paqueterias gspread, oauth2client, gspread_dataframe
#Credenciales cred.json
os.chdir('/home/carlos/Documentos/Adsocial')
os.listdir()
#Autentificacion con google cloud platform correo analytics.adsocial@gmail.com
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)

#Exportacion de la informacion
sh = client.open('Copy of DASHBOARD GG - Reporte ROAS MES A MES') #Recordar que el archivo que deseamos leer tiene que tener el correo de la api como persona compartida
worksheet = sh.get_worksheet(1) #Base_master_python
set_with_dataframe(worksheet, Base_master)

worksheet = sh.get_worksheet(2) #Union_Analytics_python
set_with_dataframe(worksheet, Union_Analytics)

#Extraccion de datos sheets
datos = worksheet.get_all_values()
datos = pd.DataFrame(datos)

#Extraccion con get_as_dataframe
#df2 = get_as_dataframe(worksheet)
#df = get_as_dataframe(worksheet, parse_dates=True, usecols=[0,2], skiprows=1, header=None)

for i in Archivos:
    print(i)



