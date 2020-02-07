#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 12:44:23 2020

@author: carlos
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
pd.set_option('display.float_format', lambda x: '%.5f' % x)
#import datetime

os.chdir("/home/carlos/Documentos/Adsocial/Bases AdSocial/2020")
os.listdir()

Facebook = pd.read_csv('KPI-Jan-1-2020-Jan-22-2020.csv')

#Formato de Columnas

    #Fechas

Facebook.Inicio = pd.to_datetime(Facebook.Inicio,format = "%d/%m/%y")
#Facebook.Finalización = pd.to_datetime(Facebook.Finalización,format = "%d/%m/%y")
Facebook.dtypes

#Extracción del nombre para cruzar con ventas
C_Facebook = Facebook.loc[:,'Nombre de la campaña'].str.split("_",10,expand = True).iloc[:,:5] ; cols = ["Año-Mes","Cliente","Marca","Tipo-1","Tipo-2"]
C_Facebook.columns = cols
C_Facebook = C_Facebook[cols].apply(lambda row: '_'.join(row.values.astype(str)), axis=1) ; del cols

Facebook['Llave_Facebook'] = C_Facebook ; del C_Facebook
Facebook['Llave_Facebook'] = Facebook['Llave_Facebook'].str.strip()

#Columnas de interés
Facebook.keys()
Facebook = Facebook.loc[:,('Nombre de la cuenta','Nombre de la campaña','Llave_Facebook','Mes','Objetivo','Inicio','Finalización','Importe gastado (MXN)','Impresiones','Clics en el enlace')]
Facebook.columns = ['Nombre_Cuenta','Nombre_campaña','llave_facebook','mes','objetivo','Fecha_Inicio','Fecha_Fin','dinero_gastado','impresiones','clics_enlace']
#tmp = Facebook.groupby(['llave'], as_index = False).sum()
#Se eliminan las campañas provenientes de estás cuentas puede que no mache con el MP
Facebook = Facebook.loc[ ~( (Facebook.Nombre_Cuenta.str.contains('Adsocial'))  |  (Facebook.Nombre_Cuenta.str.contains('Dokkoi')) ) ]
Facebook.llave_facebook = Facebook.llave_facebook.str.lower()
Facebook.llave_facebook = Facebook.llave_facebook + str("_FB")

#tmp = Facebook.groupby(['Nombre de la cuenta','Llave','Nombre de la campaña','Objetivo'], as_index = False).count()
#tmp_0 = Facebook[Facebook['Llave'] == '2001_gicsa_explanadapuebla_pi_mkt']
Facebook = Facebook.groupby(['llave_facebook'], as_index = False).sum()

########################
#Archivo de Ventas 2020#
########################
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
KPIS_MP['Plt'] = KPIS_MP.loc[:,'Plataforma']

KPIS_MP.loc[KPIS_MP['Plataforma'].str.contains('Instagram') , 'Plt'] = 'IG'
KPIS_MP.loc[KPIS_MP['Plataforma'].str.contains('Facebook') , 'Plt'] = 'FB'
KPIS_MP.loc[KPIS_MP['Plataforma'].str.contains('Google') , 'Plt'] = 'SEM'
KPIS_MP.loc[(KPIS_MP['Plataforma'].str.contains('Programmatic')) | (KPIS_MP['Plataforma'].str.contains('Display'))  , 'Plt'] = 'DSP'
KPIS_MP.loc[(KPIS_MP['Plataforma'].str.contains('Waze')) | (KPIS_MP['Plataforma'].str.contains('AdsMovil')) , 'Plt'] = 'PV'

KPIS_FIC.loc[KPIS_FIC['Plataforma'].str.contains('Instagram') , 'Plt'] = 'IG'
KPIS_FIC.loc[KPIS_FIC['Plataforma'].str.contains('Facebook') , 'Plt'] = 'FB'
KPIS_FIC.loc[KPIS_FIC['Plataforma'].str.contains('Google') , 'Plt'] = 'SEM'
KPIS_FIC.loc[(KPIS_FIC['Plataforma'].str.contains('Programmatic')) | (KPIS_FIC['Plataforma'].str.contains('Display'))  , 'Plt'] = 'DSP'
KPIS_FIC.loc[(KPIS_FIC['Plataforma'].str.contains('Waze')) | (KPIS_FIC['Plataforma'].str.contains('AdsMovil')) , 'Plt'] = 'PV'

KPIS_MP['llave_ventas'] = KPIS_MP.loc[:,'NOMENCLATURA'] + str("_") + KPIS_MP['Plt']
KPIS_MP["llave_ventas"].str.strip()

KPIS_FIC['llave_ventas'] = KPIS_FIC.loc[:,'NOMENCLATURA'] + str("_") + KPIS_FIC['Plt']
KPIS_FIC["llave_ventas"].str.strip()

