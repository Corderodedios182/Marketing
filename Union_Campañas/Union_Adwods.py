#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 11:08:40 2020

@author: carlos
"""

import os
import pandas as pd
#import datetime

os.chdir("/home/carlos/Documentos/Adsocial/Bases AdSocial/2020")
os.listdir()

Adwords = pd.read_csv('Adwords 1-01-2020 al 22-01-2019.csv', skiprows = 2)

#Formato de Columnas

    #Fechas

Adwords['Fecha de inicio'] = pd.to_datetime(Adwords['Fecha de inicio'], format='%Y-%m-%d')
Adwords['Fecha de finalización'] = pd.to_datetime(Adwords['Fecha de finalización'], format='%Y-%m-%d', errors = 'coerce')

#Extracción del nombre para cruzar con ventas

C_Adwords = Adwords.loc[:,'Campaña'].str.split("_",10,expand = True).iloc[:,:5] ; cols = ["Año-Mes","Cliente","Marca","Tipo-1","Tipo-2"]
C_Adwords.columns = cols
C_Adwords = C_Adwords[cols].apply(lambda row: '_'.join(row.values.astype(str)), axis=1) ; del cols

Adwords['Llave'] = C_Adwords ; del C_Adwords

#Columnas de interés
Adwords = Adwords.loc[:,('Cuenta', 'Campaña', 'Llave', 'Fecha de inicio', 'Fecha de finalización', 'Moneda','Costo', 'Impresiones', 'Clics')]
Adwords.dtypes

tmp = Adwords.groupby(['Llave'], as_index = False).count()
Adwords['Llave'] = Adwords['Llave'].str.lower()
#Adwords_tmp = Adwords.groupby(['Llave'], as_index = False).sum()

########################
#Archivo de Ventas 2020#
########################
#Ventas_Operativo = pd.read_excel('Ventas 2020 - AdSocial.xlsx', sheet_name = 'Ventas 2020 Operativo', skiprows = 1)
KPIS_MP = pd.read_csv('KPIS 2020 - AdSocial - KPIS MP 2020.csv', skiprows = 2)
KPIS_FIC = pd.read_csv('KPIS 2020 - AdSocial - KPIS FIC 2020.csv', skiprows = 2)

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

KPIS_MP = pd.read_csv('KPIS 2020 - AdSocial - KPIS MP 2020.csv', skiprows = 2)
KPIS_FIC = pd.read_csv('KPIS 2020 - AdSocial - KPIS FIC 2020.csv', skiprows = 2)

 #Formato columnas
KPIS_FIC.loc[:,'NOMENCLATURA'] = KPIS_FIC.loc[:,'NOMENCLATURA'].str.lower()

KPIS_MP.loc[:,'NOMENCLATURA'] = KPIS_MP.loc[:,'NOMENCLATURA'].str.lower()
KPIS_MP.loc[:,'Fin'] = KPIS_MP.loc[:,'Fin'].apply(lambda x: str(x.replace('31-ene.','31/01/20')))

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

KPIS_MP.loc[:,'Inicio'] = Formato_Fechas(KPIS_MP, 'Inicio')
KPIS_MP.loc[:,'Fin'] = Formato_Fechas(KPIS_MP, 'Fin')

KPIS_FIC.loc[:,'Inicio'] = Formato_Fechas(KPIS_FIC, 'Inicio')
KPIS_FIC.loc[:,'Fin'] = Formato_Fechas(KPIS_FIC, 'Fin')

KPIS_MP.loc[:,'Costo Planeado'] = Formato_numerico(KPIS_MP, 'Costo Planeado')
KPIS_MP.loc[:,'KPI Planeado'] = Formato_numerico(KPIS_MP, 'KPI Planeado')
KPIS_MP.loc[:,'Serving'] = Formato_numerico(KPIS_MP, 'Serving')
KPIS_MP.loc[:,'Inversión Plataforma'] = Formato_numerico(KPIS_MP, 'Inversión Plataforma')
KPIS_MP.loc[:,'Inversión Total'] = Formato_numerico(KPIS_MP, 'Inversión Total')

KPIS_FIC.loc[:,'Inversión AdOps'] = Formato_numerico(KPIS_FIC, 'Inversión AdOps')
KPIS_FIC.loc[:,'Operativo AdOps'] = Formato_numerico(KPIS_FIC, 'Operativo AdOps')
KPIS_FIC.loc[:,'Serving AdOps'] = Formato_numerico(KPIS_FIC, 'Serving AdOps')
KPIS_FIC.loc[:,'Costo Operativo'] = Formato_numerico(KPIS_FIC, 'Costo Operativo')

    #Agrupación campañas Unicas, le concatenemos su plataforma para poder cruzarlo solo con los de Facebook sino agrupa por todo.
KPIS_MP['llave_ventas'] = KPIS_MP.loc[:,'Plataforma']

KPIS_MP.loc[KPIS_MP['Plataforma'].str.contains('Instagram') , 'llave_ventas'] = 'IG'
KPIS_MP.loc[KPIS_MP['Plataforma'].str.contains('Facebook') , 'llave_ventas'] = 'FB'
KPIS_MP.loc[KPIS_MP['Plataforma'].str.contains('Google') , 'llave_ventas'] = 'SEM'
KPIS_MP.loc[(KPIS_MP['Plataforma'].str.contains('Programmatic')) | (KPIS_MP['Plataforma'].str.contains('Display'))  , 'llave_ventas'] = 'DSP'
KPIS_MP.loc[(KPIS_MP['Plataforma'].str.contains('Waze')) | (KPIS_MP['Plataforma'].str.contains('AdsMovil')) , 'llave_ventas'] = 'PV'

KPIS_FIC.loc[KPIS_FIC['Plataforma'].str.contains('Instagram') , 'llave_ventas'] = 'IG'
KPIS_FIC.loc[KPIS_FIC['Plataforma'].str.contains('Facebook') , 'llave_ventas'] = 'FB'
KPIS_FIC.loc[KPIS_FIC['Plataforma'].str.contains('Google') , 'llave_ventas'] = 'SEM'
KPIS_FIC.loc[(KPIS_FIC['Plataforma'].str.contains('Programmatic')) | (KPIS_FIC['Plataforma'].str.contains('Display'))  , 'llave_ventas'] = 'DSP'
KPIS_FIC.loc[(KPIS_FIC['Plataforma'].str.contains('Waze')) | (KPIS_FIC['Plataforma'].str.contains('AdsMovil')) , 'llave_ventas'] = 'PV'

KPIS_MP.loc[:,'llave_ventas'] = KPIS_MP.loc[:,'NOMENCLATURA'] + str("_") + KPIS_MP['llave_ventas']
KPIS_MP["llave_ventas"].str.strip()

KPIS_FIC.loc[:,'llave_ventas'] = KPIS_FIC.loc[:,'NOMENCLATURA'] + str("_") + KPIS_FIC['llave_ventas']
KPIS_FIC["llave_ventas"].str.strip()

KPIS_MP = KPIS_MP.loc[:, ('NOMENCLATURA','llave_ventas','CAMPAÑA','CLIENTE','MARCA','Mes','Versión','Plataforma','Formato','Inicio','Fin','TDC','Objetivo','Costo Planeado','KPI Planeado','Serving','Inversión Plataforma','Inversión Total')]

KPIS_FIC = KPIS_FIC.loc[:, ('NOMENCLATURA','llave_ventas','CAMPAÑA','CLIENTE','MARCA','Mes','Versión','Plataforma','Formato','Inicio','Fin','TDC','Objetivo','Inversión AdOps','Operativo AdOps', 'Serving AdOps','Costo Operativo')]

KPIS_MP = KPIS_MP.groupby(['llave_ventas'], as_index = False).sum()
KPIS_MP = KPIS_MP[KPIS_MP.llave_ventas.str.contains('_FB')]

KPIS_FIC = KPIS_FIC.groupby(['llave_ventas'], as_index = False).sum()
KPIS_FIC = KPIS_FIC[KPIS_FIC.llave_ventas.str.contains('_FB')]


########
#Cruzes#
########
#MP
FB_MP = pd.merge(Facebook, KPIS_MP, how = 'left', left_on = 'llave_facebook', right_on = 'llave_ventas')
FB_MP_NO = FB_MP[pd.isnull(FB_MP.llave_ventas)]
#¿Cuantos cruzaron?
FB_MP = FB_MP[~pd.isnull(FB_MP.llave_ventas)]

MP_FB = pd.merge(KPIS_MP, Facebook, how = 'left', left_on = 'llave_ventas', right_on = 'llave_facebook')
MP_FB_NO = MP_FB[pd.isnull(MP_FB.llave_facebook)]
#¿Cuantos cruzaron? 
MP_FB = MP_FB[~pd.isnull(MP_FB.llave_facebook)]

#FIC
FB_FIC = pd.merge(Facebook, KPIS_FIC, how = 'left', left_on = 'llave_facebook', right_on = 'llave_ventas')
FB_FIC_NO = FB_FIC[pd.isnull(FB_FIC.llave_ventas)]
#¿Cuantos cruzaron?
FB_FIC = FB_FIC[~pd.isnull(FB_FIC.llave_ventas)]

FIC_FB = pd.merge(KPIS_FIC, Facebook, how = 'left', left_on = 'llave_ventas', right_on = 'llave_facebook')
FIC_FB_NO = FIC_FB[pd.isnull(FIC_FB.llave_facebook)]
#¿Cuantos cruzaron?
FIC_FB = FIC_FB[~pd.isnull(FIC_FB.llave_facebook)]

###########################
#Validacion de lo faltante#
###########################
#FB_MP

FB_MP_NO_1 = FB_MP_NO.llave_facebook.str.split("_", 10,expand = True)
FB_MP_NO_1.columns = ["Año-Mes","Cliente","Marca","Tipo-1","Tipo-2",""]
FB_MP_NO_1['archivo'] = 'FB_MP'
FB_MP_NO_1['Nombre_Campaña'] = FB_MP_NO.llave_facebook

MP_FB_NO_1 = MP_FB_NO.llave_ventas.str.split("_", 10,expand = True)
MP_FB_NO_1.columns = ["Año-Mes","Cliente","Marca","Tipo-1","Tipo-2",""]
MP_FB_NO_1['archivo'] = 'MP'
MP_FB_NO_1['Nombre_Campaña'] = MP_FB_NO.llave_ventas

Union = []
Union.append(FB_MP_NO_1)
Union.append(MP_FB_NO_1)

#FB_FIC
FB_FIC_NO_1 = FB_FIC_NO.llave_facebook.str.split("_", 10,expand = True)
FB_FIC_NO_1.columns = ["Año-Mes","Cliente","Marca","Tipo-1","Tipo-2",""]
FB_FIC_NO_1['archivo'] = 'FB_FIC'
FB_FIC_NO_1['Nombre_Campaña'] = FB_FIC_NO.llave_facebook

FIC_FB_NO_1 = FIC_FB_NO.llave_ventas.str.split("_", 10,expand = True)
FIC_FB_NO_1.columns = ["Año-Mes","Cliente","Marca","Tipo-1","Tipo-2",""]
FIC_FB_NO_1['archivo'] = 'FIC'
FIC_FB_NO_1['Nombre_Campaña'] = FIC_FB_NO.llave_ventas

Union.append(FB_FIC_NO_1)
Union.append(FIC_FB_NO_1)
Union = pd.concat(Union)

Union["Nombre_Campaña"] = Union["Nombre_Campaña"].str.replace("_FB","")

Union.archivo.value_counts()

#Desglose por cliente
OD = Union.loc[ Union.Cliente.str.contains('od', na = False) & ~Union.Cliente.str.contains('sodexo', na = False)]
RS = Union.loc[ Union.Cliente.str.contains('rs', na = False)]
THS = Union.loc[ Union.Cliente.str.contains('ths', na = False)]
PETCO = Union.loc[ Union.Cliente.str.contains('petco', na = False)]
GICSA = Union.loc[ Union.Cliente.str.contains('gicsa', na = False)]
GWEP = Union.loc[ Union.Cliente.str.contains('gwep', na = False)]

OD.shape[0] + RS.shape[0] + THS.shape[0] + PETCO.shape[0] + GICSA.shape[0] + GWEP.shape[0]

OTROS = Union.loc[ ~Union.Cliente.str.contains('od', na = False) & ~Union.Cliente.str.contains('rs', na = False) & ~Union.Cliente.str.contains('sodexo', na = False) & ~Union.Cliente.str.contains('ths', na = False) &
                  ~Union.Cliente.str.contains('petco', na = False) & ~Union.Cliente.str.contains('gicsa', na = False) & ~Union.Cliente.str.contains('gicsa', na = False) & ~Union.Cliente.str.contains('gwep', na = False)]