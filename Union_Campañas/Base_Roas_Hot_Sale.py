#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 29 11:44:25 2020

@author: carlos

Descripcion: El siguiente script tiene como objetvo centralizar la información del MP, Reportes Plataformas, Google Analytics.

Jerarquía de ejecución:
    - Limpieza MP
    - Union reportes Plataformas
    - Cruze MP/Plataformas, formato Base Master, exportación de versiones y validaciones. 
    - Union de las Bases de Conversiones/Revenue Google Analytics (Faceboock y Google)
    - Cruze información Base Master y Google Analytics con la llave_analytics. (Se asigna el valor de forma manual a la hoja Analytics)
    - Exportación de la Base Master Final

#Nota: La hora Analytics al colocar la información de la llave de forma manual debemos tener cuidado al momento de remplazar dicha info.
    
"""
from datetime import datetime
startTime = datetime.now()

#Paquetes 

import pandas as pd
import os
import glob
import re
import datetime
from datetime import datetime, timedelta 
import seaborn as sns
import matplotlib.pyplot as plt 
pd.set_option('display.float_format', lambda x: '%.2f' % x)

#Definimos la ruta para poder trabajar con los diferentes Scripts de apoyo
os.chdir('/home/carlos/Documentos/3_Adsocial/Marketing/Union_Campañas')
os.listdir()

from librerias import MP_FIC #Une, limpia el Archivo KPIS_2020
from librerias import Plataformas #Une, limpia y les da el mismo formato a los Reportes Semanales de las Plataformas.
from librerias import Escritura_Sheets #Escribe la información en Google Sheets
from librerias import Analytics_conversiones #Conversiones asistidas y Directas de la Base Roas

#####################################################
#--------PRIMERO TRABAJAMOS CON ARCHIVO KPIS--------#
#####################################################
#Aplicando la función MP_FIC_tabla() creada para mejorar la legibilidad del código.

os.chdir('/home/carlos/Dropbox/ROAS 2020')
Archivos = os.listdir()

#-- MP_FIC (KPI) --#
#La funcion MP_FIC_tabla que vive en el script MP_FIC nos ayuda a procesar el MP y FIC, descargado del google drive KPIS 2020.
Arch_MP_FIC = [x for x in Archivos if "Hot Sale - KPIS 2020 - AdSocial.xlsx" in x]

#La función regresa una tupla con mp_fic, mp, fic
tablas_mp_fic =  MP_FIC.MP_FIC_tabla(Arch_MP_FIC)
#Base MP y FIC
mp_fic = tablas_mp_fic[0]

del Arch_MP_FIC, Archivos

###############################################
#--------UNION INFORMACIÓN PLATAFORMAS--------#
###############################################
#¿Como unimos toda la información de las Plataformas?,
#Si la Carpeta donde colocamos los reportes tiene el formato adecuado de Carpetas funcionará correctamente.
#
#Ejemplo: 2001_Enero -> Semanal -> 1:01:2020 al 8:01:2020 (d:mm:yyyy)

#Archivos
Archivos_csv = glob.glob('/home/carlos/Dropbox/ROAS 2020/2005_Mayo/Semanal/Hot Sale/**/*.csv')
Archivos_xlsx = glob.glob('/home/carlos/Dropbox/ROAS 2020/2005_Mayo/Semanal/Hot Sale/**/*.xlsx')

#Unión, Función que extraer el nombre de los Archivos que tenemos en las carpetas de los reportes
plataformas = Plataformas.Plataformas_tabla(Archivos_csv, Archivos_xlsx)
plataformas.plataforma.value_counts()

######################################################################
#--------CREACION BASE MASTER (UNION KPIS 2020 Y PLATAFORMAS)--------#
######################################################################
#   Es la Unión de la información de MP y Plataformas.
#   Se realizo un analisis de la union del mp y plataformas, se realizo un outer join.
#   El cual permite desglosar paso por paso el cruce de información, división de casos (intersección, uniones y exclusiones) .

#--Toda la información--#
tmp = pd.merge(mp_fic, plataformas, how = 'outer', left_on = 'llave_ventas', right_on = 'llave_plataformas')

#Validación individual de los cruzes de las plataformas
tmp = tmp.rename(columns = {'plataforma_x':'plataforma'})
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
tmp_d_1_1 = tmp_d_1[ ~(tmp_d_1.plataforma.str.contains('pv')) ] #Se tiene que revisar si se encuentra mal la nomenclatura en los reportes
tmp_d_1_2 = tmp_d_1[ (tmp_d_1.plataforma.str.contains('pv')) ] #Se regresará a la base final ya que no contamos con datos de estas plataformas
tmp_d_1_2['comentario'] = "información de provedores no contamos con reportes de plataformas"

#-Tengo en las plataformas y no las encontre en mp
tmp_d_2 = tmp_d[ tmp_d.llave_ventas.isnull() ]
#Esta informacion como no viene en el mp le tengo que generar ciertas columnas.
tmp_d_2['cuenta'] = tmp_d_2['cuenta'].str.lower()
tmp_d_2.loc[tmp_d_2['cuenta'].str.contains('gicsa'), 'cliente'] = 'GICSA'
tmp_d_2.loc[tmp_d_2['cuenta'].str.contains('gwep'), 'cliente'] = 'GWEP'
tmp_d_2.loc[tmp_d_2['cuenta'].str.contains('office'), 'cliente'] = 'Office Depot'
tmp_d_2.loc[tmp_d_2['cuenta'].str.contains('petco'), 'cliente'] = 'Petco'
tmp_d_2.loc[tmp_d_2['cuenta'].str.contains('radio'), 'cliente'] = 'RadioShack'
tmp_d_2.loc[tmp_d_2['cuenta'].str.contains('sodexo'), 'cliente'] = 'Sodexo'
tmp_d_2.loc[tmp_d_2['cuenta'].str.contains('tequila'), 'cliente'] = 'Tequila 1921'
tmp_d_2.loc[tmp_d_2['cuenta'].str.contains('home'), 'cliente'] = 'The Home Store'

tmp_d_2['llave_ventas'] = tmp_d_2['llave_plataformas']

tmp_d_2['Año-Mes'] = "20" + tmp_d_2['mes'] 

tmp_d_2['plataforma_x'] = tmp_d_2['plataforma_y']

tmp_d_2.loc[tmp_d_2['plataforma_y'].str.contains('Adform'), 'plataforma'] = 'dsp'
tmp_d_2.loc[tmp_d_2['plataforma_y'].str.contains('Adwords'), 'plataforma'] = 'sem'
tmp_d_2.loc[tmp_d_2['plataforma_y'].str.contains('Facebook'), 'plataforma'] = 'fb'

#Dividimos en casos 20 y ~20
tmp_d_2_1 = tmp_d_2[ (tmp_d_2.llave_plataformas.str.contains('20')) ] #Se tiene que revisar si encuentra mal en el mp
tmp_d_2_2 = tmp_d_2[ ~(tmp_d_2.llave_plataformas.str.contains('20')) ] #Se regresará a la base final ya que son datos buenos (conversiones asistidas, gereraron un gasto)
tmp_d_2_2['versión'] = 'No aplica'

tmp_d_2_2['comentario'] = "conversiones asistidas campañas que no tengo en el mp"

#--¿Con que me debo quedar?--#
#El objetivo actual es tener un monitoreo de las campañas.
#Por lo tanto solo me quedo con campañas que se encuentran en el MP y en Plataformas.
tmp_union = pd.concat([ tmp_c]) 

tmp_union.comentario.value_counts()
tmp_union = tmp_union.fillna(0)
tmp_union['conteo_x'] = 1

list(enumerate(tmp_union.keys()))

#Los valores unicos deben ser de información correcta, que tenemos en el mp y en las plataformasa
tmp_union.plataforma.value_counts()
validacion = tmp_union.groupby(['llave_unica_mp', 'archivo']).count()

#Limpieza para variables de entorno que no usaremos despues
#del tmp, tmp_a, tmp_b, tmp_c, tmp_d, tmp_d_1, tmp_d_1_1, tmp_d_1_2, tmp_d_2, tmp_d_2_1, tmp_d_2_2

#--¿Que formato final debe tener la base?--#
#
# 1 - Se crea la llave_analytics para poder cruzar con la información de Google Analytics.
# 2 - Se transforma algunas columnas con cierta nomenclatura.
# 3 - Se calcula el dinero Gastado Adform.
# 4 - Se le coloca el número de Semana apartir de la Fechas de los Reportes.
# 5 - Métricas que se calculan teniendo toda la información unida, ejemplo: 
#       días semanales, dias mensuales, inversión diaria, inversión semanal.

#Llave Analytics
tmp_union['llave_analytics'] = tmp_union['llave_ventas'] + "_" + tmp_union.inicio_reporte.apply(lambda x : str(x).split(" ")[0])
tmp_union['total_conversiones'] = 0 
tmp_union['total_revenue'] = 0

#Columnas con cierta nomenclatura
tmp_union.loc[tmp_union['plataforma'].str.contains('fb'), 'plataforma'] = 'Facebook'
tmp_union.loc[tmp_union['plataforma'].str.contains('sem'), 'plataforma'] = 'Google Search'
tmp_union.loc[tmp_union['plataforma'].str.contains('gdn'), 'plataforma'] = 'Google Display'
tmp_union.loc[tmp_union['plataforma'].str.contains('ytb'), 'plataforma'] = 'Google YouTube'
tmp_union.loc[tmp_union['plataforma'].str.contains('dsp'), 'plataforma'] = 'Programmatic'

#Dinero gastado Adform
tmp_union.loc[tmp_union['plataforma'] == 'Programmatic', 'dinero_gastado'] = (tmp_union['costo_planeado'] * tmp_union['impresiones'])/1000
tmp_union.loc[ (tmp_union['dinero_gastado'] > tmp_union['inversión_total']) & (tmp_union['plataforma'] == 'Programmatic') , 'dinero_gastado' ] = tmp_union['inversión_total']

#Colocación de la Semana
tmp_union['semana'] = ''
d = tmp_union.inicio_reporte.unique()
d = pd.DataFrame( d[d != 0]).T
d.columns = ['inicio_reporte']
d = d.sort_values('inicio_reporte').reset_index()
d['index'] = d.index
d.columns = ['semana','inicio_reporte']
d.semana = d.semana + 1
d.semana = d.semana.astype('str')
d['semana'] = d.semana

for i in range(0,d.semana.shape[0]):
    tmp_union.loc[tmp_union.inicio_reporte == d.inicio_reporte[i], 'semana'] = d.semana[i]

#Metricas semanales
tmp_union = tmp_union[tmp_union.fin_campaña_reporte != 0]

tmp_union['dias_mes'] = ((tmp_union.fecha_fin_plan - tmp_union.fecha_inicio_plan) + timedelta(days=1)).dt.days
tmp_union['dias_semana'] = ((tmp_union.fin_campaña_reporte - tmp_union.inicio_campaña_reporte) + timedelta(days=1)).dt.days

tmp_union.loc[tmp_union.dias_semana < 0, 'dias_semana'] = 0

tmp_union['kpi_planeado_diario'] = round(tmp_union.kpi_planeado / tmp_union.dias_mes)
tmp_union['kpi_planeado_semanal'] = round(tmp_union.kpi_planeado_diario * tmp_union.dias_semana)

tmp_union['inversion_plataforma_diaria'] = round(tmp_union.inversión_plataforma / tmp_union.dias_mes)
tmp_union['inversion_plataforma_semanal'] = round(tmp_union.inversion_plataforma_diaria * tmp_union.dias_semana)

tmp_union['inversion_AdOps_diaria'] = round(tmp_union.Operativo_AdOps / tmp_union.dias_mes)
tmp_union['inversion_AdOps_semanal'] = round(tmp_union.inversion_AdOps_diaria * tmp_union.dias_semana)

#validamos el formato
list(enumerate(tmp_union.keys()))

#columnas semanal
tmp_union = tmp_union.loc[:,['cliente_nomenclatura','llave_ventas',	'llave_unica_mp', 'versión',
                             'tipo_presupuesto', 'tipo_2', 'comentario', 'Año-Mes', 'mes_plan', 'campaña_nomenclatura',
                             'plataforma', 'fecha_inicio_plan', 'fecha_fin_plan', 'inicio_campaña',	'fin_campaña',
                             'costo_planeado', 'kpi_planeado', 'serving', 'inversión_plataforma', 'inversión_total',
                             'inversión_AdOps', 'Operativo_AdOps','Serving_AdOps', 'costo_operativo',
                             'semana','dias_mes', 'dias_semana','kpi_planeado_diario','kpi_planeado_semanal',
                             'inversion_plataforma_diaria','inversion_plataforma_semanal','inversion_AdOps_diaria','inversion_AdOps_semanal',
                             'inicio_reporte', 'fin_reporte', 'inicio_campaña_reporte','fin_campaña_reporte', 'divisa',
                             'dinero_gastado', 'impresiones', 'clics', 'conversiones', 'revenue','llave_analytics',
                             'conversiones_directas', 'conversiones_asistidas', 'revenue_directo', 'revenue_asistido',
                             'total_conversiones', 'total_revenue']]

tmp_union.dinero_gastado = round(tmp_union.dinero_gastado)

#Por si queremos analizar la información desde el csv.
tmp_union.to_csv("/home/carlos/Documentos/3_Adsocial/Marketing/Union_Campañas/base_roas_semanal.csv")

###################################
#--¿Donde vive la información?--#
###################################
#Con ayuda de Escritura_Sheets podemos colocar la información en Google Sheets. (Base master Roas)
#Se separa la información de Versión Normal y Versión Cliente.
#Antes de escribir la información revisemos que el numero de Hojas es el Correcto comenzando a contar desde 0.

#Validamos el día que agregaremos
semanal = Escritura_Sheets.archivos_finales(sheets = 'Base Master Roas Hot Sale', hoja = 3)
semanal.groupby(['inicio_campaña_reporte','versión'], as_index = False).count().loc[:,['inicio_campaña_reporte','versión','ultima_actualizacion']]

semanal = Escritura_Sheets.archivos_finales(sheets = 'Base Master Roas Hot Sale', hoja = 4)
semanal.groupby(['inicio_campaña_reporte','versión'], as_index = False).count().loc[:,['inicio_campaña_reporte','versión','ultima_actualizacion']]

#Vemos que día nos hace falta
tmp_union = tmp_union[tmp_union.inicio_campaña_reporte == '2020-05-28'] 

#Separamos en version normal
vn_union = tmp_union[~tmp_union.versión.str.contains('VC')]
Escritura_Sheets.Escritura(vn_union ,
                           hoja = 3,
                           Escribir = 'si',
                           header = True,
                           archivo_sheet = 'test')

#Separamos en version cliente
vc_union = tmp_union[tmp_union.versión.str.contains('VC')]
Escritura_Sheets.Escritura(vc_union ,
                           hoja = 4,
                           Escribir = 'si',
                           header = True,
                           archivo_sheet = 'test')

#--¿Toda la información cruzo?--#
#
# No, se debe revisar que es lo que no esta cruzando y ¿por que?
# Las validaciones se realizan por Cliente
# Se escriben en Sheets (Validaciones Nomenclatura Base Roas)
# Una ves que se corrija volvemos a correr el código.

#¿Qué debemos revisar sobre la nomenclatura? #
a = tmp_d_2_1.llave_plataformas.str.split("_", 10,expand = True)
a.columns = ["Año-Mes","Cliente","Marca","Tipo-1","Tipo-2","plataforma"]
a['dummy'] = ''
a['comentario'] = "Los tenemos en plataforma, se tiene que revisar si encuentra mal en el mp"
a['Nombre_Campaña'] = tmp_d_2_1.llave_plataformas

b = tmp_d_1_1.llave_ventas.str.split("_", 5,expand = True)
b.columns = ["Año-Mes","Cliente","Marca","Tipo-1","Tipo-2","plataforma"]
b.fillna('')
b = b.iloc[:,[0,1,2,3,4,5]]
b['comentario'] = 'Lo tenemos en el mp, se tiene que revisar si se encuentra mal la nomenclatura en los reportes'
b['Nombre_Campaña'] = tmp_d_1_1.llave_ventas

tmp_revision = pd.concat([a,b]) ; del a,b

tmp_revision['conteo'] = 1
tmp_revision.dummy = tmp_revision.dummy.apply(lambda x : str(x).replace('None',''))

tmp_revision = tmp_revision.groupby(['Año-Mes', 'Cliente', 'Marca', 'Tipo-1', 'Tipo-2', 'plataforma',
                                     'dummy', 'comentario', 'Nombre_Campaña'], as_index = False).count()

#Hot Sale
Escritura_Sheets.Escritura(tmp_revision, hoja = 0, header = 'si', Escribir = 'si', archivo_sheet = 'test')

###################################################################################
#--UNION DE LAS BASES DE CONVERSIONES ASISTIDAS/DIRECTAS PARA CRUZAR BASE MASTER--#
###################################################################################

#Función que vive en Analytics_conversiones
analytics = Analytics_conversiones.Analytics(mes = 'Hot Sale')

analytics = analytics[(analytics.conversiones != 0) & (analytics.revenue != 0)]

analytics = analytics.fillna('')

analytics.inicio_reporte = pd.to_datetime(analytics.inicio_reporte, format = "%Y-%m-%d")
analytics.fin_reporte = pd.to_datetime(analytics.fin_reporte, format = "%Y-%m-%d")

tmp = analytics.groupby(['cliente','Año-Mes','plataforma_abreviacion','inicio_reporte','fin_reporte','tipo_conversion','fuente_medio','Nombre_Campaña','archivo'],
                              as_index = False).count()

#vemos que información nos hace falta con lo que enemos arriba y la seleccionamos para pegarla
tmp = analytics.groupby(['inicio_reporte'],as_index = False).count() ; tmp

analytics = analytics[analytics.inicio_reporte == '2020-05-28']

analytics.to_csv("/home/carlos/Documentos/3_Adsocial/Marketing/Analytics/analytics_union.csv")

#Escritura Google Sheets#

Escritura_Sheets.Escritura(analytics ,
                           hoja = 2,
                           Escribir = 'si',
                           header = True,
                           archivo_sheet = 'test')

print(datetime.now() - startTime)

################################################
#--CRUZE CON INFORMACION DE GOOGLE ANALYTICS--##
################################################

def Formato_numerico(Base, Columna):
        Base.loc[:,Columna] = Base.loc[:,Columna].apply(lambda x : str(x).replace('$',''))
        Base.loc[:,Columna] = Base.loc[:,Columna].apply(lambda x : str(x).replace(',',''))
        Base.loc[:,Columna] = Base.loc[:,Columna].apply(lambda x : str(x).strip())
        Base.loc[:,Columna] = Base.loc[:,Columna].apply(lambda x : str(x).replace('-','0'))
        Base.loc[:,Columna] = Base.loc[:,Columna].astype('float')
        Base.loc[:,Columna] = round(Base.loc[:,Columna],2)
        return Base.loc[:,Columna]

#Importación de las bases
semanal = Escritura_Sheets.archivos_finales(sheets = 'Base Master Roas Hot Sale', hoja = 3)

analytics_semanal = Escritura_Sheets.archivos_finales(sheets = 'Base Master Roas Hot Sale', hoja = 2)

#Transformación de los datos de analytics
analytics_semanal = analytics_semanal[~analytics_semanal.plataforma_abreviacion.str.contains('DSP')] #Dsp ya cuenta con sus conversiones asistidas
    
analytics_semanal['revenue'] = Formato_numerico(analytics_semanal, 'revenue')
analytics_semanal['conversiones'] = Formato_numerico(analytics_semanal, 'conversiones')

analytics_semanal = analytics_semanal.loc[:,['tipo_conversion','llave_analytics','conversiones','revenue']]
analytics_semanal = analytics_semanal.groupby(['llave_analytics',
                                               'tipo_conversion'], as_index = False).sum()

analytics_semanal = analytics_semanal.pivot(index = 'llave_analytics',
                                            columns = 'tipo_conversion')

analytics_semanal.columns = ['conversiones_asistidas',
                             'conversiones_directas',
                             'revenue_asistido',
                             'revenue_directo']

analytics_semanal = analytics_semanal.fillna(0).reset_index()

semanal_DSP = semanal[semanal.plataforma.str.contains('Programmatic')]

#Cruze de la información semanal con analytics Facebook y Google
#Debo quitar los que no cruzen, bien.
semanal_FB_GO = semanal[~semanal.plataforma.str.contains('Programmatic')].drop(['conversiones_directas',
                                                                                          'conversiones_asistidas',
                                                                                          'revenue_directo',
                                                                                          'revenue_asistido'], axis = 1).fillna(0)

semanal_FB_GO = pd.merge(semanal_FB_GO, 
                         analytics_semanal,
                         how = 'outer',
                         on = 'llave_analytics')

tmp = semanal_FB_GO.loc[:,['cliente_nomenclatura','llave_ventas',	'llave_unica_mp', 'versión',
                           'tipo_presupuesto', 'tipo_2', 'comentario', 'Año-Mes', 'mes_plan', 'campaña_nomenclatura',
                           'plataforma', 'fecha_inicio_plan', 'fecha_fin_plan', 'inicio_campaña',	'fin_campaña',
                           'costo_planeado', 'kpi_planeado', 'serving', 'inversión_plataforma', 'inversión_total',
                           'inversión_AdOps', 'Operativo_AdOps','Serving_AdOps', 'costo_operativo',
                           'semana','dias_mes', 'dias_semana','kpi_planeado_diario','kpi_planeado_semanal',
                           'inversion_total_diaria','inversion_total_semanal','inversion_AdOps_diaria','inversion_AdOps_semanal',
                           'inicio_reporte', 'fin_reporte', 'inicio_campaña_reporte','fin_campaña_reporte', 'divisa',
                           'dinero_gastado', 'impresiones', 'clics', 'conversiones', 'revenue','llave_analytics',
                           'conversiones_directas', 'conversiones_asistidas', 'revenue_directo', 'revenue_asistido',
                           'total_conversiones', 'total_revenue']]

semanal_FB_GO = semanal_FB_GO.iloc[:-2]
                                                            
semanal_tmp = pd.concat([semanal_DSP, semanal_FB_GO], axis = 0)

semanal_tmp = semanal_tmp.loc[:,['cliente_nomenclatura','llave_ventas', 'llave_unica_mp', 'versión',
                   'tipo_presupuesto', 'tipo_2', 'comentario', 'Año-Mes', 'mes_plan', 'campaña_nomenclatura',
                   'plataforma', 'fecha_inicio_plan', 'fecha_fin_plan', 'inicio_campaña',	'fin_campaña',
                   'costo_planeado', 'kpi_planeado', 'serving', 'inversión_plataforma', 'inversión_total',
                   'inversión_AdOps', 'Operativo_AdOps','Serving_AdOps', 'costo_operativo',
                   'semana','dias_mes', 'dias_semana','kpi_planeado_diario','kpi_planeado_semanal',
                   'inversion_total_diaria','inversion_total_semanal','inversion_AdOps_diaria','inversion_AdOps_semanal',
                   'inicio_reporte', 'fin_reporte', 'inicio_campaña_reporte','fin_campaña_reporte', 'divisa',
                   'dinero_gastado', 'impresiones', 'clics', 'conversiones', 'revenue','llave_analytics',
                   'conversiones_directas', 'conversiones_asistidas', 'revenue_directo', 'revenue_asistido',
                   'total_conversiones', 'total_revenue']]

Escritura_Sheets.Escritura(semanal_tmp , 3, Escribir = 'si', header = True, archivo_sheet = 'Base Master Roas Hot Sale')

