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
os.listdir()

from librerias import MP_FIC
from librerias import Plataformas
from librerias import Escritura_Sheets

#Aquí descargo el nuevo archivo de KPIS
os.chdir('/home/carlos/Dropbox/ROAS 2020')
Archivos = os.listdir()

#-- MP_FIC (KPI) --#
#La funcion MP_FIC_tabla que vive en el script MP_FIC nos ayuda a procesar el MP y FIC, descargado del google drive KPIS 2020
Arch_MP_FIC = [x for x in Archivos if "KPI" in x]
mp_fic = MP_FIC.MP_FIC_tabla(Arch_MP_FIC)

#-- Plataformas --#
#Une los archivos de las plataformas que se dejan en las carpetas del dropbox, se pueden unir de forma semanal o mensual (la fecha de referencia será la fecha del reporte).
def archivos_plataformas(mes = 'Enero', tipo_union = 'Semanal'):
    if tipo_union == 'Semanal':
        Archivos_csv = glob.glob('/home/carlos/Dropbox/ROAS 2020/' + mes + '/Semanal/**/*.csv')
        Archivos_xlsx = glob.glob('/home/carlos/Dropbox/ROAS 2020/' + mes + '/Semanal/**/*.xlsx')
    else:
        Archivos_csv = glob.glob('/home/carlos/Dropbox/ROAS 2020/' + mes + '/Mensual/*.csv')
        Archivos_xlsx = glob.glob('/home/carlos/Dropbox/ROAS 2020/' + mes + '/Mensual/*.xlsx')
    return Archivos_csv, Archivos_xlsx

#Solo es necesario especificar el nombre del Mes de la carpeta y el tipo de union.
archivos_csv_01, archivos_xlsx_01 = archivos_plataformas(mes = 'Enero', tipo_union = 'Semanal')
archivos_csv_02, archivos_xlsx_02 = archivos_plataformas(mes = 'Febrero', tipo_union = 'Semanal')

#Base con la información de los reportes de todas las plataformas
plataformas_01 = Plataformas.Plataformas_tabla(archivos_csv_01, archivos_xlsx_01)
plataformas_02 = Plataformas.Plataformas_tabla(archivos_csv_02, archivos_xlsx_02)

plataformas_01.plataforma.value_counts()
plataformas_02.plataforma.value_counts()

plataformas = pd.concat([plataformas_01,plataformas_02])

del archivos_csv_01, archivos_csv_02, archivos_xlsx_01, archivos_xlsx_02, Arch_MP_FIC, Archivos

#a = plataformas_01[plataformas_01.llave_plataformas.str.contains('pachuca')]

##############
#Base Master
#Aun se están haciendo pruebas para trabajar cada mes por separado, hacer una función que una todo dependiendo del mes#
##############
#plt
mp_plt_01 = pd.merge(mp_fic, plataformas_01, how = 'left', left_on = 'llave_ventas', right_on = 'llave_plataformas')

bien_01 = mp_plt_01[(mp_plt_01.mes_plan == 'Enero') & ~(mp_plt_01.plataforma_y.isnull())]
mal_01 = mp_plt_01[(mp_plt_01.mes_plan == 'Enero') & (mp_plt_01.plataforma_y.isnull())]

mp_plt_01['mes_cruze'] = 'Enero'
#Los que no cruzaron de enero
mp_plt_01.mes_plan.value_counts()

b = mp_plt_01[mp_plt_01.llave_ventas.str.contains('pachuca')]
#'2001_GICSA_ExplanadaPachuca_PI_MKT_SEM_TRF' #Revisar si es correcto que este en 2 reportes

mp_plt_02 = pd.merge(mp_fic, plataformas_02, how = 'left', left_on = 'llave_ventas', right_on = 'llave_plataformas')
mp_plt_02['mes_cruze'] = 'Febrero'

mp_plt_02.mes_plan.value_counts()

bien_02 = mp_plt_02[~mp_plt_02.plataforma_y.isnull()]
mal_02 = mp_plt_02[(mp_plt_02.mes_plan == 'Febrero') & (mp_plt_02.plataforma_y.isnull())]

c = mp_plt_02[mp_plt_02.llave_ventas.str.contains('pachuca')]

union = pd.concat([bien_01, bien_02])

union.mes_cruze.value_counts()

union = union.fillna('')
union['llave_unica'] = union.llave_ventas + "-" + union.versión + "-" +  union.mes_plan

FB = union[union.plataforma_abreviacion.str.contains('FB')]
ADFORM = union[union.plataforma_abreviacion.str.contains('DSP')]
ADWORDS = union[union.plataforma_abreviacion.str.contains('SEM')]

a = ADWORDS[ADWORDS.llave_ventas.str.contains('pachuca')]

union[union.cliente.str.contains('Depot')]
union.cliente.value_counts()

##########################################################
#Cruzes para detectar errores de nomenclatura en mp ó plt#
##########################################################

#plt con mp
plt_mp = pd.merge(plataformas, mp_fic, how = 'left', left_on = 'llave_plataformas', right_on = 'llave_ventas')
plt_mp_no = plt_mp[pd.isnull(plt_mp.llave_ventas)]
#¿Cuantos cruzaron?
plt_mp = plt_mp[~pd.isnull(plt_mp.llave_ventas)]
#mp con plt
mp_plt = pd.merge(mp_fic, plataformas, how = 'left', left_on = 'llave_ventas', right_on = 'llave_plataformas')
mp_plt_no = mp_plt[pd.isnull(mp_plt.llave_plataformas)]
#¿Cuantos cruzaron? 
mp_plt = mp_plt[~pd.isnull(mp_plt.llave_plataformas)]

###########################
#Validacion de lo faltante#
###########################
#plt_mp
plt_mp_no_1 = plt_mp_no.llave_plataformas.str.split("_", 10,expand = True)
plt_mp_no_1.columns = ["Año-Mes","Cliente","Marca","Tipo-1","Tipo-2","dummy"]
plt_mp_no_1['dummy'] = ''
plt_mp_no_1['archivo'] = 'plt_mp'
plt_mp_no_1['Nombre_Campaña'] = plt_mp_no.llave_plataformas

mp_plt_no_1 = mp_plt_no.llave_ventas.str.split("_", 10,expand = True)
mp_plt_no_1.columns = ["Año-Mes","Cliente","Marca","Tipo-1","Tipo-2","dummy","dummy"]
mp_plt_no_1 = mp_plt_no_1.iloc[:,[0,1,2,3,4,5]]
mp_plt_no_1['archivo'] = 'mp_plt'
mp_plt_no_1['Nombre_Campaña'] = mp_plt_no.llave_ventas

Union = []
Union.append(plt_mp_no_1)
Union.append(mp_plt_no_1)
Union = pd.concat(Union)

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
Escritura_Sheets.Escritura(OD, 12, header = True, Escribir = 'no')
Escritura_Sheets.Escritura(RS, 13, header = True, Escribir = 'no')
Escritura_Sheets.Escritura(THS, 14, header = True, Escribir = 'no')
Escritura_Sheets.Escritura(PETCO, 15, header = True, Escribir = 'no')
Escritura_Sheets.Escritura(GICSA, 16, header = True, Escribir = 'no')
Escritura_Sheets.Escritura(GWEP, 17, header = True, Escribir = 'no')
Escritura_Sheets.Escritura(OTROS, 18, header = True, Escribir = 'no')

#Validaciones del momento (borrar)
a = union[union.llave_plataformas.str.contains('2002_odcam')]

tmp = union[union.mes_cruze == 'Febrero']





