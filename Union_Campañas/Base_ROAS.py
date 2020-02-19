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

#Formato números
pd.set_option('display.float_format', lambda x: '%.5f' % x)

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

Facebook.columns = ('archivo','cuenta','campaña','mes','fecha_inicio','fecha_finalización','divisa','dinero_gastado','impresiones','clics')
Facebook['plataforma'] = 'Facebook'

#-- Adwords -- #
Arch_Adwords = [x for x in Archivos if "Adwords" in x]

Adwords = []
fallas = []

for csv in Arch_Adwords:
    try:
        tmp = pd.read_csv(csv, sep = ',', skiprows = 2)
        tmp['Archivo'] = csv
        Adwords.append(tmp)
    except:
        #En ocasiones por el formato no leía el archivo utf-
        fallas.append(csv)
    print("En ocasiones se guardan como UTF-16 excell ocasionando estas fallas : ",fallas)

Adwords = pd.concat(Adwords).reset_index(drop = True)

Adwords = Adwords.loc[:,('Archivo','Cuenta','Campaña','Mes','Fecha de inicio','Fecha de finalización',
                           'Moneda','Costo','Impresiones','Clics')]

Adwords.columns = ('archivo','cuenta','campaña','mes','fecha_inicio','fecha_finalización','divisa','dinero_gastado','impresiones','clics')
Adwords['plataforma'] = 'Adwords'

#-- Adform --#
Arch_Adform = [x for x in Archivos if "Adform" in x]

Adform = pd.read_excel(Arch_Adform[0], sheet_name = 'Sheet', skiprows = 2)
Adform['Archivo'] = Arch_Adform[0] 

Adform = Adform.iloc[:-1,].loc[:, ('Archivo','Client','Campaign','Campaign Start Date','Campaign End Date',
                                               'Sales (All)','Tracked Ads','Clicks')]

Adform.columns = ('archivo','cuenta','campaña','fecha_inicio','fecha_finalización','dinero_gastado','impresiones','clics')

Adform['plataforma'] = 'Adform'
Adform['divisa'] = 'MXN'
Adform['mes'] = ''

Adform = Adform.loc[:,('archivo','cuenta','campaña','mes','fecha_inicio','fecha_finalización','divisa','dinero_gastado','impresiones','clics','plataforma')]

#############################
#Unión de las Bases
# -Unión de todo
#
####
Base_ROAS = pd.concat([Facebook, Adwords, Adform], axis = 0)

Base_ROAS.plataforma.value_counts()

######################
#Exportación a Sheets#
######################
#Colocar la base completa en sheets
#   - Validar que no se puede colocar un archivo repetido
#   - 

