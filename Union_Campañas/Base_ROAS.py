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
pd.set_option('display.float_format', lambda x: '%.10f' % x)

#Aquí descargo el nuevo archivo de KPIS
os.chdir('/home/carlos/Dropbox/ROAS 2020')
Archivos = os.listdir()

#-- MP_FIC (KPI) --#
#La funcion MP_FIC_tabla que vive en el script MP_FIC nos ayuda a procesar el MP y FIC, descargado del google drive KPIS 2020
Arch_MP_FIC = [x for x in Archivos if "KPIS 2020 .xlsx" in x]
#La función regresa una tupla con mp_fic, mp, fic
tablas_mp_fic =  MP_FIC.MP_FIC_tabla(Arch_MP_FIC)

mp_fic = tablas_mp_fic[0]
mp = tablas_mp_fic[1] 
fic = tablas_mp_fic[2] 

#Cuadrando el mp
list(enumerate(mp_fic.keys()))
mp_fic['conteo'] = 1
#Veamos que podemos tener algunos duplicados por los temas de la llave que no es unica
#Duplicado incorrecto
a = mp_fic[mp_fic.llave_ventas.str.contains('2003_gicsa_paseointerlomas_pi_mkt_PV')]
b = mp[mp.llave_ventas.str.contains('2003_gicsa_paseointerlomas_pi_mkt_PV')]
c = fic[fic.llave_ventas.str.contains('2003_gicsa_paseointerlomas_pi_mkt_PV')]
#Duplicado correcto
a = mp_fic[mp_fic.llave_ventas.str.contains('2003_od_brother-impresion_ppf_pfm_SEM')]
b = mp[mp.llave_ventas.str.contains('2003_od_brother-impresion_ppf_pfm_SEM')]
c = fic[fic.llave_ventas.str.contains('2003_od_brother-impresion_ppf_pfm_SEM')]

#nuevos duplicados
a = mp_fic[mp_fic.llave_ventas.str.contains('2002_gicsa_explanadapachuca_pi_mkt_FB')]
b = mp[mp.llave_ventas.str.contains('2002_gicsa_explanadapachuca_pi_mkt_FB')]
c = fic[fic.llave_ventas.str.contains('2002_gicsa_explanadapachuca_pi_mkt_FB')] #esta mal escrito la marca

a = mp_fic[mp_fic.llave_ventas.str.contains('2003_gwep_aurum_pi_pfm_SEM')]
b = mp[mp.llave_ventas.str.contains('2003_gwep_aurum_pi_pfm_SEM')]
c = fic[fic.llave_ventas.str.contains('2003_gwep_aurum_pi_pfm_SEM')] #la plataforma no es la misma


#De esta manera el mp ya no cuenta con registros duplicados
cuadrar = mp_fic.groupby(['cliente','cliente_nomenclatura','marca','campaña_nomenclatura','llave_ventas','llave_unica_mp','plataforma',
                          'plataforma_abreviacion','versión','fecha_inicio_plan','fecha_fin_plan','Año-Mes','mes_plan','tipo_presupuesto',
                          'tipo_2','plan_x'], as_index = False).agg({
                                                                      'costo_planeado':'mean',
                                                                      'kpi_planeado':'mean',
                                                                      'serving':'mean',
                                                                      'inversión_plataforma':'mean',
                                                                      'inversión_total':'mean',
                                                                      'inversión_AdOps':'mean',
                                                                      'Operativo_AdOps':'mean',
                                                                      'Serving_AdOps':'mean',
                                                                      'costo_operativo':'mean',
                                                                      'conteo_MP_FIC':'sum',
                                                                      'conteo':'sum'})
                          
#El valor se vuelve unico pero el fic se promedia
b = cuadrar[cuadrar.llave_ventas.str.contains('2003_gicsa_paseointerlomas_pi_mkt_PV')]

duplicados = cuadrar[cuadrar.conteo > 1]

cuadrar = cuadrar.groupby(['plataforma','plataforma_abreviacion'], as_index = False).sum()
cuadrar.sum()

