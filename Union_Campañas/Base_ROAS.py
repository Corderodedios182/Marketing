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

#Rutas
Ruta = input("Coloca la ruta donde se encuentran tus archivos: ") #Ejemplo: /home/carlos/Dropbox/ROAS 2020
os.chdir('/home/carlos/Dropbox/ROAS 2020')
Mes = input("¿Qué mes deseas actualizar? " + str(os.listdir( )) + " : " )
os.chdir('Enero')
Archivos = os.listdir()

#############################
#Importación de las bases
# -Limpieza de las bases
# -Estandarización
#   -Reglas de Fechas
#   -Columnas a ocupar
#   -Ver el nombre de la campaña por rmnt o pi (caso especial)
#
############################

#Facebook#
Arch_FB = [x for x in Archivos if "FB" in x]

Union_FB = []

for csv in Arch_FB:
    
    tmp = pd.read_csv(csv)
    tmp['Archivo'] = csv
    Union_FB.append(tmp)

Union_FB = pd.concat(Union_FB)

Union_FB = Union_FB.loc[:,('Archivo','Nombre de la cuenta','Nombre de la campaña','Mes','Inicio','Finalización',
                           'Divisa','Importe gastado (MXN)','Impresiones','Clics')]

Union_FB.head()

#Adwords#
Arch_Adwords = [x for x in Archivos if "Adwords" in x]

Union_Ad = []
fallas = []

for csv in Arch_Adwords:
    try:
        tmp = pd.read_csv(csv, sep = ',', skiprows = 2)
        tmp['Archivo'] = csv
        Union_Ad.append(tmp)
    except:
        #En ocasiones por el formato no leía el archivo utf-
        fallas.append(csv)
    print("En ocasiones se guardan como UTF-16 excell ocasionando estas fallas : ",fallas)

Union_Ad = pd.concat(Union_Ad).reset_index(drop = True)

Union_Ad = Union_Ad.loc[:,('Archivo','Cuenta','Campaña','Mes','Fecha de inicio','Fecha de finalización',
                           'Moneda','Costo','Impresiones','Clics')]

Union_Ad.head()

tmp = pd.concat([Union_Ad, Union_FB], axis = 0)


#Adform#
Arch_Adform = [x for x in Archivos if "Adform" in x]

#MP_FIC (KPI)#
Arch_MP_FIC = [x for x in Archivos if "KPI" in x]


#############################
#Unión de las Bases
# -Unión de todo
#
####

######################
#Exportación a Sheets#
######################
#Colocar la base completa en sheets
#   - Validar que no se puede colocar un archivo repetido
#   - 

