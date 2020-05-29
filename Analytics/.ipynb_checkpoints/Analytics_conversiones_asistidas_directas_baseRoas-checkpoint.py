#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 11:30:53 2019

@author: carlos

Union de las conversiones asistidas y directas de los reportes semanales para cruzar con la base master roas

"""
import pandas as pd
import glob
import re
import datetime

###########
#Analytics#
###########
#Aquí descargo el nuevo archivo de KPIS
def archivos_plataformas(mes = 'Enero', tipo_union = 'Mensual'):
    if tipo_union == 'Semanal':
        Archivos_csv = glob.glob('/home/carlos/Dropbox/ROAS 2020/' + mes + '/Semanal/**/*.csv')
        Archivos_xlsx = glob.glob('/home/carlos/Dropbox/ROAS 2020/' + mes + '/Semanal/**/*.xlsx')
    else:
        Archivos_csv = glob.glob('/home/carlos/Dropbox/ROAS 2020/' + mes + '/Mensual/*.csv')
        Archivos_xlsx = glob.glob('/home/carlos/Dropbox/ROAS 2020/' + mes + '/Mensual/*.xlsx')
    return Archivos_csv, Archivos_xlsx

#Funcion que arroja conversiones asistidas y trafico al sitio
def Analytics(mes = '2001_Enero'):
    
    csv, xlsx = archivos_plataformas(mes = mes)

    analytics_asistidas = [x for x in csv if "Analytics" in x]

    union_conversiones = []
    
    #Trabaja solo los archivos de conversiones
    for csv in analytics_asistidas:
        try:
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
        except:
            #En ocasiones por el formato no leía el archivo utf-
            print("No tiene datos el archivo:", csv)
            
    union_conversiones = pd.concat(union_conversiones)
    
    union_conversiones['cliente'] = ''
    union_conversiones['Año.Mes'] = mes
    union_conversiones['plataforma_abreviacion'] = ''
    union_conversiones['Tipo'] = 'Asistida'
    union_conversiones['llave_analytics'] = ''
    
    list(enumerate(union_conversiones.keys()))
    
    union_conversiones = union_conversiones.loc[:,['cliente','Año.Mes','plataforma_abreviacion','inicio_reporte','fin_reporte','Tipo','Fuente/Medio','Campaña','llave_analytics','Conversiones asistidas','Valor de las conversiones asistidas','archivo']]
    union_conversiones.columns = ['cliente', 'Año-Mes', 'plataforma_abreviacion',	'inicio_reporte', 'fin_reporte', 'tipo_conversion',	'fuente_medio',	'Nombre_Campaña', 'llave_analytcis', 'conversiones', 'revenue',	'archivo']
    
    union_conversiones.fuente_medio = union_conversiones.fuente_medio.str.lower()
    
    union_conversiones.loc[ (union_conversiones.fuente_medio.str.contains('od')) | (union_conversiones.archivo.str.contains('officedepot')) , 'cliente' ] = 'Office Depot'
    union_conversiones.loc[ (union_conversiones.fuente_medio.str.contains('rs')) | (union_conversiones.archivo.str.contains('radioshack')), 'cliente' ] = 'RadioShack'
    union_conversiones.loc[ (union_conversiones.fuente_medio.str.contains('pet')) | (union_conversiones.archivo.str.contains('All Web Site Data Todo el tráfico')), 'cliente' ] = 'Petco'
    union_conversiones.loc[ (union_conversiones.fuente_medio.str.contains('ths')) | (union_conversiones.archivo.str.contains('thehomestore')), 'cliente' ] = 'The Home Store'
    union_conversiones.loc[ union_conversiones.fuente_medio.str.contains('push'), 'cliente' ] = 'PV_AdsMovil'
    union_conversiones.loc[ union_conversiones.fuente_medio.str.contains('gdn') , 'cliente' ] = 'gdn'
    
    union_conversiones.loc[ (union_conversiones.fuente_medio.str.contains('_fb')) | 
                             (union_conversiones.fuente_medio.str.contains('_ig')) |
                             (union_conversiones.fuente_medio.str.contains('adsocialfb')), 'plataforma_abreviacion'] = 'FB'
    union_conversiones.loc[ union_conversiones.fuente_medio.str.contains('_sem'), 'plataforma_abreviacion' ] = 'SEM'
    union_conversiones.loc[ union_conversiones.fuente_medio.str.contains('_dsp'), 'plataforma_abreviacion' ] = 'DSP'
    
    union_conversiones.conversiones = union_conversiones.conversiones.astype('int')
    
    union_conversiones.revenue = union_conversiones.revenue.apply(lambda x : str(x).replace('.',''))
    union_conversiones.revenue = union_conversiones.revenue.apply(lambda x : str(x).replace(',','.'))
    union_conversiones.revenue = union_conversiones.revenue.apply(lambda x : str(x).replace('MXN','')).astype('float')
    
    #Conversiones todo el trafico
    analytics_trafico = [x for x in xlsx if "Analytics" in x]
    
    union_trafico = []
    
    #Trabaja los archivos de trafico al sitio
    for xls in analytics_trafico:
        try:
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
        except:
            #En ocasiones por el formato no leía el archivo utf-
            print("No tiene datos el archivo:", xls)
        
    union_trafico = pd.concat(union_trafico)
    
    union_trafico['cliente'] = ''
    union_trafico['Año.Mes'] = mes
    union_trafico['plataforma_abreviacion'] = ''
    union_trafico['Tipo'] = 'Directa'
    union_trafico['llave_analytics'] = ''
    
    list(enumerate(union_trafico.keys()))
    
    union_trafico = union_trafico.loc[:,['cliente', 'Año.Mes', 'plataforma_abreviacion', 'inicio_reporte', 'fin_reporte', 'Tipo', 'Fuente/Medio', 'Campaña', 'llave_analytcis', 'Transacciones', 'Ingresos', 'archivo']]
    union_trafico.columns = ['cliente', 'Año-Mes', 'plataforma_abreviacion','inicio_reporte', 'fin_reporte', 'tipo_conversion',	'fuente_medio',	'Nombre_Campaña', 'llave_analytcis', 'conversiones', 'revenue',	'archivo']
    
    union_trafico.fuente_medio = union_trafico.fuente_medio.str.lower()
    
    union_trafico.loc[ (union_trafico.fuente_medio.str.contains('od')) | (union_trafico.archivo.str.contains('officedepot')) , 'cliente' ] = 'Office Depot'
    union_trafico.loc[ (union_trafico.fuente_medio.str.contains('rs')) | (union_trafico.archivo.str.contains('radioshack')), 'cliente' ] = 'RadioShack'
    union_trafico.loc[ (union_trafico.fuente_medio.str.contains('pet')) | (union_trafico.archivo.str.contains('All Web Site Data Todo el tráfico')), 'cliente' ] = 'Petco'
    union_trafico.loc[ (union_trafico.fuente_medio.str.contains('ths')) | (union_trafico.archivo.str.contains('thehomestore')), 'cliente' ] = 'The Home Store'
    union_trafico.loc[ union_trafico.fuente_medio.str.contains('push'), 'cliente' ] = 'PV_AdsMovil'
    union_trafico.loc[ union_trafico.fuente_medio.str.contains('gdn') , 'cliente' ] = 'gdn'
    

    union_trafico.loc[ (union_trafico.fuente_medio.str.contains('_fb')) | 
                       (union_trafico.fuente_medio.str.contains('_ig')) |
                       (union_trafico.fuente_medio.str.contains('adsocialfb')), 'plataforma_abreviacion'] = 'FB'
    union_trafico.loc[ union_trafico.fuente_medio.str.contains('_sem'), 'plataforma_abreviacion' ] = 'SEM'
    union_trafico.loc[ union_trafico.fuente_medio.str.contains('_dsp'), 'plataforma_abreviacion' ] = 'DSP'    
    
    union_trafico.conversiones = union_trafico.conversiones.astype('int')
        
        #Union de los 2 tmp
    union_analytics = pd.concat([union_conversiones,union_trafico])
    
    return union_analytics

analytics = pd.concat( [Analytics(mes = '2001_Enero'), 
                       Analytics(mes = '2002_Febrero'), 
                       Analytics(mes = '2003_Marzo') ] )

analytics = analytics[(analytics.conversiones != 0) & (analytics.revenue != 0)]

analytics = analytics.fillna('')

analytics.inicio_reporte = pd.to_datetime(analytics.inicio_reporte, format = "%Y-%m-%d")
analytics.fin_reporte = pd.to_datetime(analytics.fin_reporte, format = "%Y-%m-%d")

tmp = analytics.groupby(['cliente','Año-Mes','plataforma_abreviacion','inicio_reporte','fin_reporte','tipo_conversion','fuente_medio','Nombre_Campaña','archivo'],
                              as_index = False).count()

tmp_0 = tmp[tmp.Nombre_Campaña == '']
a = pd.DataFrame(tmp_0.archivo.unique())


analytics.to_csv("/home/carlos/Documentos/3_Adsocial/Marketing/Analytics/analytics_union.csv")

#########################################
#Escritura de los datos en Google Sheets#
#########################################
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe #,get_as_dataframe
from datetime import datetime

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
    
        sh = client.open('Base master Roas') #Recordar que el archivo que deseamos leer tiene que tener el correo de la api como persona compartida
        worksheet = sh.get_worksheet(hoja) #Base_master_python
        #sh.worksheets()
        
        filas = len(worksheet.get_all_values()) + 1
        set_with_dataframe(worksheet, Base, row = filas, include_column_header = header)

    else: 
        print("Ok!, No escribimos nada")    

Escritura(analytics, 2,header = True , Escribir = 'si')



