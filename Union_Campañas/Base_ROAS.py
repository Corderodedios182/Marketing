#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 12:13:57 2020

El siguiente script creará la Base de los ROAS

Los Archivos se encuentran en: /home/carlos/Dropbox/ROAS 2020 (Cada mes se crea la base del Mes y se colocan los reportes de las Plataformas)

- Facebook: FB-AdSocial-Jan-1-2020-Jan-31-2020

- Adwords:  Adwords 1-01-2020 al 31-01-2020-2

- Adform: 

- MP_FIC: KPIS 2020 - AdSocial

@author: carlos
"""
#Paqueterías
import os
import pandas as pd
import datetime
import re
#Formato números
pd.set_option('display.float_format', lambda x: '%.10f' % x)

#Rutas
#Ruta = input("Coloca la ruta donde se encuentran tus archivos: ") #Ejemplo: /home/carlos/Dropbox/ROAS 2020
os.chdir('/home/carlos/Dropbox/ROAS 2020')
#Mes = input("¿Qué mes deseas actualizar? " + str(os.listdir( )) + " : " )
os.chdir('Enero')
Archivos = os.listdir()

#############################
#Importación de las bases
#   -Estandarización
#   -Reglas de Fechas
#   -Columnas a ocupar
#   -Ver el nombre de la campaña por rmnt o pi (caso especial)
#
############################

#-- MP_FIC (KPI) --#

Arch_MP_FIC = [x for x in Archivos if "KPI" in x]
#MP
MP = pd.read_excel(Arch_MP_FIC[0], sheet_name = 'KPIS MP 2020', skiprows = 2)
MP.loc[:,'NOMENCLATURA'] = MP.loc[:,'NOMENCLATURA'].str.lower()
MP['Archivo'] = Arch_MP_FIC[0] 


#FIC
FIC = pd.read_excel(Arch_MP_FIC[0], sheet_name = 'KPIS FIC 2020', skiprows = 2)
FIC.loc[:,'NOMENCLATURA'] = FIC.loc[:,'NOMENCLATURA'].str.lower()
FIC['Archivo'] = Arch_MP_FIC[0] 

def Formato_Fechas(Base, Columna):
    Base.loc[:,Columna] = pd.to_datetime(Base.loc[:,Columna], errors = 'ignore', format = '%d/%m/%y')
    return Base.loc[:,Columna]

def Formato_numerico(Base, Columna):
    Base.loc[:,Columna] = Base.loc[:,Columna].apply(lambda x : str(x).replace('$',''))
    Base.loc[:,Columna] = Base.loc[:,Columna].apply(lambda x : str(x).replace(',',''))
    Base.loc[:,Columna] = Base.loc[:,Columna].apply(lambda x : str(x).strip())
    Base.loc[:,Columna] = Base.loc[:,Columna].apply(lambda x : str(x).replace('-','0'))
    Base.loc[:,Columna] = Base.loc[:,Columna].astype('float')
    Base.loc[:,Columna] = round(Base.loc[:,Columna],2)
    return Base.loc[:,Columna]
#Limpieza fechas
MP.loc[:,'Inicio'] = Formato_Fechas(MP, 'Inicio')
MP.loc[:,'Fin'] = Formato_Fechas(MP, 'Fin')

FIC.loc[:,'Inicio'] = Formato_Fechas(FIC, 'Inicio')
FIC.loc[:,'Fin'] = Formato_Fechas(FIC, 'Fin')
#Limpieza columnas numericas
MP.loc[:,'Costo Planeado'] = Formato_numerico(MP, 'Costo Planeado')
MP.loc[:,'KPI Planeado'] = Formato_numerico(MP, 'KPI Planeado')
MP.loc[:,'Serving'] = Formato_numerico(MP, 'Serving')
MP.loc[:,'Inversión Plataforma'] = Formato_numerico(MP, 'Inversión Plataforma')
MP.loc[:,'Inversión Total'] = Formato_numerico(MP, 'Inversión Total')

FIC.loc[:,'Inversión AdOps'] = Formato_numerico(FIC, 'Inversión AdOps')
FIC.loc[:,'Operativo AdOps'] = Formato_numerico(FIC, 'Operativo AdOps')
FIC.loc[:,'Serving AdOps'] = Formato_numerico(FIC, 'Serving AdOps')
FIC.loc[:,'Costo Operativo'] = Formato_numerico(FIC, 'Costo Operativo')

#Para poder trabajar mejor con la nomeclatura, le agregamos su plataforma para cruzar con la información de plataformas
MP['Plt'] = MP.loc[:,'Plataforma']

MP.loc[MP['Plataforma'].str.contains('Instagram') , 'Plt'] = 'IG'
MP.loc[MP['Plataforma'].str.contains('Facebook') , 'Plt'] = 'FB'
MP.loc[MP['Plataforma'].str.contains('Google') , 'Plt'] = 'SEM'
MP.loc[(MP['Plataforma'].str.contains('Programmatic')) | (MP['Plataforma'].str.contains('Display'))  , 'Plt'] = 'DSP'
MP.loc[(MP['Plataforma'].str.contains('Waze')) | (MP['Plataforma'].str.contains('AdsMovil')) , 'Plt'] = 'PV'

FIC.loc[FIC['Plataforma'].str.contains('Instagram') , 'Plt'] = 'IG'
FIC.loc[FIC['Plataforma'].str.contains('Facebook') , 'Plt'] = 'FB'
FIC.loc[FIC['Plataforma'].str.contains('Google') , 'Plt'] = 'SEM'
FIC.loc[(FIC['Plataforma'].str.contains('Programmatic')) | (FIC['Plataforma'].str.contains('Display'))  , 'Plt'] = 'DSP'
FIC.loc[(FIC['Plataforma'].str.contains('Waze')) | (FIC['Plataforma'].str.contains('AdsMovil')) , 'Plt'] = 'PV'

MP['llave_ventas'] = MP.loc[:,'NOMENCLATURA'] + str("_") + MP['Plt']
MP["llave_ventas"].str.strip()

FIC['llave_ventas'] = FIC.loc[:,'NOMENCLATURA'] + str("_") + FIC['Plt']
FIC["llave_ventas"].str.strip()

MP = MP.loc[:, ('Archivo','NOMENCLATURA','llave_ventas','CAMPAÑA','CLIENTE','MARCA','Mes','Versión','Plataforma','Plt','Formato','Inicio','Fin','TDC','Objetivo','Costo Planeado','KPI Planeado','Serving','Inversión Plataforma','Inversión Total')]
FIC = FIC.loc[:, ('Archivo','NOMENCLATURA','llave_ventas','CAMPAÑA','CLIENTE','MARCA','Mes','Versión','Plataforma','Plt','Formato','Inicio','Fin','TDC','Objetivo','Inversión AdOps','Operativo AdOps', 'Serving AdOps','Costo Operativo')]

#Filtro sobre el MP
MP = MP[~MP['Versión'].str.contains('VC')]

#Campañas unicas
MP = MP.groupby(['llave_ventas','Plt','Inicio','Fin'], as_index = False).agg({'Costo Planeado':'mean',
                                                                               'KPI Planeado':'sum',
                                                                               'Serving':'sum',
                                                                               'Inversión Plataforma':'sum',
                                                                               'Inversión Total':'sum',
                                                                               'NOMENCLATURA':'count'})

MP.groupby(['Plt']).count()['llave_ventas'].reset_index()

FIC = FIC.groupby(['llave_ventas','Plt','Inicio','Fin'], as_index = False).agg({'Inversión AdOps':'sum',
                                                                               'Operativo AdOps':'sum',
                                                                               'Serving AdOps':'sum',
                                                                               'Costo Operativo':'sum',
                                                                               'NOMENCLATURA':'count'})
FIC.groupby(['Plt']).count()['llave_ventas'].reset_index()

del Arch_MP_FIC
#############################
#Importación de las bases
#   -Limpieza de las bases, formatos, fechas, agrupaciones
#   -Estandarización
#   -Reglas de Fechas
#   -Columnas a ocupar
#   -Ver el nombre de la campaña por rmnt o pi (caso especial)
#
############################

#-- Facebook -- #
Arch_FB = [x for x in Archivos if "FB" in x]

Facebook = []

for csv in Arch_FB:
    
    tmp = pd.read_csv(csv)
    tmp['Archivo'] = csv
    Facebook.append(tmp)
    
Facebook = pd.concat(Facebook)

Facebook = Facebook.loc[:,('Archivo','Nombre de la cuenta','Nombre de la campaña','Mes','Inicio','Finalización','Divisa','Importe gastado (MXN)','Impresiones','Clics en el enlace')]
Facebook['plataforma'] = 'Facebook'
Facebook.Mes
    
    #Fechas 
def Formato_Fechas(Base, Columna):

    fechas = Base[Columna].astype(str).str.split(" - ",expand = True)
    fechas = pd.DataFrame(fechas)
    fechas.columns = ['inicio_reporte','fin_reporte']
     
    Base['inicio_reporte'] = fechas.iloc[:,0]
    Base['fin_reporte'] = fechas.iloc[:,1]
       
    Base.inicio_reporte = Base.inicio_reporte.apply(lambda x: str(x).replace("['",""))
    Base.fin_reporte = Base.fin_reporte.apply(lambda x: str(x).replace("']",""))
    
    Base.inicio_reporte = pd.to_datetime(Base.inicio_reporte,format = "%Y-%m-%d")
    Base.fin_reporte = pd.to_datetime(Base.fin_reporte,format = "%Y-%m-%d")

    return Base

Facebook = Formato_Fechas(Facebook, 'Mes')

Facebook.dtypes
Facebook['Mes'] = Facebook.inicio_reporte.apply(lambda x : x.month)

    #Extracción del nombre para cruzarlo con ventas
C_Facebook = Facebook.loc[:,'Nombre de la campaña'].str.split("_",10,expand = True).iloc[:,:5] ; cols = ["Año-Mes","Cliente","Marca","Tipo-1","Tipo-2"]
C_Facebook.columns = cols
C_Facebook = C_Facebook[cols].apply(lambda row: '_'.join(row.values.astype(str)), axis=1) ; del cols

Facebook['llave_plataformas'] = C_Facebook ; del C_Facebook
Facebook['llave_plataformas'] = Facebook['llave_plataformas'].str.strip()

    #Columnas de interés
Facebook.keys()
Facebook = Facebook.loc[:,('Archivo','Nombre de la cuenta','Nombre de la campaña','llave_plataformas','Mes','inicio_reporte','fin_reporte',
                           'Inicio','Finalización','Divisa','Importe gastado (MXN)','Impresiones','Clics en el enlace')]

Facebook.columns = ['archivo','cuenta','nombre_campaña','llave_plataformas','mes','inicio_reporte','fin_reporte',
                    'fecha_inicio','fecha_fin','divisa','dinero_gastado','impresiones','clics']

    #Se eliminan las campañas provenientes de estás cuentas puede que no mache con el MP
Facebook = Facebook.loc[ ~( (Facebook.cuenta.str.contains('Adsocial'))  |  (Facebook.cuenta.str.contains('Dokkoi')) ) ]
Facebook.llave_plataformas = Facebook.llave_plataformas.str.lower()
Facebook.llave_plataformas = Facebook.llave_plataformas + str("_FB")

#tmp_0 = Facebook[Facebook['llave_facebook'] == '2001_gicsa_explanadapuebla_pi_mkt_FB']
#Facebook_0 = Facebook.groupby(['archivo','cuenta','llave_plataformas','mes','inicio_reporte','fin_reporte','fecha_inicio','fecha_fin'], as_index = False).sum()
Facebook = Facebook.groupby(['archivo','cuenta','llave_plataformas','mes','inicio_reporte','fin_reporte'], as_index = False).sum()

del Arch_FB, csv, tmp

#-- Adwords -- #
Arch_Adwords = [x for x in Archivos if "Adwords" in x]

Adwords = []
fallas = []

for csv in Arch_Adwords:
    try:
        tmp = pd.read_csv(csv, sep = ',', skiprows = 2)
        tmp['Archivo'] = csv
        #Extreamos las fechas del nombre del reporte
        Fechas = list(tmp.Archivo.unique())
        #####Se extrae la fecha de la columna Archivo, para crear Fecha_inicio_reporte y Fecha_fin_reporte
        tmp['Archivo_fechas'] = tmp['Archivo']

        tmp['fecha_reporte'] = [re.findall(r"\d{1}-\d{1}-\d{4}|\d{2}-\d{1}-\d{4}|\d{1}-\d{2}-\d{4}|\d{2}-\d{2}-\d{4}", i) 
                                    for i in list(tmp.Archivo_fechas)]

        fechas = [re.findall(r"\d{1}-\d{1}-\d{4}|\d{2}-\d{1}-\d{4}|\d{1}-\d{2}-\d{4}|\d{2}-\d{2}-\d{4}", i) for i in list(tmp.Archivo_fechas)]

        fechas = pd.DataFrame(fechas)
        fechas.columns = ['inicio_reporte','fin_reporte']
        
        tmp = pd.concat([tmp.reset_index(drop = True), pd.DataFrame(fechas)], axis = 1)
        
        Adwords.append(tmp)
    except:
        #En ocasiones por el formato no leía el archivo utf-
        fallas.append(csv)
        print("En ocasiones se guardan como UTF-16 excell ocasionando estas fallas : ",fallas)

Adwords = pd.concat(Adwords).reset_index(drop = True)

del Fechas, csv, fallas, fechas, tmp
    #Formato correcto para trabajar con las fechas

#ok
Adwords['Fecha de inicio'] =  pd.to_datetime(Adwords.loc[:,'Fecha de inicio'],errors='ignore',
                              format='%Y-%m-%d')
#ok
Adwords['Fecha de finalizaci�n'] =  pd.to_datetime(Adwords['Fecha de finalizaci�n'], errors = 'coerce',
                              format='%Y-%m-%d')
#ok
Adwords['inicio_reporte'] =  pd.to_datetime(Adwords['inicio_reporte'],
                              format='%d-%m-%Y')

#ok
Adwords['fin_reporte'] =  pd.to_datetime(Adwords['fin_reporte'],errors='coerce',
                              format='%d-%m-%Y')

Adwords.keys()

Adwords = Adwords.loc[:,('Archivo','Cuenta','Campa�a','Mes','Fecha de inicio','Fecha de finalizaci�n','inicio_reporte','fin_reporte',
                           'Moneda','Costo','Impresiones','Clics')]

Adwords.columns = ('archivo','cuenta','campaña','mes','fecha_inicio','fecha_finalización','inicio_reporte','fin_reporte','divisa','dinero_gastado','impresiones','clics')
Adwords['plataforma'] = 'Adwords'

Adwords['mes'] = Adwords.inicio_reporte.apply(lambda x : x.month)

    #Extracción del nombre para cruzar con ventas

C_Adwords = Adwords.loc[:,'campaña'].str.split("_",10,expand = True).iloc[:,:5] ; cols = ["Año-Mes","Cliente","Marca","Tipo-1","Tipo-2"]
C_Adwords.columns = cols
C_Adwords = C_Adwords[cols].apply(lambda row: '_'.join(row.values.astype(str)), axis=1) ; del cols

Adwords['llave_plataformas'] = C_Adwords ; del C_Adwords
Adwords['llave_plataformas'] = Adwords['llave_plataformas'].str.lower()
Adwords['llave_plataformas'] = Adwords['llave_plataformas'] + str("_SEM")

    #Formato numerico
Adwords.clics = Adwords.clics.apply(lambda x : str(x).replace(',','')).astype('int')
Adwords.impresiones = Adwords.impresiones.apply(lambda x: str(x).replace(',','')).astype('int')
Adwords.dinero_gastado = Adwords.dinero_gastado.apply(lambda x: str(x).replace(',','')).astype('float')

Adwords = Adwords.groupby(['archivo','cuenta','llave_plataformas','mes','inicio_reporte','fin_reporte'], as_index = False).sum()

#-- Adform --#
Arch_Adform = [x for x in Archivos if "Adform" in x]

Adform = pd.read_excel(Arch_Adform[0], sheet_name = 'Sheet', skiprows = 2)
Adform['Archivo'] = Arch_Adform[0] 

Adform['Archivo_fechas'] = Adform['Archivo']

Adform['fecha_reporte'] = [re.findall(r"\d{1}-\d{1}-\d{4}|\d{2}-\d{1}-\d{4}|\d{1}-\d{2}-\d{4}|\d{2}-\d{2}-\d{4}", i) 
                                    for i in list(Adform.Archivo_fechas)]

fechas = [re.findall(r"\d{1}-\d{1}-\d{4}|\d{2}-\d{1}-\d{4}|\d{1}-\d{2}-\d{4}|\d{2}-\d{2}-\d{4}", i) for i in list(Adform.Archivo_fechas)]
fechas = pd.DataFrame(fechas)
fechas.columns = ['inicio_reporte','fin_reporte']
        
Adform = pd.concat([Adform.reset_index(drop = True), pd.DataFrame(fechas)], axis = 1)

Adform = Adform.iloc[:-1,].loc[:, ('Archivo','Client','Campaign','Month','Campaign Start Date','Campaign End Date','inicio_reporte',
                                   'fin_reporte','Sales (All)','Tracked Ads','Clicks')]

Adform.columns = ('archivo','cuenta','campaña','mes','fecha_inicio','fecha_finalización','inicio_reporte','fin_reporte','dinero_gastado',
                  'impresiones','clics')

Adform['plataforma'] = 'Adform'
Adform['divisa'] = 'MXN'

Adform = Adform.loc[:,('archivo','cuenta','campaña','mes','fecha_inicio','fecha_finalización','inicio_reporte','fin_reporte','divisa',
                       'dinero_gastado','impresiones','clics','plataforma')]

    #Fechas 
Adform.fecha_inicio = pd.to_datetime(Adform.fecha_inicio, format = "%Y-%m-%d")
Adform.fecha_finalización = pd.to_datetime(Adform.fecha_finalización,format = "%Y-%m-%d")

Adform.inicio_reporte = pd.to_datetime(Adform.inicio_reporte, format = '%d-%m-%Y')
Adform.fin_reporte = pd.to_datetime(Adform.fin_reporte,format = '%d-%m-%Y')

Adform['mes'] = Adform.inicio_reporte.apply(lambda x : x.month)

    #Extracción del nombre para cruzarlo con ventas
C_Adform = Adform.loc[:,'campaña'].str.split("_",10,expand = True).iloc[:,:5] ; cols = ["Año-Mes","Cliente","Marca","Tipo-1","Tipo-2"]
C_Adform.columns = cols
C_Adform = C_Adform[cols].apply(lambda row: '_'.join(row.values.astype(str)), axis=1) ; del cols

Adform['llave_plataformas'] = C_Adform ; del C_Adform
Adform['llave_plataformas'] = Adform['llave_plataformas'].str.strip()

    #Se eliminan las campañas provenientes de estás cuentas puede que no mache con el MP
#Facebook = Facebook.loc[ ~( (Facebook.Nombre_Cuenta.str.contains('Adsocial'))  |  (Facebook.Nombre_Cuenta.str.contains('Dokkoi')) ) ]
Adform.llave_plataformas = Adform.llave_plataformas.str.lower()
Adform.llave_plataformas = Adform.llave_plataformas + str("_DSP")

    #Formato numerico
Adform.clics = Adform.clics.apply(lambda x : str(x).replace(',','')).astype('int')
Adform.impresiones = Adform.impresiones.apply(lambda x: str(x).replace(',','')).astype('int')
Adform.dinero_gastado = Adform.dinero_gastado.apply(lambda x: str(x).replace(',','')).astype('float')

Adform = Adform.groupby(['archivo','cuenta','llave_plataformas','mes','inicio_reporte','fin_reporte'], as_index = False).sum()

del Arch_Adform

#############################
#Unión de las Bases
# -Unión de todo
#
Facebook.keys() 
Adwords.keys()
Adform.keys()

Plataformas = pd.concat([Facebook, Adwords, Adform])

tmp = Plataformas[Plataformas.llave_plataformas.str.contains('_SEM')] #Validación

del fechas, Archivos, Arch_Adwords, tmp

####################################
#Separación del MP ó FIC Plataforma#
####################################
#MP
MP_PLT = pd.merge(MP, Plataformas, how = 'left', left_on = 'llave_ventas', right_on = 'llave_plataformas')

#########################################
#Escritura de los datos en Google Sheets#
#########################################
import os
import gspread
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe #,get_as_dataframe

Base_master_final = MP_PLT

Escribir = input("Deseas escribir los datos en sheets si/no : ")

if Escribir == 'si':
    os.chdir('/home/carlos/Documentos/3_Adsocial')
    os.listdir()
    #Autentificacion con google cloud platform correo analytics.adsocial@gmail.com
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)

    Base_master_final['ultima_actualizacion'] = datetime.now()
    
    sh = client.open('Validación Nomeclatura Adsocial') #Recordar que el archivo que deseamos leer tiene que tener el correo de la api como persona compartida
    worksheet = sh.get_worksheet(8) #Base_master_python

    filas = len(worksheet.get_all_values()) + 1
    set_with_dataframe(worksheet, Base_master_final, row = filas, include_column_header = True)

else: 
    print("Ok!")    

