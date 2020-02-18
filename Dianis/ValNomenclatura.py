#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 11:22:10 2020

@author: dianabarquera
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib


pd.set_option('display.float_format', lambda x: '%.5f' % x)

#import datetime

os.chdir("/Users/dianabarquera/AdSocial Dropbox/Diana Barquera/Bases AdSocial/2020/Febrero/")
os.listdir()

#########################################################################################################################################################
####################              Archivo de Ventas 2020              #################################################################################################
#########################################################################################################################################################


KPIS_MP = pd.read_excel('KPIS 2020 - AdSocial.xlsx', skiprows = 2, sheet_name='KPIS MP 2020')
KPIS_FIC = pd.read_excel('KPIS 2020 - AdSocial.xlsx', skiprows = 2, sheet_name='KPIS FIC 2020')

 #Formato columnas
KPIS_FIC.loc[:,'NOMENCLATURA'] = KPIS_FIC.loc[:,'NOMENCLATURA'].str.lower()

KPIS_MP.loc[:,'NOMENCLATURA'] = KPIS_MP.loc[:,'NOMENCLATURA'].str.lower()
# KPIS_MP.loc[:,'Fin'] = KPIS_MP.loc[:,'Fin'].apply(lambda x: str(x.replace('31-ene.','31/01/20')))

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
tmp = pd.merge(KPIS_MP, KPIS_FIC, how = 'inner')


#########################################################################################################################################################
####################              FACEBOOK              #################################################################################################
#########################################################################################################################################################

pd.set_option('display.float_format', lambda x: '%.5f' % x)

#import datetime

os.chdir("/Users/dianabarquera/AdSocial Dropbox/Diana Barquera/Bases AdSocial/2020/Febrero/")
os.listdir()

Facebook = pd.read_csv('KPI-Jan-1-2020-Feb-14-2020.csv')

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




#################################################################################################
########################         Separación del MP ó FIC Plataforma     #########################
#################################################################################################

KPIS_FIC_FB = KPIS_FIC[KPIS_FIC.llave_ventas.str.contains('_FB')]

KPIS_MP_FB = KPIS_MP[KPIS_MP.llave_ventas.str.contains('_FB')]

##########
# Cruces #
##########

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

#############################
# Validacion de lo faltante #
#############################


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



##################################################################################
#             Escritura de los datos en Google Sheets FACEBOOK
##################################################################################

import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe #,get_as_dataframe

Escribir = input("Deseas escribir los datos en sheets si/no : ")

if Escribir == 'si':
    os.chdir('/Users/dianabarquera/AdSocial Dropbox/Diana Barquera/Bases AdSocial/2020/Febrero/')
    os.listdir()
    #Autentificacion con google cloud platform correo analytics.adsocial@gmail.com
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)
    spr = client.open_by_url('https://docs.google.com/spreadsheets/d/1UfJanJuI1uwmD_VH3_e_aC1p6-LmTjNel-CQap9nk-I/edit#gid=0')
    wks = spr.worksheet('Información_Bien')

    filas = len(wks.get_all_values()) + 1
    set_with_dataframe(wks, FB_MP, row = filas ,include_column_header = True)

else: 
    print("Ok!")    


#########################################################################################################################################################
####################          ADFORM            #########################################################################################################
#########################################################################################################################################################


pd.set_option('display.float_format', lambda x: '%.5f' % x)

#import datetime

os.chdir("/Users/dianabarquera/AdSocial Dropbox/Diana Barquera/Bases AdSocial/2020/Febrero/")
os.listdir()

Adform = pd.read_csv('Nom_14_02_2020.csv', skiprows=8, skipfooter=1, engine='python')

#Formato de Columnas

#Fechas
Adform['Date'] = pd.to_datetime(Adform.loc[:, ('Campaign Start Date') ], format = "%d/%m/%y")

Adform.dtypes

#Extracción del nombre para cruzar con ventas
C_Adform = Adform.loc[:,'Campaign'].str.split("_",10,expand = True).iloc[:,:5] ; cols = ["Año-Mes","Cliente","Marca","Tipo-1","Tipo-2"]
C_Adform.columns = cols
C_Adform = C_Adform[cols].apply(lambda row: '_'.join(row.values.astype(str)), axis=1) ; del cols