#se le hace esta agrupacion para que no tengamos duplicados erroneos
mp_fic = mp_fic.groupby(['cliente','cliente_nomenclatura','marca','campaña_nomenclatura','llave_ventas','llave_unica_mp','plataforma',
                          'plataforma_abreviacion','versión','fecha_inicio_plan','fecha_fin_plan','Año-Mes','mes_plan','tipo_presupuesto',
                          'tipo_2','plan_x'], as_index = False).agg({
                                                                      'costo_planeado':'mean',
                                                                      'kpi_planeado':'mean',
                                                                      'serving':'mean',
                                                                      'inversión_plataforma':'mean',
                                                                      'inversión_total':'mean',
                                                                      'inversión_AdOps':'mean',
                                                                      'Operativo_AdOps':'mean',
                                                                      'Serving_AdOps':'mean',
                                                                      'costo_operativo':'mean',
                                                                      'conteo_MP_FIC':'sum',
                                                                      'conteo':'sum'})

tmp = mp_fic.groupby(['mes_plan','plataforma'], as_index = False).sum()
                          
#-- Plataformas --#
#Une los archivos de las plataformas que se dejan en las carpetas del dropbox, se pueden unir de forma semanal o mensual (la fecha de referencia será la fecha del reporte).
def Archivos_Plataformas(mes = '2001_Enero', tipo_union = 'Semanal'):
    if tipo_union == 'Semanal':
        Archivos_csv = glob.glob('/home/carlos/Dropbox/ROAS 2020/' + mes + '/Semanal/**/*.csv')
        Archivos_xlsx = glob.glob('/home/carlos/Dropbox/ROAS 2020/' + mes + '/Semanal/**/*.xlsx')
    else:
        Archivos_csv = glob.glob('/home/carlos/Dropbox/ROAS 2020/' + mes + '/Mensual/*.csv')
        Archivos_xlsx = glob.glob('/home/carlos/Dropbox/ROAS 2020/' + mes + '/Mensual/*.xlsx')
    return Archivos_csv, Archivos_xlsx

#Solo es necesario especificar el nombre del Mes de la carpeta y el tipo de union.
archivos_csv_01, archivos_xlsx_01 = Archivos_Plataformas(mes = '2001_Enero', tipo_union = 'Semanal')
archivos_csv_02, archivos_xlsx_02 = Archivos_Plataformas(mes = '2002_Febrero', tipo_union = 'Semanal')
archivos_csv_03, archivos_xlsx_03 = Archivos_Plataformas(mes = '2003_Marzo', tipo_union = 'Semanal')

#Base con la información de los reportes de todas las plataformas
plataformas_01 = Plataformas.Plataformas_tabla(archivos_csv_01, archivos_xlsx_01)
plataformas_02 = Plataformas.Plataformas_tabla(archivos_csv_02, archivos_xlsx_02)
plataformas_03 = Plataformas.Plataformas_tabla(archivos_csv_03, archivos_xlsx_03)

plataformas_01.plataforma.value_counts()
plataformas_02.plataforma.value_counts()
plataformas_03.plataforma.value_counts()

plataformas = pd.concat([plataformas_01,plataformas_02,plataformas_03])
plataformas.mes.value_counts()

del archivos_csv_01, archivos_csv_02, archivos_csv_03, archivos_xlsx_01, archivos_xlsx_02, archivos_xlsx_03, Arch_MP_FIC, Archivos, plataformas_01, plataformas_02, plataformas_03

#a = plataformas_01[plataformas_01.llave_plataformas.str.contains('pachuca')]


#####################################################################################################
#Base master Roas union
#
# Analisis de la union del mp y plataformas, división de casos (intersección, uniones y exclusiones) 
#####################################################################################################

tmp = pd.merge(mp_fic, plataformas, how = 'outer', left_on = 'llave_ventas', right_on = 'llave_plataformas')

tmp['comentario'] = ""

#-Eliminamos filas que no tienen nada en las plataformas
tmp_a = tmp[ (tmp.dinero_gastado != 0) | (tmp.impresiones != 0) | (tmp.conversiones != 0) | (tmp.revenue != 0)]
#-Eliminamos filas que no tienen nada en las plataformas
tmp_b = tmp[ (tmp.dinero_gastado == 0) & (tmp.impresiones == 0) & (tmp.conversiones == 0) & (tmp.revenue == 0)]

