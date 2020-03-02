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

#Escritura_Sheets es un script de apoyo que contiene la función Escritura para el google sheets
from librerias import Escritura_Sheets

#Formato números
pd.set_option('display.float_format', lambda x: '%.10f' % x)

os.chdir('/home/carlos/Dropbox/ROAS 2020')
Archivos = os.listdir()

#################################################################
#Importación de las bases
#   -Ver el nombre de la campaña por rmnt o pi (caso especial)
#
#################################################################

#-- MP_FIC (KPI) --#

Arch_MP_FIC = [x for x in Archivos if "KPI" in x]
#MP Son unicos
MP = pd.read_excel(Arch_MP_FIC[0], sheet_name = 'KPIS MP 2020', skiprows = 2)
MP = MP.fillna('')
MP.loc[:,'NOMENCLATURA'] = MP.loc[:,'NOMENCLATURA'].str.lower()
MP['Archivo'] = Arch_MP_FIC[0] 

#Validaciones MP
#MP.shape[0] - MP[MP.Versión.str.contains('VC')].shape[0]

#Filtro sobre el MP 
#MP = MP[~MP['Versión'].str.contains('VC')]

#FIC
FIC = pd.read_excel(Arch_MP_FIC[0], sheet_name = 'KPIS FIC 2020', skiprows = 2)
FIC = FIC.fillna('')
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

MP = MP.loc[:, ('Archivo','NOMENCLATURA','llave_ventas','CLIENTE','MARCA','Mes','Versión','Plataforma','Plt','Formato','Inicio','Fin','TDC','Objetivo','Costo Planeado','KPI Planeado','Serving','Inversión Plataforma','Inversión Total')]
FIC = FIC.loc[:, ('Archivo','NOMENCLATURA','llave_ventas','CLIENTE','MARCA','Mes','Versión','Plataforma','Plt','Formato','Inicio','Fin','TDC','Objetivo','Inversión AdOps','Operativo AdOps', 'Serving AdOps','Costo Operativo')]

#Campañas unicas
MP = MP.groupby(['CLIENTE','MARCA','llave_ventas','Plt','Plataforma','Versión','Inicio','Fin','Mes'], as_index = False).agg(
                                                                               {'Costo Planeado':'mean',
                                                                               'KPI Planeado':'sum',
                                                                               'Serving':'sum',
                                                                               'Inversión Plataforma':'sum',
                                                                               'Inversión Total':'sum',
                                                                               'NOMENCLATURA':'count'})
MP['Plan'] = 'MP'
#Se tienen estos duplicados en el MP soló es necesario eliminarlos o ajustarlos, 
#Los duplicados pueden existir por el nombre de la campaña es distinto pero la nomeclatura es la misma
Duplicados_MP = MP[MP.NOMENCLATURA == 2]
#Campañas unicas
FIC = FIC.groupby(['CLIENTE','MARCA','llave_ventas','Plt','Plataforma','Versión','Inicio','Fin','Mes'], as_index = False).agg({'Inversión AdOps':'sum',
                                                                               'Operativo AdOps':'sum',
                                                                               'Serving AdOps':'sum',
                                                                               'Costo Operativo':'mean',
                                                                               'NOMENCLATURA':'count'})
FIC['Plan'] = 'FIC'
#Se tienen estos duplicados en el FIC soló es necesario eliminarlos o ajustarlos
Duplicados_FIC = FIC[FIC.NOMENCLATURA == 2]

#Importación google sheets
Escritura_Sheets.Escritura(Duplicados_MP, 0, header = True, Escribir = 'no')
Escritura_Sheets.Escritura(Duplicados_FIC, 1, header = True, Escribir = 'no')

#Cruze MP y FIC
#Primero lo que debe de cruzar
MP_FIC = pd.merge(MP, FIC, how = 'left', left_on = 'llave_ventas', right_on = 'llave_ventas')

#Analisis de lo que no debe cruzar
MP_FIC[MP_FIC.Plan_y.isnull() & MP_FIC.Versión_x.str.contains('VC')].Versión_x.value_counts()
Faltantes_FIC = MP_FIC[MP_FIC.Plan_y.isnull() & ~MP_FIC.Versión_x.str.contains('VC')]