Adform['Llave_Adform'] = C_Adform ; del C_Adform
Adform['Llave_Adform'] = Adform['Llave_Adform'].str.strip()

#Columnas de interés
Adform.keys()
Adform = Adform.loc[:,('Client','Campaign','Llave_Adform','Date', 'Tracked Ads', 'Clicks','Conversions', 'Sales (All)')]
Adform.columns = ['Nombre_Cuenta','Nombre_campaña','llave_adform','mes','impresiones','clicks', 'conversiones', 'revenue']

#tmp = Adform.groupby(['llave_adform'], as_index = False).count()
#tmp_1 = Adform[Adform.llave_adform == '2002_OD_Brother-Impresion_PPF_PFM']

Adform = Adform.groupby(['llave_adform'], as_index = False).sum()

#Se eliminan las campañas provenientes de estás cuentas puede que no mache con el MP
Adform = Adform.loc[ Adform.llave_adform.str.contains('20') ]
Adform.llave_adform = Adform.llave_adform.str.lower()
Adform.llave_adform = Adform.llave_adform + str("_DSP")


#################################################################################################
########################         Separación del MP ó FIC Plataforma     #########################
#################################################################################################

KPIS_FIC_DSP = KPIS_FIC[KPIS_FIC.llave_ventas.str.contains('_DSP')]

KPIS_MP_DSP = KPIS_MP[KPIS_MP.llave_ventas.str.contains('_DSP')]


#################################################################################################
########################         Cruces                                 #########################
#################################################################################################

tmp = pd.concat([Adform, KPIS_MP_DSP], axis = 0)


#MP
DSP_MP = pd.merge(Adform, KPIS_MP_DSP, how = 'left', left_on = 'llave_adform', right_on = 'llave_ventas')
DSP_MP_NO = DSP_MP[pd.isnull(DSP_MP.llave_ventas)]

#¿Cuantos cruzaron?
DSP_MP = DSP_MP[~pd.isnull(DSP_MP.llave_ventas)]

MP_DSP = pd.merge(KPIS_MP_DSP, Adform, how = 'left', left_on = 'llave_ventas', right_on = 'llave_adform')
MP_DSP_NO = MP_DSP[pd.isnull(MP_DSP.llave_adform)]

#¿Cuantos cruzaron? 
MP_DSP = MP_DSP[~pd.isnull(MP_DSP.llave_adform)]

#FIC
DSP_FIC = pd.merge(Adform, KPIS_FIC_DSP, how = 'left', left_on = 'llave_adform', right_on = 'llave_ventas')
DSP_FIC_NO = DSP_FIC[pd.isnull(DSP_FIC.llave_ventas)]

#¿Cuantos cruzaron?
DSP_FIC = DSP_FIC[~pd.isnull(DSP_FIC.llave_ventas)]

FIC_DSP = pd.merge(KPIS_FIC_DSP, Adform, how = 'left', left_on = 'llave_ventas', right_on = 'llave_adform')
FIC_DSP_NO = FIC_DSP[pd.isnull(FIC_DSP.llave_adform)]

#¿Cuantos cruzaron?
FIC_DSP = FIC_DSP[~pd.isnull(FIC_DSP.llave_adform)]



#################################################################################################
########################         Validación de lo faltante              #########################
#################################################################################################


#DSP_MP

DSP_MP_NO_1 = DSP_MP_NO.llave_adform.str.split("_", 10,expand = True)
DSP_MP_NO_1
DSP_MP_NO_1.columns = ["Año-Mes","Cliente","Marca","Tipo-1","Tipo-2",""]
DSP_MP_NO_1['archivo'] = 'DSP_MP'
DSP_MP_NO_1['Nombre_Campaña'] = DSP_MP_NO.llave_adform

