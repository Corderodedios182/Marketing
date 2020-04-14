#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 13:51:42 2020

@author: carlos
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
    tmp = Base.Producto.str.split(" ", 20, expand=True).iloc[:,:3]
    tmp.fillna(value=" ", inplace=True)
    Producto_nueva = tmp.iloc[:,0] + " " + tmp.iloc[:,1] + " " +  tmp.iloc[:,2]

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