#-Es lo que cruza correctamente
tmp_c = tmp_a[ ~(tmp_a.llave_ventas.isnull()) & ~(tmp_a.llave_plataformas.isnull()) ]
tmp_c['comentario'] = "información correcta, que tenemos en el mp y en las plataformas"
#-Lo que debo revisar 
tmp_d = tmp_a[ (tmp_a.llave_ventas.isnull()) | (tmp_a.llave_plataformas.isnull()) ]

#-Tengo en el mp y no las encontre en las plataformas
tmp_d_1 = tmp_d[ tmp_d.llave_plataformas.isnull() ]
 #Son unicas y no todas deben estar en las plataformas
len(tmp_d_1.llave_unica_mp.unique())
 #Dividimos en casos campañas de PV y ~PV
tmp_d_1_1 = tmp_d_1[ ~(tmp_d_1.plataforma_abreviacion.str.contains('PV')) ] #Se tiene que revisar si se encuentra mal la nomenclatura en los reportes
tmp_d_1_2 = tmp_d_1[ (tmp_d_1.plataforma_abreviacion.str.contains('PV')) ] #Se regresará a la base final ya que no contamos con datos de estas plataformas
tmp_d_1_2['comentario'] = "información de provedores no contamos con reportes de plataformas"

#-Tengo en las plataformas y no las encontre en mp
tmp_d_2 = tmp_d[ tmp_d.llave_ventas.isnull() ]
 #Dividimos en casos 20 y ~20
tmp_d_2_1 = tmp_d_2[ (tmp_d_2.llave_plataformas.str.contains('20')) ] #Se tiene que revisar si encuentra mal en el mp
tmp_d_2_2 = tmp_d_2[ ~(tmp_d_2.llave_plataformas.str.contains('20')) ] #Se regresará a la base final ya que son datos buenos (conversiones asistidas, gereraron un gasto)
tmp_d_2_2['comentario'] = "conversiones asistidas campañas que no tengo en el mp"

##########################
#¿Con que me debo quedar?
tmp_union = pd.concat([ tmp_c, tmp_d_1_2, tmp_d_2_2 ])

tmp_union = tmp_union.fillna('')
tmp_union.mes_plan.value_counts()

tmp_union.cliente.value_counts()

########################################
#¿Que formato final debe tener la base?

tmp_union['dias_totales_campaña'] = 0
tmp_union['semana'] = ''
tmp_union['inversión_planeada'] = 0
tmp_union['inversión_mp'] = 0
tmp_union['inversión_diaria'] = 0
tmp_union['ctr'] = 0
tmp_union['llave_analytics'] = tmp_union['llave_ventas']
tmp_union['total_conversiones'] = 0 
tmp_union['total_revenue'] = 0
tmp_union['roas'] = 0 

list(enumerate(tmp_union.keys()))

tmp_union = tmp_union.iloc[:,[0,1,2,4,5,8,13,14,50,11,12,3,6,7,9,10,34,35,51,16,17,18,19,20,21,22,23,24,52,32,33,47,48,49,53,54,55,36,37,38,39,56,40,41,57,42,43,44,45,58,59,60]]

list(enumerate(tmp_union))

FB_t = tmp_union[tmp_union.plataforma_abreviacion.str.contains('FB')]
ADFORM_t = tmp_union[tmp_union.plataforma_abreviacion.str.contains('DSP')]
ADWORDS_t = tmp_union[tmp_union.plataforma_abreviacion.str.contains('SEM')]

#Separamos en version normal
vn_union = tmp_union[~tmp_union.versión.str.contains('VC')]

Escritura_Sheets.Escritura(vn_union , 2, Escribir = 'si', header = True, archivo_sheet = 'Base master Roas')

#Separamos en version cliente
vc_union = tmp_union[tmp_union.versión.str.contains('VC')]

Escritura_Sheets.Escritura(vc_union , 3, Escribir = 'si', header = True, archivo_sheet = 'Base master Roas')

###########################
#Validacion de lo faltante#
###########################