MP_DSP_NO_1 = MP_DSP_NO.llave_ventas.str.split("_", 10,expand = True)
MP_DSP_NO_1.columns = ["Año-Mes","Cliente","Marca","Tipo-1","Tipo-2",""]
MP_DSP_NO_1['archivo'] = 'MP'
MP_DSP_NO_1['Nombre_Campaña'] = MP_DSP_NO.llave_ventas

Union = []
Union.append(DSP_MP_NO_1)
Union.append(MP_DSP_NO_1)


#DSP_FIC

DSP_FIC_NO_1 = DSP_FIC_NO.llave_adform.str.split("_", 10,expand = True)
DSP_FIC_NO_1.columns = ["Año-Mes","Cliente","Marca","Tipo-1","Tipo-2",""]
DSP_FIC_NO_1['archivo'] = 'DSP_FIC'
DSP_FIC_NO_1['Nombre_Campaña'] = DSP_FIC_NO.llave_adform

FIC_DSP_NO_1 = FIC_DSP_NO.llave_ventas.str.split("_", 10,expand = True)
FIC_DSP_NO_1.columns = ["Año-Mes","Cliente","Marca","Tipo-1","Tipo-2",""]
FIC_DSP_NO_1['archivo'] = 'FIC'
FIC_DSP_NO_1['Nombre_Campaña'] = FIC_DSP_NO.llave_ventas

Union.append(DSP_FIC_NO_1)
Union.append(FIC_DSP_NO_1)
Union = pd.concat(Union)

Union["Nombre_Campaña"] = Union["Nombre_Campaña"].str.replace("_DSP","")
Union.archivo.value_counts()

#Desglose por cliente

Union.Cliente.value_counts()

OD = Union.loc[ Union.Cliente.str.contains('od', na = False)]
RS = Union.loc[ Union.Cliente.str.contains('rs', na = False)]
THS = Union.loc[ Union.Cliente.str.contains('ths', na = False)]
PETCO = Union.loc[ Union.Cliente.str.contains('petco', na = False)]
GWEP = Union.loc[ Union.Cliente.str.contains('gwep', na = False)]

OD.shape[0] + RS.shape[0] + THS.shape[0] + PETCO.shape[0] + GWEP.shape[0]

#OTROS = Union.loc[ ~Union.Cliente.str.contains('od', na = False) & ~Union.Cliente.str.contains('rs', na = False) & ~Union.Cliente.str.contains('sodexo', na = False) & ~Union.Cliente.str.contains('ths', na = False) &
                  #~Union.Cliente.str.contains('petco', na = False) & ~Union.Cliente.str.contains('gicsa', na = False) & ~Union.Cliente.str.contains('gicsa', na = False) & ~Union.Cliente.str.contains('gwep', na = False)]


##################################################################################
#             Escritura de los datos en Google Sheets ADFORM
##################################################################################

import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe #,get_as_dataframe

Escribir = input("Deseas escribir los datos en sheets si/no : ")

if Escribir == 'si':
    os.chdir('/Users/dianabarquera/AdSocial Dropbox/Diana Barquera/Bases AdSocial/2020/Febrero/')
    os.listdir()
    #Autentificacion con google cloud platform correo analytics.adsocial@gmail.com
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)
    spr = client.open_by_url('https://docs.google.com/spreadsheets/d/1UfJanJuI1uwmD_VH3_e_aC1p6-LmTjNel-CQap9nk-I/edit#gid=0')
    wks = spr.worksheet('Información_Bien')

    filas = len(wks.get_all_values()) + 1
    set_with_dataframe(wks, DSP_MP, row = filas ,include_column_header = True)

else: 
    print("Ok!")    




#########################################################################################################################################################
####################          GOOGLE ADWORDS            #########################################################################################################
#########################################################################################################################################################


pd.set_option('display.float_format', lambda x: '%.5f' % x)

#import datetime

os.chdir("/Users/dianabarquera/AdSocial Dropbox/Diana Barquera/Bases AdSocial/2020/Febrero/")
os.listdir()

Adwords = pd.read_csv('Adwords 1-01-2020 al 14-02-2020.csv', skiprows=2)

Adwords.keys()

#Formato de Columnas

#Fechas

Adwords['Fecha de inicio'] = pd.to_datetime(Adwords['Fecha de inicio'], format='%d/%m/%y')

