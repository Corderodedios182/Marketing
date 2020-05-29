#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 13:51:42 2020

@author: carlos

Descripcion: Visualización de la información de Google Analytics:
    
    Productos más vendidos por mes
    1.General
    2.Edad
    3.Región
    4.Sexo

Solo tomar 2019, agregar homestore

Primero se importan todos los archivos -> se limpian y agrupan -> se grafican

Funciones de apoyo para el cuaderno jupyter Reporte analytics

"""


#Paqueterías
import os 
import re 
import pandas as pd
import plotly.offline as pyo
import plotly.express as px
import plotly.graph_objects as go
import glob
import random
analysis = 'segmentos_intencion_compra'
nivel = 'Audiencia'
Cuenta = ['Office Depot']
i = 0
pd.set_option('display.float_format', lambda x: '%.f' % x)

#--          UNION DE LOS DIFERENTES ARCHIVOS DE GOOGLE ANALYTICS       --#

#Une todos los archivos de productos de las cuentas.
def Union_Archivos(Cuenta, analysis = '', nivel = ''):
    
    if nivel == 'Productos':
        
        analytics_union = []
    
        for i in range(len(Cuenta)):
            archivos = glob.glob("/home/carlos/Dropbox/Históricos GG/Históricos GG/" + Cuenta[i] + "/G Analytics/Productos/" + analysis + "/*.xlsx")
            
            # Productos por Campaña #
            for xls in archivos:
                tmp = pd.ExcelFile(xls)
                tmp = pd.read_excel(xls, 'Conjunto de datos1')
                tmp['archivo'] = xls
                tmp = tmp.iloc[:-1]
                tmp['cuenta'] = Cuenta[i]
                analytics_union.append(tmp)
                    
        analytics_union = pd.concat(analytics_union)

        analytics_union['fechas'] = [ re.findall( r"\d{8}-\d{8}" ,i) for i in analytics_union.archivo ]
                    
    elif nivel == 'Audiencia':
        
        analytics_union = []
        
        for i in range(len(Cuenta)):
            archivos = glob.glob("/home/carlos/Dropbox/Históricos GG/Históricos GG/" + Cuenta[i] + "/G Analytics/Audiencia/" + analysis + "/*.xlsx")
            
            # Productos por Campaña #
            
            for xls in archivos:
                tmp = pd.ExcelFile(xls)
                tmp = pd.read_excel(xls, 'Conjunto de datos1')
                tmp['archivo'] = xls
                tmp = tmp.iloc[:-1]
                tmp['cuenta'] = Cuenta[i]
                analytics_union.append(tmp)
                
        analytics_union = pd.concat(analytics_union)

        analytics_union['fechas'] = [ re.findall( r"\d{8}-\d{8}" ,i) for i in analytics_union.archivo ]
                    
    elif nivel == 'Tráfico':
        
        analytics_union = []
        
        for i in range(len(Cuenta)):
            archivos = glob.glob("/home/carlos/Dropbox/Históricos GG/Históricos GG/" + Cuenta[i] + "/G Analytics/Tráfico/*.xlsx")
            
            # Productos por Campaña #
            for xls in archivos:
                    tmp = pd.ExcelFile(xls)
                    tmp = pd.read_excel(xls, 'Conjunto de datos1')
                    tmp['archivo'] = xls
                    tmp = tmp.iloc[:-1]
                    tmp['cuenta'] = Cuenta[i]
                    analytics_union.append(tmp)
        
        analytics_union = pd.concat(analytics_union)

        analytics_union['fechas'] = [ re.findall( r"\d{8}-\d{8}" ,i) for i in analytics_union.archivo ]
        
    return analytics_union

tmp = Union_Archivos(Cuenta = ['Office Depot'], analysis = 'segmentos_intencion_compra', nivel = 'Audiencia')
analytics_productos = Union_Archivos(Cuenta = ['Office Depot','Petco','RadioShack','Home Store'], nivel = "Tráfico")
analytics_productos = analytics_productos.fillna('vacio')
tmp = analytics_productos.head()

tmp


###############################################################################################
#
#                                               LIMPIEZA DE DATOS
#
# 1.Formato de fechas, colocamos la fecha del reporte para extraer el mes del reporte
# 2.Reducción del nombre del producto tomando las primeras 3 palabras
# 3.Agrupacion por mes, cuenta, producto_nuevo
# 4.Limpiamos la fuente de medios
#
# Objetivo: tenero mayor claridad de los datos.
###############################################################################################

#Fechas
def Formato_Fechas_Analytics(Base, Columna):

    fechas = Base[Columna].astype(str).str.split("-",expand = True)
    fechas = pd.DataFrame(fechas)
    fechas.columns = ['Fecha_inicio','Fecha_fin']
     
    Base['Fecha_inicio'] = fechas.iloc[:,0]
    Base['Fecha_fin'] = fechas.iloc[:,1]
       
    Base.Fecha_inicio = Base.Fecha_inicio.apply(lambda x: str(x).replace("['",""))
    Base.Fecha_fin = Base.Fecha_fin.apply(lambda x: str(x).replace("']",""))
    
    Base.Fecha_inicio = pd.to_datetime(Base.Fecha_inicio,format = "%Y%m%d")
    Base.Fecha_fin = pd.to_datetime(Base.Fecha_fin,format = "%Y%m%d")

    return Base

#Reduccion del nombre de los productos
def Formato_Producto(Base):

    #Base.Producto[Base.Producto.isnull()] = ""
    Base.Producto = Base.Producto.str.lower()
    tmp = Base.Producto.str.split(" ", 20, expand=True).iloc[:,:6]
    tmp.fillna(value=" ", inplace=True)
    Producto_nueva = tmp.iloc[:,0] + " " + tmp.iloc[:,1] + " " +  tmp.iloc[:,2] + tmp.iloc[:,3] + " " + tmp.iloc[:,4] + " " +  tmp.iloc[:,5]

    return Producto_nueva

#Categorías fuentes medios
def Categoria(Base):
    #Adsocial
    Base.loc[Base['Fuente_categoria'].str.contains('adsocial'), 'Fuente_categoria'] = 'Adsocial'

    #Otros sitios
    Base.loc[Base['Fuente_categoria'].str.contains('referral'), 'Fuente_categoria'] = 'otros_sitios_web'

    #Organico
    Base.loc[( (Base['Fuente_categoria'].str.contains('organic')) |
               (Base['Fuente_categoria'].str.contains('bin')) |
               (Base['Fuente_categoria'].str.contains('google / cpc')) |
	       (Base['Fuente_categoria'].str.contains('google / search')) ), 'Fuente_categoria'] = 'organico'
		

    #Email
    Base.loc[Base['Fuente_categoria'].str.contains('email', case=False), 'Fuente_categoria'] = 'email'

    #Tiendeo
    Base.loc[Base['Fuente_categoria'].str.contains('tiendeo', case=False), 'Fuente_categoria'] = 'tiendeo'

    #direct
    Base.loc[Base['Fuente_categoria'].str.contains('direct', case=False), 'Fuente_categoria'] = 'direct'

    #Otros
    Base.loc[ (~(Base['Fuente_categoria'].str.contains('Adsocial')) &
               ~(Base['Fuente_categoria'].str.contains('otros_sitios')) &
               ~(Base['Fuente_categoria'].str.contains('organico')) &
               ~(Base['Fuente_categoria'].str.contains('email')) &
               ~(Base['Fuente_categoria'].str.contains('tiendeo')) & 
               ~(Base['Fuente_categoria'].str.contains('direct')) ) , 'Fuente_categoria'] = 'otros'
    
    return Base


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