KPIS_MP = KPIS_MP.loc[:, ('NOMENCLATURA','llave_ventas','CAMPAÑA','CLIENTE','MARCA','Mes','Versión','Plataforma','Plt','Formato','Inicio','Fin','TDC','Objetivo','Costo Planeado','KPI Planeado','Serving','Inversión Plataforma','Inversión Total')]

KPIS_FIC = KPIS_FIC.loc[:, ('NOMENCLATURA','llave_ventas','CAMPAÑA','CLIENTE','MARCA','Mes','Versión','Plataforma','Plt','Formato','Inicio','Fin','TDC','Objetivo','Inversión AdOps','Operativo AdOps', 'Serving AdOps','Costo Operativo')]

#MP
KPIS_MP = KPIS_MP[~KPIS_MP['Versión'].str.contains('VC')]

KPIS_MP = KPIS_MP.groupby(['llave_ventas','Plt'], as_index = False).sum()
KPIS_MP.groupby(['Plt']).count()['llave_ventas'].reset_index()

fig, ax = plt.subplots()
rects1 = ax.bar(KPIS_MP.groupby(['Plt']).count()['llave_ventas'].reset_index()['Plt'],
                KPIS_MP.groupby(['Plt']).count()['llave_ventas'].reset_index()['llave_ventas']
                ,label='Plt')

ax.set_ylabel('Conteo')
ax.set_title('KPIS_MP Agrupación por Plataforma y Campaña')

def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


autolabel(rects1) ; fig.tight_layout() ; plt.show()

#FIC
KPIS_FIC = KPIS_FIC.groupby(['llave_ventas','Plt'], as_index = False).sum()
KPIS_FIC.groupby(['Plt']).count()['llave_ventas'].reset_index()

fig, ax = plt.subplots()
rects1 = ax.bar(KPIS_FIC.groupby(['Plt']).count()['llave_ventas'].reset_index()['Plt'],
                KPIS_FIC.groupby(['Plt']).count()['llave_ventas'].reset_index()['llave_ventas']
                ,label='Plt')

ax.set_ylabel('Conteo')
ax.set_title('KPIS_FIC Agrupación por Plataforma y Campaña')

def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

autolabel(rects1) ; fig.tight_layout() ; plt.show()

#¿Cual falta en el FIC Ó MP?
pd.merge(KPIS_MP, KPIS_FIC, how = 'inner')

####################################
#Separación del MP ó FIC Plataforma#
####################################

KPIS_FIC_FB = KPIS_FIC[KPIS_FIC.llave_ventas.str.contains('_FB')]

KPIS_MP_FB = KPIS_MP[KPIS_MP.llave_ventas.str.contains('_FB')]

########
#Cruzes#
########
#MP
FB_MP = pd.merge(Facebook, KPIS_MP_FB, how = 'left', left_on = 'llave_facebook', right_on = 'llave_ventas')
FB_MP_NO = FB_MP[pd.isnull(FB_MP.llave_ventas)]
#¿Cuantos cruzaron?
FB_MP = FB_MP[~pd.isnull(FB_MP.llave_ventas)]

MP_FB = pd.merge(KPIS_MP_FB, Facebook, how = 'left', left_on = 'llave_ventas', right_on = 'llave_facebook')
MP_FB_NO = MP_FB[pd.isnull(MP_FB.llave_facebook)]
#¿Cuantos cruzaron? 
MP_FB = MP_FB[~pd.isnull(MP_FB.llave_facebook)]

#FIC
FB_FIC = pd.merge(Facebook, KPIS_FIC_FB, how = 'left', left_on = 'llave_facebook', right_on = 'llave_ventas')
FB_FIC_NO = FB_FIC[pd.isnull(FB_FIC.llave_ventas)]
#¿Cuantos cruzaron?
FB_FIC = FB_FIC[~pd.isnull(FB_FIC.llave_ventas)]

FIC_FB = pd.merge(KPIS_FIC_FB, Facebook, how = 'left', left_on = 'llave_ventas', right_on = 'llave_facebook')
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

#########################################
#Escritura de los datos en Google Sheets#
#########################################

import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe #,get_as_dataframe

Escribir = input("Deseas escribir los datos en sheets si/no : ")

if Escribir == 'si':
    os.chdir('/home/carlos/Documentos/Adsocial/Bases AdSocial/2020')
    os.listdir()
    #Autentificacion con google cloud platform correo analytics.adsocial@gmail.com
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)
    spr = client.open_by_url('https://docs.google.com/spreadsheets/d/1UfJanJuI1uwmD_VH3_e_aC1p6-LmTjNel-CQap9nk-I/edit#gid=0')
    wks = spr.worksheet('GICSA')

    filas = len(wks.get_all_values()) + 1
    set_with_dataframe(wks, GICSA , row = filas ,include_column_header = True)

else: 
    print("Ok!")    