#Adwords['Fecha de finalización'] = pd.to_datetime(Adwords['Fecha de finalización'], format='%Y-%m-%d', errors = 'coerce')

Adwords.dtypes

#Extracción del nombre para cruzar con ventas
C_Adwords = Adwords.loc[:,'Campaña'].str.split("_",10,expand = True).iloc[:,:5] ; cols = ["Año-Mes","Cliente","Marca","Tipo-1","Tipo-2"]
C_Adwords.columns = cols
C_Adwords = C_Adwords[cols].apply(lambda row: '_'.join(row.values.astype(str)), axis=1) ; del cols

Adwords['Llave_Adwords'] = C_Adwords ; del C_Adwords
Adwords['Llave_Adwords'] = Adwords['Llave_Adwords'].str.strip()

#Columnas de interés
Adwords.keys()

Adwords = Adwords.loc[:,('Cuenta', 'Campaña', 'Llave_Adwords', 'Fecha de inicio', 'Impresiones', 'Clics', 'Costo')]
Adwords.columns = ['Nombre_Cuenta','Nombre_campaña','llave_adwords','Fecha de inicio','impresiones','clicks', 'dinero_gastado']

#tmp = Adwords.groupby(['llave_adwords'], as_index = False).count()
#tmp_1 = Adwords[Adwords.llave_adwords == '2002_OD_Brother-Impresion_PPF_PFM']

Adwords = Adwords.groupby(['llave_adwords'], as_index = False).sum()

#Se eliminan las campañas provenientes de estás cuentas puede que no mache con el MP
Adwords = Adwords.loc[ Adwords.llave_adwords.str.contains('20') ]
Adwords.llave_adwords = Adwords.llave_adwords.str.lower()
Adwords.llave_adwords = Adwords.llave_adwords + str("_SEM")


#################################################################################################
########################         Separación del MP ó FIC Plataforma     #########################
#################################################################################################

KPIS_FIC_SEM = KPIS_FIC[KPIS_FIC.llave_ventas.str.contains('_SEM')]

KPIS_MP_SEM = KPIS_MP[KPIS_MP.llave_ventas.str.contains('_SEM')]


#################################################################################################
########################         Cruces                                 #########################
#################################################################################################

tmp = pd.concat([Adwords, KPIS_MP_SEM], axis = 0)


#MP
SEM_MP = pd.merge(Adwords, KPIS_MP_SEM, how = 'left', left_on = 'llave_adwords', right_on = 'llave_ventas')
SEM_MP_NO = SEM_MP[pd.isnull(SEM_MP.llave_ventas)]

#¿Cuantos cruzaron?
SEM_MP = SEM_MP[~pd.isnull(SEM_MP.llave_ventas)]

MP_SEM = pd.merge(KPIS_MP_SEM, Adwords, how = 'left', left_on = 'llave_ventas', right_on = 'llave_adwords')
MP_SEM_NO = MP_SEM[pd.isnull(MP_SEM.llave_adwords)]

#¿Cuantos cruzaron? 
MP_SEM = MP_SEM[~pd.isnull(MP_SEM.llave_adwords)]

#FIC
SEM_FIC = pd.merge(Adwords, KPIS_FIC_SEM, how = 'left', left_on = 'llave_adwords', right_on = 'llave_ventas')
SEM_FIC_NO = SEM_FIC[pd.isnull(SEM_FIC.llave_ventas)]

#¿Cuantos cruzaron?
SEM_FIC = SEM_FIC[~pd.isnull(SEM_FIC.llave_ventas)]

FIC_SEM = pd.merge(KPIS_FIC_SEM, Adwords, how = 'left', left_on = 'llave_ventas', right_on = 'llave_adwords')
FIC_SEM_NO = FIC_SEM[pd.isnull(FIC_SEM.llave_adwords)]

#¿Cuantos cruzaron?
FIC_SEM = FIC_SEM[~pd.isnull(FIC_SEM.llave_adwords)]



#################################################################################################
########################         Validación de lo faltante              #########################
#################################################################################################


#SEM_MP

