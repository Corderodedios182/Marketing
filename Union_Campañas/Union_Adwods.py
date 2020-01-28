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
Adwords_tmp = Adwords.groupby(['Llave'], as_index = False).sum()

########################
#Archivo de Ventas 2020#
########################
Ventas_Operativo = pd.read_excel('Ventas 2020 - AdSocial.xlsx', sheet_name = 'Ventas 2020 Operativo', skiprows = 1)
Ventas_Operativo.CAMPAÑA = Ventas_Operativo.CAMPAÑA.str.lower()
Ventas_Operativo = Ventas_Operativo[~pd.isnull(Ventas_Operativo.CLIENTE)]

#Cruze Adwords vs Ventas_Operativas
Cruze_Adwords = pd.merge(Adwords_tmp, Ventas_Operativo, how = 'left', left_on = 'Llave', right_on = 'CAMPAÑA')
NO_Cruze_Adwords = Cruze_Adwords[pd.isnull(Cruze_Adwords.CAMPAÑA)]
#¿Cuantas cruzaron?
Cruze_Adwords = Cruze_Adwords[~pd.isnull(Cruze_Adwords.CAMPAÑA)]

#¿Cuantas faltan?
Cruze_Ventas = pd.merge(Ventas_Operativo,Adwords_tmp,how = 'left', left_on = 'CAMPAÑA', right_on = 'Llave')
NO_Cruze_Ventas = Cruze_Ventas[pd.isnull(Cruze_Ventas.Llave)]

tmp_1_f = NO_Cruze_Adwords.Llave.str.split("_", expand = True) 
tmp_1_f.columns = ["Año-Mes","Cliente","Marca","Tipo-1","Tipo-2"]
tmp_1_f['archivo'] = 'Adwords'
tmp_1_f['Nombre_Campaña'] = NO_Cruze_Adwords.Llave

tmp_1_f['Año-Mes'].value_counts()
tmp_1_f['Cliente'].value_counts()
tmp_1_f['Marca'].value_counts()
tmp_1_f['Tipo-1'].value_counts()
tmp_1_f['Tipo-2'].value_counts()

tmp_2_v = NO_Cruze_Ventas.CAMPAÑA.str.split("_", expand = True) 
tmp_2_v.columns = ["Año-Mes","Cliente","Marca","Tipo-1","Tipo-2"]
tmp_2_v['archivo'] = 'Ventas Operativo Adwords'
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

Union_a = Union








