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
import pandas as pd
import os
import glob

#En este script se encuentra la función que nos arroja la unión del MP y FIC
os.chdir('/home/carlos/Documentos/3_Adsocial/Marketing/Union_Campañas')
from librerias import MP_FIC
from librerias import Plataformas
from librerias import Escritura_Sheets

#Aquí descargo el nuevo archivo de KPIS
os.chdir('/home/carlos/Dropbox/ROAS 2020')
Archivos = os.listdir()

        #-- MP_FIC (KPI) --#
Arch_MP_FIC = [x for x in Archivos if "KPI" in x]
MP_FIC = MP_FIC.MP_FIC_tabla(Arch_MP_FIC)

        #-- Plataformas --#
Mes = 'Enero'

#Archivos_csv = glob.glob('/home/carlos/Dropbox/ROAS 2020/' + Mes + '/Semanal/**/*.csv')
#Archivos_xlsx = glob.glob('/home/carlos/Dropbox/ROAS 2020/' + Mes + '/Semanal/**/*.xlsx')

Archivos_csv = glob.glob('/home/carlos/Dropbox/ROAS 2020/' + Mes + '/Mensual/*.csv')
Archivos_xlsx = glob.glob('/home/carlos/Dropbox/ROAS 2020/' + Mes + '/Mensual/*.xlsx')

plataformas = Plataformas.Plataformas_tabla(Archivos_csv, Archivos_xlsx)

plataformas.plataforma.value_counts()

##############
#Base Master #
##############
MP_PLT = pd.merge(MP_FIC, plataformas, how = 'left', left_on = 'llave_ventas', right_on = 'llave_plataformas')
MP_PLT = MP_PLT.sort_values(['cliente','marca','llave_ventas','fecha_inicio_plan','plataforma_y'])

#Semanal
#Escritura_Sheets.Escritura(MP_PLT, 6, header = True, Escribir = 'si') 

#Mensual
Escritura_Sheets.Escritura(MP_PLT, 8, header = True, Escribir = 'si')

#Información que no cruzo
NO_CRUZO = MP_PLT[MP_PLT.plataforma_y.isnull()]
NO_CRUZO = NO_CRUZO.sort_values(['llave_ventas'])

Escritura_Sheets.Escritura(NO_CRUZO, 9, header = True, Escribir = 'si')


#
import os
import numpy as np
import matplotlib.pyplot as plt

plataformas.keys()
cuentas = plataformas.groupby(['plataforma'], as_index = False).count().loc[:,('plataforma','cuenta')]

x = cuentas.plataforma
y = cuentas.cuenta

fig, ax = plt.subplots()    
width = 0.75 # the width of the bars 
ind = np.arange(len(y))  # the x locations for the groups
ax.barh(ind, y, width, color="blue")
ax.set_yticks(ind+width/2)
ax.set_yticklabels(x, minor=False)
plt.title('Conteo registros plataformas (tabla plataformas)')
plt.xlabel('Se agrupa por la nomenclatura')
for i, v in enumerate(y):
    ax.text(v , i, str(v))

#Validemos cifras MP original y cruze
MP = [] #Me lo traigo de correr por pedazos el MP_FIC
MP.keys()
MP.loc[:,'Inversión Total'].sum() - MP_FIC.loc[:,'inversión_total'].sum() 


MP_FIC.keys()
MP_FIC[MP_FIC.versión.str.contains('VC')].groupby(['plataforma','versión'], as_index = False).count().loc[:,('plataforma','versión','cliente')]
MP_FIC[~MP_FIC.versión.str.contains('VC')].groupby(['plataforma','versión'], as_index = False).count().loc[:,('plataforma','versión','cliente')]
a = MP_FIC[~MP_FIC.versión.str.contains('VC') & MP_FIC.plataforma_abreviacion.str.contains('FB')].groupby(['llave_ventas','mes_plan'], as_index = False).count().loc[:,('llave_ventas','mes_plan','versión')]
a[a.versión > 1]

#Se duplican por error de la nomenclatura pero las cifras estan bien
b = MP_FIC[MP_FIC.llave_ventas == '2001_od_payclip_ppf_pfm_FB']
b = MP_FIC[MP_FIC.llave_ventas == '2002_petco_fulltrust_ppf_pfm_promo_FB']

x = cuentas.plataforma
y = cuentas.cuenta

fig, ax = plt.subplots()    
width = 0.75 # the width of the bars 
ind = np.arange(len(y))  # the x locations for the groups
ax.barh(ind, y, width, color="blue")
ax.set_yticks(ind+width/2)
ax.set_yticklabels(x, minor=False)
plt.title('Conteo registros plataformas (tabla plataformas)')
plt.xlabel('Se agrupa por la nomenclatura')
for i, v in enumerate(y):
    ax.text(v , i, str(v))