Escritura_Sheets.Escritura(Faltantes_FIC, 3, header = True, Escribir = 'no') 

#Me quedo con lo que cruzo
MP_FIC = MP_FIC[~MP_FIC.Plan_y.isnull()]

#Base final MP_FIC
MP_FIC = pd.merge(MP, FIC, how = 'left', left_on = 'llave_ventas', right_on = 'llave_ventas')

MP_FIC.keys()

MP_FIC = MP_FIC.iloc[:, [0,1,2,3,4,5,6,7,8,9,10,11,12,13,15,24,25,26,27,28,29]]

MP_FIC.columns = ['cliente','marca','llave_ventas','plataforma_abreviacion','plataforma','versión','fecha_inicio_plan',
                  'fecha_fin_plan','mes_plan','costo_planeado','kpi_planeado','serving','inversión_plataforma','inversión_total'
                  ,'plan_x','inversión_AdOps','Operativo_AdOps','Serving_AdOps','costo_operativo','conteo_MP_FIC','plan_y']

Escritura_Sheets.Escritura(MP_FIC, 2, header = True, Escribir = 'no') 

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
import glob
Mes = 'Enero'

#Archivos_csv = glob.glob('/home/carlos/Dropbox/ROAS 2020/' + Mes + '/Semanal/**/*.csv')
#Archivos_xlsx = glob.glob('/home/carlos/Dropbox/ROAS 2020/' + Mes + '/Semanal/**/*.xlsx')

Archivos_csv = glob.glob('/home/carlos/Dropbox/ROAS 2020/' + Mes + '/Mensual/*.csv')
Archivos_xlsx = glob.glob('/home/carlos/Dropbox/ROAS 2020/' + Mes + '/Mensual/*.xlsx')

#FB_MP = MP_FIC[MP_FIC.plataforma_abreviacion.str.contains('FB')]

Arch_FB = [x for x in Archivos_csv if "FB" in x]

Facebook = []

for csv in Arch_FB:
    
    tmp = pd.read_csv(csv)
    tmp['Archivo'] = csv
    Facebook.append(tmp)
    
Facebook = pd.concat(Facebook)

#Revisiones rápidas
Facebook.Archivo.value_counts()
Facebook.keys()
#Columna de interés
Facebook = Facebook.loc[:,('Archivo','Nombre de la cuenta','Nombre de la campaña','Mes','Inicio','Finalización','Divisa','Importe gastado (MXN)','Impresiones','Clics en el enlace')]
Facebook['plataforma'] = 'Facebook'
Facebook = Facebook.reset_index()
#Con esta columna extraemos la fecha del reporte
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
Facebook = Facebook.loc[:,('Archivo','plataforma','Nombre de la cuenta','Nombre de la campaña','llave_plataformas','Mes','inicio_reporte','fin_reporte',
                           'Inicio','Finalización','Divisa','Importe gastado (MXN)','Impresiones','Clics en el enlace')]

Facebook.columns = ['archivo','plataforma','cuenta','nombre_campaña','llave_plataformas','mes','inicio_reporte','fin_reporte',
                    'fecha_inicio','fecha_fin','divisa','dinero_gastado','impresiones','clics']

    #Se eliminan las campañas provenientes de estás cuentas puede que no mache con el MP
Facebook = Facebook.loc[ ~( (Facebook.cuenta.str.contains('Adsocial'))  |  (Facebook.cuenta.str.contains('Dokkoi')) ) ]
Facebook.llave_plataformas = Facebook.llave_plataformas.str.lower()
Facebook.llave_plataformas = Facebook.llave_plataformas + str("_FB")

Facebook['conteo'] = 1
Facebook['divisa'] = 'mxn'


#Facebook_0 = Facebook.groupby(['archivo','cuenta','llave_plataformas','mes','inicio_reporte','fin_reporte','fecha_inicio','fecha_fin'], as_index = False).sum()
Facebook = Facebook.groupby(['plataforma','cuenta','llave_plataformas','mes','inicio_reporte','fin_reporte'], as_index = False).agg({
                                                                               'dinero_gastado':'sum',
                                                                               'impresiones':'sum',
                                                                               'clics':'sum',
                                                                               'conteo':'count'})
