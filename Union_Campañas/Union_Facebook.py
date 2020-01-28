#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 12:44:23 2020

@author: carlos
"""
import os
import pandas as pd
#import datetime

os.chdir("/home/carlos/Documentos/Adsocial/Bases AdSocial/2020")
os.listdir()

Facebook = pd.read_csv('KPI-Jan-1-2020-Jan-22-2020.csv')

#Formato de Columnas

    #Fechas

Facebook.Inicio = pd.to_datetime(Facebook.Inicio,format = "%d/%m/%y")
#Facebook.Finalización = pd.to_datetime(Facebook.Finalización,format = "%d/%m/%y")

#Extracción del nombre para cruzar con ventas
C_Facebook = Facebook.loc[:,'Nombre de la campaña'].str.split("_",10,expand = True).iloc[:,:5] ; cols = ["Año-Mes","Cliente","Marca","Tipo-1","Tipo-2"]
C_Facebook.columns = cols
C_Facebook = C_Facebook[cols].apply(lambda row: '_'.join(row.values.astype(str)), axis=1) ; del cols

Facebook['Llave'] = C_Facebook ; del C_Facebook

#Columnas de interés
Facebook.keys()
Facebook = Facebook.loc[:,('Nombre de la cuenta','Nombre de la campaña','Llave','Mes','Objetivo','Inicio','Finalización','Importe gastado (MXN)','Impresiones','Clics en el enlace')]
Facebook.columns = ['Nombre_Cuenta','Nombre_campaña','llave','mes','objetivo','Fecha_Inicio','Fecha_Fin','dinero_gastado','impresiones','clics_enlace']
tmp = Facebook.groupby(['llave'], as_index = False).sum()
#Se eliminan las campañas provenientes de estás cuentas puede que no mache con el MP
Facebook = Facebook.loc[ ~( (Facebook.Nombre_Cuenta.str.contains('Adsocial'))  |  (Facebook.Nombre_Cuenta.str.contains('Dokkoi')) ) ]
Facebook.llave = Facebook.llave.str.lower()

#tmp = Facebook.groupby(['Nombre de la cuenta','Llave','Nombre de la campaña','Objetivo'], as_index = False).count()
#tmp_0 = Facebook[Facebook['Llave'] == '2001_gicsa_explanadapuebla_pi_mkt']
Facebook_tmp = Facebook.groupby(['llave'], as_index = False).sum()

########################
#Archivo de Ventas 2020#
########################

Ventas_Operativo = pd.read_excel('Ventas 2020 - AdSocial.xlsx', sheet_name = 'Ventas 2020 Operativo', skiprows = 1)
Ventas_Operativo.CAMPAÑA = Ventas_Operativo.CAMPAÑA.str.lower()
Ventas_Operativo = Ventas_Operativo[~pd.isnull(Ventas_Operativo.CLIENTE)]

#tmp_1 = Ventas_Operativo[Ventas_Operativo['CAMPAÑA'] == '2001_OD_Instagram_PI_MKT']
Ventas_Operativo.keys()

#Cruze Facebook vs Ventas_Operativas
Cruze_Facebook = pd.merge(Facebook_tmp,Ventas_Operativo,how = 'left', left_on = 'llave', right_on = 'CAMPAÑA')
NO_Cruze_Facebook = Cruze_Facebook[pd.isnull(Cruze_Facebook.CAMPAÑA)]
#¿Cuantos cruzaron? 12
Cruze_Facebook = Cruze_Facebook[~pd.isnull(Cruze_Facebook.CAMPAÑA)]

#¿Cuantas faltan de acuerdo a ventas? 25
Cruze_Ventas = pd.merge(Ventas_Operativo,Facebook_tmp,how = 'left', left_on = 'CAMPAÑA', right_on = 'llave')
NO_Cruze_Ventas = Cruze_Ventas[pd.isnull(Cruze_Ventas.llave)]

#Separación de la nomeclatura

tmp_1_f = NO_Cruze_Facebook.llave.str.split("_", expand = True) 
tmp_1_f.columns = ["Año-Mes","Cliente","Marca","Tipo-1","Tipo-2"]
tmp_1_f['archivo'] = 'Facebook'
tmp_1_f['Nombre_Campaña'] = NO_Cruze_Facebook.llave

tmp_1_f['Año-Mes'].value_counts()
tmp_1_f['Cliente'].value_counts()
tmp_1_f['Marca'].value_counts()
tmp_1_f['Tipo-1'].value_counts()
tmp_1_f['Tipo-2'].value_counts()

tmp_2_v = NO_Cruze_Ventas.CAMPAÑA.str.split("_", expand = True) 
tmp_2_v.columns = ["Año-Mes","Cliente","Marca","Tipo-1","Tipo-2"]
tmp_2_v['archivo'] = 'Ventas Operativo Facebook'
tmp_2_v['Nombre_Campaña'] = NO_Cruze_Ventas.CAMPAÑA

tmp_2_v['Año-Mes'].value_counts()
tmp_2_v['Cliente'].value_counts()
tmp_2_v['Marca'].value_counts()
tmp_2_v['Tipo-1'].value_counts()
tmp_2_v['Tipo-2'].value_counts()

Union = []
Union.append(tmp_1_f)
Union.append(tmp_2_v)
Union = pd.concat(Union)

Union.archivo.value_counts()

Union_f = Union
#
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
    wks = spr.worksheet('OTROS')

    filas = len(wks.get_all_values()) + 1
    set_with_dataframe(wks, OTROS, row = filas ,include_column_header = True)

else: 
    print("Ok!")    













