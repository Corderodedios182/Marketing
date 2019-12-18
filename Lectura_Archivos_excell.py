#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 13:20:36 2019

@author: carlos

Nota importante: Los archivos tienen que tener codificación utf-8

El siguiente script une la iformación de varias fuentes, al final crea la base que debe subirse al sheets

- Facebook: Se descargan reportes mensuales por Marca de las plataformas
  Respetando el nombre de la plataforma: Office-Depot-Campañas-1-abr-2019-30-abr-2019.csv

- Adwords: Solo se descarga un reporte al Mes KPI , al nombrar el archivo debemos colocar la fecha de la siguiente manera:
         KPI_1-feb-2019-29-feb-2019.csv

- Adform: Se extraen de los sheets de los Operadores se descarga en un csv la hoja llamada General y cuidar el nombre de las columnas
  Renombrar el nombre del reporte que contenga la fecha de la siguiente manera: 
      1-ene-2020-30-ene-2020

Las columnas que recabo son: 
    'Archivo', 'Clics', 'Fecha_Fin', 'Fecha_inicio', 'Impresiones', 'Marca','Mes', 'Nombre_Campaña', 'Plataforma', 'dinero_gastado'

"""

###Paqueterias
import os 
import pandas as pd
import re

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

Union_FB.columns = ['Nombre_Campaña','Fecha_inicio','Fecha_Fin','Marca','Archivo','Clics','dinero_gastado','Impresiones']
Union_FB['Plataforma'] = 'Facebook'
Union_FB['Mes'] = ''

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
        #En ocasiones por el formato no leía el archivo utf-
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

Union_Ad.Fecha_Fin = Union_Ad.Fecha_Fin.apply(lambda x : str(x).replace(' --','')).astype('str')

#Validaciones
#Union_Ad.Marca.value_counts()

#########################
#Adform/Sizmek (display)#
#########################

#Archivos de Pao
os.chdir('/home/carlos/Documentos/Adsocial/Sheets/Adform')
Archivos = os.listdir()

Union_Adf_nuevo = []

for csv in Archivos:
    try:
        tmp = pd.read_csv(csv, skiprows = 1)
        tmp = tmp.iloc[:-2,:]
        tmp['Archivo'] = csv
        Union_Adf_nuevo.append(tmp)
    except:
        print('Alguno archivo no es csv')

Union_Adf_nuevo = pd.concat(Union_Adf_nuevo).reset_index(drop = True)
Union_Adf_nuevo['Plataforma'] = 'Adform'
Union_Adf_nuevo['Mes'] = ''
#De nomviembre para adelante tomo impresiones de Adform
#Seleccion de columnas necesarios
Union_Adf_nuevo = Union_Adf_nuevo.loc[:,('Mes','Archivo','Campaña','Fecha Inicio','Fecha Fin','Marca','KPI Entregado Adform','Clics Adform','$$ Planeada MXN','Plataforma')]
Union_Adf_nuevo.columns = ['Mes','Archivo','Nombre_Campaña','Fecha_inicio','Fecha_Fin','Marca','Impresiones','Clics','dinero_gastado','Plataforma'] 

Union_Adf_nuevo.loc[Union_Adf_nuevo.Nombre_Campaña.str.contains('Petco') | Union_Adf_nuevo.Nombre_Campaña.str.contains('PC'), 'Marca'] = 'Petco'
Union_Adf_nuevo.loc[Union_Adf_nuevo.Nombre_Campaña.str.contains('Office') | Union_Adf_nuevo.Nombre_Campaña.str.contains('OD'), 'Marca'] = 'Office Depot MEX'
Union_Adf_nuevo.loc[Union_Adf_nuevo.Nombre_Campaña.str.contains('RadioShack') | Union_Adf_nuevo.Nombre_Campaña.str.contains('RS'), 'Marca'] = 'Radioshack'

Union_Adf_nuevo.Fecha_inicio = pd.to_datetime(Union_Adf_nuevo.Fecha_inicio, errors = 'coerce', format = '%d/%m/%Y')
Union_Adf_nuevo.Fecha_Fin = pd.to_datetime(Union_Adf_nuevo.Fecha_Fin,errors = 'coerce', format = '%d/%m/%Y')

Union_Adf_nuevo.Fecha_inicio = Union_Adf_nuevo.Fecha_inicio.apply(lambda x: x.date())
Union_Adf_nuevo.Fecha_Fin = Union_Adf_nuevo.Fecha_Fin.apply(lambda x: x.date())

Union_Adf_nuevo.Clics.fillna(0, inplace=True)
Union_Adf_nuevo.Clics = Union_Adf_nuevo.Clics.apply(lambda x : str(x).replace(',','')).astype('float').astype('int')
Union_Adf_nuevo.Impresiones = Union_Adf_nuevo.Impresiones.apply(lambda x: str(x).replace(',','')).astype('int')
Union_Adf_nuevo.dinero_gastado = Union_Adf_nuevo.dinero_gastado.apply(lambda x: str(x).replace('$',''))
Union_Adf_nuevo.dinero_gastado = Union_Adf_nuevo.dinero_gastado.apply(lambda x: str(x).replace(',','')).astype('float')

#Historico
#Antes de septiembre tomo impresiones de SAS
Acumulado = pd.read_excel('Historico/Acumulado Reporte DSP.xlsx') 
#Acumulado.keys() #Ya vienen columnas que nos ayudan con info de los MP
Acumulado['Plataforma'] = 'Adform'
Acumulado['Archivo'] = 'Acumulado Reporte DSP.xlsx'
#Acumulado.keys() ya tenemos columnas que facilitan uniones futuras, solo tomo estas para el caso del archivo primera_base_master
Acumulado = Acumulado.loc[:,('Mes','Archivo','Campaña','Fecha Inicio','Fecha Fin','Marca','KPI Entregado','CLICKS','MP Planeada','Plataforma')]
Acumulado.columns = ['Mes','Archivo','Nombre_Campaña','Fecha_inicio','Fecha_Fin','Marca','Impresiones','Clics','dinero_gastado','Plataforma'] 

#Colocación de la columna Marca
Acumulado.loc[Acumulado.Nombre_Campaña.str.contains('Petco') | Acumulado.Nombre_Campaña.str.contains('PC'), 'Marca'] = 'Petco'
Acumulado.loc[Acumulado.Nombre_Campaña.str.contains('Office') | Acumulado.Nombre_Campaña.str.contains('OD'), 'Marca'] = 'Office Depot MEX'
Acumulado.loc[Acumulado.Nombre_Campaña.str.contains('RadioShack') | Acumulado.Nombre_Campaña.str.contains('RS'), 'Marca'] = 'Radioshack'

Acumulado.Fecha_inicio = pd.to_datetime(Acumulado.Fecha_inicio, errors = 'coerce', format = '%d/%m/%Y')
Acumulado.Fecha_Fin = pd.to_datetime(Acumulado.Fecha_Fin,errors = 'coerce', format = '%d/%m/%Y')

Acumulado.Fecha_inicio = Acumulado.Fecha_inicio.apply(lambda x: x.date())
Acumulado.Fecha_Fin = Acumulado.Fecha_Fin.apply(lambda x: x.date())

Union_Adf = pd.concat([Union_Adf_nuevo,Acumulado])

###################
#Union de Archivos#
###################

Base_master = pd.concat([Union_FB,Union_Ad,Union_Adf], axis = 0)
Base_master.Fecha_inicio = pd.to_datetime(Base_master.Fecha_inicio)

print("Facebook : " + str(Union_FB.shape)) ; print("Adwords : " + str(Union_Ad.shape)) ; print("Adform : " + str(Union_Adf.shape)) ; print("Total : " + str(Union_FB.shape[0] + Union_Ad.shape[0] + Union_Adf.shape[0]))
del Union_Ad, Union_Adf, Union_Adf_nuevo, Union_FB,tmp, Archivos, csv, Informacion_Facebook, fallas, Acumulado

########
#Fechas#
########
#Extreamos las fechas del nombre del reporte
Fechas = list(Base_master.Archivo.unique())

#####Se extrae la fecha de la columna Archivo, para crear Fecha_inicio_reporte y Fecha_fin_reporte

Base_master['Archivo_fechas'] = Base_master['Archivo']

for word, initial in {"ene":"1", "feb":"2","mar":"3", "abr":"4","may":"5", "jun":"6","jul":"7", "ago":"8","sep":"9", "oct":"10","nov":"11", "dic":"12"}.items():
    Base_master.Archivo_fechas = Base_master.Archivo_fechas.str.replace(str(word),str(initial))

Base_master['fecha_reporte'] = [re.findall(r"\d{1}-\d{1}-\d{4}|\d{2}-\d{1}-\d{4}|\d{1}-\d{2}-\d{4}|\d{2}-\d{2}-\d{4}", i) 
                                for i in list(Base_master.Archivo_fechas)]

fechas = [re.findall(r"\d{1}-\d{1}-\d{4}|\d{2}-\d{1}-\d{4}|\d{1}-\d{2}-\d{4}|\d{2}-\d{2}-\d{4}", i) for i in list(Base_master.Archivo_fechas)]

fechas = pd.DataFrame(fechas)
fechas.columns = ['Fecha_inicio_reporte','Fecha_fin_reporte']

Base_master = pd.concat([Base_master.reset_index(drop=True),pd.DataFrame(fechas)], axis=1)

del Fechas, fechas, initial, word
#Formato correcto para trabajar con las fechas

#ok
Base_master['t_fecha_fin'] =  pd.to_datetime(Base_master.loc[:,'Fecha_Fin'],errors='ignore',
                              format='%Y-%m-%d')
#ok
Base_master['t_fecha_inicio'] =  pd.to_datetime(Base_master['Fecha_inicio'],
                              format='%Y-%m-%d')
#ok
Base_master['t_fecha_inicio_reporte'] =  pd.to_datetime(Base_master['Fecha_inicio_reporte'],
                              format='%d-%m-%Y')

#ok
Base_master['t_fecha_fin_reporte'] =  pd.to_datetime(Base_master['Fecha_fin_reporte'],errors='coerce',
                              format='%d-%m-%Y')

#Reglas para determinar los dias de duracion de una campaña en un mes
#Fecha inicio reporte
def fechas_inicio(x,y):
    if x <= y:
        return y
    else:
        return x
    
Base_master['inicio'] = [fechas_inicio(x,y) for x, y in zip(Base_master.t_fecha_inicio_reporte,Base_master.t_fecha_inicio)] #Este es el bueno

#Fecha fin reporte
def fechas_fin(x,y):
    if x <= y:
        return x
    else:
        return y
    
Base_master['fin'] = [fechas_fin(x,y) for x, y in zip(Base_master.t_fecha_fin_reporte,Base_master.t_fecha_fin)] #Este es el bueno

#Fechas faltantes 
Base_master['fin'] = Base_master.fin.fillna(0)

def fechas_vacias(x,y):
    if x == 0:
        return y
    else:
        return x

Base_master['fin'] = [fechas_vacias(x,y) for x, y in zip(Base_master.fin, Base_master.t_fecha_fin_reporte)]

Base_master['dias'] = Base_master.fin - Base_master.inicio

#Tengo días negativos

#Columna mes
Base_master['Mes'] = Base_master.inicio.apply(lambda x : x.month)
Base_master['Año'] = Base_master.inicio.apply(lambda x : x.year)

#Columnas que se muestran en el archivo del sheets
Base_master_final = Base_master.loc[:,('Archivo','Marca','Plataforma','Nombre_Campaña','Mes','Año','inicio','fin','dias','t_fecha_inicio_reporte','t_fecha_fin_reporte','Impresiones','Clics','dinero_gastado')]

#########################################
#Escritura de los datos en Google Sheets#
#########################################
import os
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe #,get_as_dataframe

Escribir = input("Deseas escribir los datos en sheets si/no : ")

if Escribir == 'si':
    os.chdir('/home/carlos/Documentos/Adsocial')
    os.listdir()
    #Autentificacion con google cloud platform correo analytics.adsocial@gmail.com
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)

    Base_master_final['ultima_actualizacion'] = datetime.now()
    
    sh = client.open('Copy of DASHBOARD GG - Reporte ROAS MES A MES') #Recordar que el archivo que deseamos leer tiene que tener el correo de la api como persona compartida
    worksheet = sh.get_worksheet(1) #Base_master_python

    filas = len(worksheet.get_all_values()) + 1
    set_with_dataframe(worksheet, Base_master_final, row = filas, include_column_header = False)

else: 
    print("Ok!")    

#Agregar que valide la información que ya existe por nombre de Archivo

#Tengo problemas con adwords
    #Volver a bajar el reporte
tmp = Base_master_final[Base_master_final.Plataforma == 'Facebook']
#Facebook necesito los reportes en formato csv

#Adform no se cual es la información