##############################################
#¿Qué debemos revisar sobre la nomenclatura? #

a = tmp_d_2_1.llave_plataformas.str.split("_", 10,expand = True)
a.columns = ["Año-Mes","Cliente","Marca","Tipo-1","Tipo-2","plataforma"]
a['dummy'] = ''
a['comentario'] = "Los tenemos en plataforma, se tiene que revisar si encuentra mal en el mp"
a['Nombre_Campaña'] = tmp_d_2_1.llave_plataformas

b = tmp_d_1_1.llave_ventas.str.split("_", 10,expand = True)
b.columns = ["Año-Mes","Cliente","Marca","Tipo-1","Tipo-2","plataforma","dummy"]
b.fillna('')
b = b.iloc[:,[0,1,2,3,4,5,6]]
b['comentario'] = 'Lo tenemos en el mp, se tiene que revisar si se encuentra mal la nomenclatura en los reportes'
b['Nombre_Campaña'] = tmp_d_1_1.llave_ventas

tmp_revision = pd.concat([a,b]) ; del a,b

tmp_revision['conteo'] = 1
tmp_revision.dummy = tmp_revision.dummy.apply(lambda x : str(x).replace('None',''))

tmp_revision = tmp_revision.groupby(['Año-Mes', 'Cliente', 'Marca', 'Tipo-1', 'Tipo-2', 'plataforma',
                                     'dummy', 'comentario', 'Nombre_Campaña'], as_index = False).count()


#Desglose por cliente
OD = tmp_revision.loc[ tmp_revision.Cliente.str.contains('od', na = False) & ~tmp_revision.Cliente.str.contains('sodexo', na = False)]
RS = tmp_revision.loc[ tmp_revision.Cliente.str.contains('rs', na = False)]
THS = tmp_revision.loc[ tmp_revision.Cliente.str.contains('ths', na = False)]
PETCO = tmp_revision.loc[ tmp_revision.Cliente.str.contains('petco', na = False)]
GICSA = tmp_revision.loc[ tmp_revision.Cliente.str.contains('gicsa', na = False)]
GWEP = tmp_revision.loc[ tmp_revision.Cliente.str.contains('gwep', na = False)]

OD.shape[0] + RS.shape[0] + THS.shape[0] + PETCO.shape[0] + GICSA.shape[0] + GWEP.shape[0]

OTROS = tmp_revision.loc[ ~tmp_revision.Cliente.str.contains('od', na = False) & ~tmp_revision.Cliente.str.contains('rs', na = False) & ~tmp_revision.Cliente.str.contains('sodexo', na = False) & ~tmp_revision.Cliente.str.contains('ths', na = False) &
                  ~tmp_revision.Cliente.str.contains('petco', na = False) & ~tmp_revision.Cliente.str.contains('gicsa', na = False) & ~tmp_revision.Cliente.str.contains('gicsa', na = False) & ~tmp_revision.Cliente.str.contains('gwep', na = False)]

#Escritura de validaciones
Escritura_Sheets.Escritura(OD, hoja = 0, header = 'si', Escribir = 'si', archivo_sheet = 'Validación Nomenclatura Base Roas')
Escritura_Sheets.Escritura(RS, hoja = 1, header = 'si', Escribir = 'si', archivo_sheet = 'Validación Nomenclatura Base Roas')
Escritura_Sheets.Escritura(THS, hoja = 2, header = 'si', Escribir = 'si', archivo_sheet = 'Validación Nomenclatura Base Roas')
Escritura_Sheets.Escritura(PETCO, hoja = 3, header = 'si', Escribir = 'si', archivo_sheet = 'Validación Nomenclatura Base Roas')
Escritura_Sheets.Escritura(GICSA, hoja = 4, header = 'si', Escribir = 'si', archivo_sheet = 'Validación Nomenclatura Base Roas')
Escritura_Sheets.Escritura(GWEP, hoja = 5, header = 'si', Escribir = 'si', archivo_sheet = 'Validación Nomenclatura Base Roas')

Escritura_Sheets.Escritura(OTROS, hoja = 6, header = 'si', Escribir = 'si', archivo_sheet = 'Validación Nomenclatura Base Roas')