SEM_MP_NO_1 = SEM_MP_NO.llave_adwords.str.split("_", 10,expand = True)
SEM_MP_NO_1
SEM_MP_NO_1.columns = ["Año-Mes","Cliente","Marca","Tipo-1","Tipo-2",""]
SEM_MP_NO_1['archivo'] = 'SEM_MP'
SEM_MP_NO_1['Nombre_Campaña'] = SEM_MP_NO.llave_adwords

MP_SEM_NO_1 = MP_SEM_NO.llave_ventas.str.split("_", 10,expand = True)
MP_SEM_NO_1.columns = ["Año-Mes","Cliente","Marca","Tipo-1","Tipo-2",""]
MP_SEM_NO_1['archivo'] = 'MP'
MP_SEM_NO_1['Nombre_Campaña'] = MP_SEM_NO.llave_ventas

Union = []
Union.append(SEM_MP_NO_1)
Union.append(MP_SEM_NO_1)


#SEM_FIC

SEM_FIC_NO_1 = SEM_FIC_NO.llave_adwords.str.split("_", 10,expand = True)
SEM_FIC_NO_1.columns = ["Año-Mes","Cliente","Marca","Tipo-1","Tipo-2",""]
SEM_FIC_NO_1['archivo'] = 'SEM_FIC'
SEM_FIC_NO_1['Nombre_Campaña'] = SEM_FIC_NO.llave_adwords

FIC_SEM_NO_1 = FIC_SEM_NO.llave_ventas.str.split("_", 10,expand = True)
FIC_SEM_NO_1.columns = ["Año-Mes","Cliente","Marca","Tipo-1","Tipo-2",""]
FIC_SEM_NO_1['archivo'] = 'FIC'
FIC_SEM_NO_1['Nombre_Campaña'] = FIC_SEM_NO.llave_ventas

Union.append(SEM_FIC_NO_1)
Union.append(FIC_SEM_NO_1)
Union = pd.concat(Union)

Union["Nombre_Campaña"] = Union["Nombre_Campaña"].str.replace("_SEM","")
Union.archivo.value_counts()

#Desglose por cliente

Union.Cliente.value_counts()

OD = Union.loc[ Union.Cliente.str.contains('od', na = False)]
RS = Union.loc[ Union.Cliente.str.contains('rs', na = False)]
THS = Union.loc[ Union.Cliente.str.contains('ths', na = False)]
PETCO = Union.loc[ Union.Cliente.str.contains('petco', na = False)]
GWEP = Union.loc[ Union.Cliente.str.contains('gwep', na = False)]

OTROS = Union.loc[ ~Union.Cliente.str.contains('od', na = False) & ~Union.Cliente.str.contains('rs', na = False) & ~Union.Cliente.str.contains('sodexo', na = False) & ~Union.Cliente.str.contains('ths', na = False) &
                  ~Union.Cliente.str.contains('petco', na = False) & ~Union.Cliente.str.contains('gicsa', na = False) & ~Union.Cliente.str.contains('gicsa', na = False) & ~Union.Cliente.str.contains('gwep', na = False)]

OD.shape[0] + RS.shape[0] + THS.shape[0] + PETCO.shape[0] + GWEP.shape[0]                  

##################################################################################
#             Escritura de los datos en Google Sheets ADFORM
##################################################################################

import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe #,get_as_dataframe

Escribir = input("Deseas escribir los datos en sheets si/no : ")

if Escribir == 'si':
    os.chdir('/Users/dianabarquera/AdSocial Dropbox/Diana Barquera/Bases AdSocial/2020/Febrero/')
    os.listdir()
    #Autentificacion con google cloud platform correo analytics.adsocial@gmail.com
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)
    spr = client.open_by_url('https://docs.google.com/spreadsheets/d/1UfJanJuI1uwmD_VH3_e_aC1p6-LmTjNel-CQap9nk-I/edit#gid=0')
    wks = spr.worksheet('OD')

    filas = len(wks.get_all_values()) + 1
    set_with_dataframe(wks, OD, row = filas ,include_column_header = True)

else: 
    print("Ok!")    




























































    
    
    
    