#Validación
#tmp_0 = Facebook[Facebook['llave_plataformas'].str.contains('ao-mkt')]
del Arch_FB, csv, tmp

#-- Adwords -- #
Arch_Adwords = [x for x in Archivos_csv if "Adwords" in x]

Adwords = []
fallas = []

for csv in Arch_Adwords:
    try:
        tmp = pd.read_csv(csv, sep = ',', skiprows = 2, encoding='utf-8')
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

Adwords = Adwords.rename(columns = {'Campa�a':'Campaña', 'Fecha de finalizaci�n':'Fecha de finalización'})

#ok
Adwords['Fecha de inicio'] =  pd.to_datetime(Adwords.loc[:,'Fecha de inicio'],errors='ignore',
                              format='%Y-%m-%d')
#ok
Adwords['Fecha de finalización'] =  pd.to_datetime(Adwords['Fecha de finalización'], errors = 'coerce',
                              format='%Y-%m-%d')
#ok
Adwords['inicio_reporte'] =  pd.to_datetime(Adwords['inicio_reporte'],
                              format='%d-%m-%Y')

#ok
Adwords['fin_reporte'] =  pd.to_datetime(Adwords['fin_reporte'],errors='coerce',
                              format='%d-%m-%Y')

Adwords.keys()

Adwords = Adwords.loc[:,('Archivo','Cuenta','Campaña','Mes','Fecha de inicio','Fecha de finalización','inicio_reporte','fin_reporte',
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

Adwords['plataforma'] = 'Adwords'
Adwords['conteo'] = 1

Adwords = Adwords.groupby(['plataforma','cuenta','llave_plataformas','mes','inicio_reporte','fin_reporte'], as_index = False).sum()

#-- Adform --#
Arch_Adform = [x for x in Archivos_xlsx if "Adform" in x]

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

Adform['conteo'] = 1

Adform = Adform.groupby(['plataforma','cuenta','llave_plataformas','mes','inicio_reporte','fin_reporte'], as_index = False).sum()

del Arch_Adform

#############################
#Unión de las Bases
# -Unión de todo
#
Facebook.shape[0] + Adwords.shape[0] + Adform.shape[0]

Plataformas = pd.concat([Facebook, Adwords,Adform])

#Semanal
#Escritura_Sheets.Escritura(Plataformas, 4, header = True, Escribir = 'no') 

#Mensual
#Escritura_Sheets.Escritura(Plataformas, 5, header = True, Escribir = 'si') 


tmp = Plataformas[Plataformas.llave_plataformas.str.contains('_SEM')] #Validación alguna plataforma

del fechas, Archivos, Arch_Adwords, tmp

####################################
#Separación del MP ó FIC Plataforma#
####################################
#Solo lo que tenemos en el MP
MP_PLT = pd.merge(MP_FIC, Plataformas, how = 'left', left_on = 'llave_ventas', right_on = 'llave_plataformas')
MP_PLT = MP_PLT.sort_values(['cliente','marca','llave_ventas','fecha_inicio_plan','plataforma_y'])

#Semanal
#Escritura_Sheets.Escritura(MP_PLT, 6, header = True, Escribir = 'si') 

#Mensual
Escritura_Sheets.Escritura(MP_PLT, 8, header = True, Escribir = 'si')

#Información que no cruzo
NO_CRUZO = MP_PLT[MP_PLT.plataforma_y.isnull()]
NO_CRUZO = NO_CRUZO.sort_values(['llave_ventas'])

Escritura_Sheets.Escritura(NO_CRUZO, 9, header = True, Escribir = 'si')

#MP_PLT.plataforma.value_counts()

#MP_PLT = MP_PLT.fillna(0)

#Validaciones
tmp_f = Facebook[Facebook.llave_plataformas.str.contains('FB')]
a = tmp_f.llave_plataformas.value_counts()

tmp_mp = MP_PLT[MP_PLT.llave_plataformas.str.contains('FB', na = False)]
b = tmp_mp.llave_plataformas.value_counts()


A = MP_PLT[MP_PLT.llave_ventas == '2001_petco_hills_ppf_pfm_FB']
B = MP_PLT[MP_PLT.llave_ventas == '2001_gicsa_explanadapachuca_pi_mkt_FB']
