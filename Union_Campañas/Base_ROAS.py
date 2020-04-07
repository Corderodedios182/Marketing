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
Arch_MP_FIC = [x for x in Archivos if "KPI" in x]
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

a = mp_fic[(mp_fic.cliente == 'Petco') & (mp_fic.marca == 'Petco') & (mp_fic.mes_plan == 'Marzo') & (mp_fic.versión == 'V1') & (mp_fic.plataforma == 'Facebook')]

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

del archivos_csv_01, archivos_csv_02, archivos_xlsx_01, archivos_xlsx_02, Arch_MP_FIC, Archivos

#a = plataformas_01[plataformas_01.llave_plataformas.str.contains('pachuca')]

##############
#Base Master
#Aun se están haciendo pruebas para trabajar cada mes por separado, hacer una función que una todo dependiendo del mes#
##############
#plt
#Enero
mp_plt_01 = pd.merge(mp_fic, plataformas_01, how = 'left', left_on = 'llave_ventas', right_on = 'llave_plataformas')

mp_plt_01['mes_cruze'] = 'Enero'

bien_01 = mp_plt_01[(mp_plt_01.mes_plan == 'Enero') & ~(mp_plt_01.plataforma_y.isnull())]
mal_01 = mp_plt_01[(mp_plt_01.mes_plan == 'Enero') & (mp_plt_01.plataforma_y.isnull())]

#Los que no cruzaron de enero
mp_plt_01.mes_plan.value_counts()

b = mp_plt_01[mp_plt_01.llave_ventas.str.contains('pachuca')]
#'2001_GICSA_ExplanadaPachuca_PI_MKT_SEM_TRF' #Revisar si es correcto que este en 2 reportes

#Febrero
mp_plt_02 = pd.merge(mp_fic, plataformas_02, how = 'left', left_on = 'llave_ventas', right_on = 'llave_plataformas')
mp_plt_02['mes_cruze'] = 'Febrero'

mp_plt_02.mes_plan.value_counts()

bien_02 = mp_plt_02[~mp_plt_02.plataforma_y.isnull()]
mal_02 = mp_plt_02[(mp_plt_02.mes_plan == 'Febrero') & (mp_plt_02.plataforma_y.isnull())]

c = mp_plt_02[mp_plt_02.llave_ventas.str.contains('pachuca')]

#Marzo
mp_plt_03 = pd.merge(mp_fic, plataformas_03, how = 'left', left_on = 'llave_ventas', right_on = 'llave_plataformas')
mp_plt_03['mes_cruze'] = 'Marzo'

mp_plt_03.mes_plan.value_counts()

bien_03 = mp_plt_03[~mp_plt_03.plataforma_y.isnull()]
mal_03 = mp_plt_03[(mp_plt_03.mes_plan == 'Marzo') & (mp_plt_03.plataforma_y.isnull())]

d = mp_plt_03[mp_plt_03.llave_ventas.str.contains('pachuca')]

union = pd.concat([bien_01, bien_02,bien_03])

union.mes_cruze.value_counts()

union = union.fillna('')

FB = union[union.plataforma_abreviacion.str.contains('FB')]
ADFORM = union[union.plataforma_abreviacion.str.contains('DSP')]
ADWORDS = union[union.plataforma_abreviacion.str.contains('SEM')]

a = ADWORDS[ADWORDS.llave_ventas.str.contains('pachuca')]

union[union.cliente.str.contains('Depot')]
union.cliente.value_counts()

union['dias_totales_campaña'] = 0
union['semana'] = ''
union['inversión_planeada'] = 0
union['inversión_mp'] = 0
union['inversión_diaria'] = 0
union['ctr'] = 0
union['llave_analytics'] = union['llave_ventas']
union['total_conversiones'] = 0 
union['total_revenue'] = 0
union['roas'] = 0 

union = union.iloc[:,[0,1,2,4,5,8,13,14,50,11,3,6,7,9,10,34,35,51,16,17,18,19,20,21,22,23,24,52,32,33,47,48,49,53,54,55,36,37,38,39,56,40,41,57,42,43,44,45,58,59,60]]

list(enumerate(union))

#Separamos en version normal
vn_union = union[~union.versión.str.contains('VC')]

Escritura_Sheets.Escritura(vn_union , 2, Escribir = 'si', header = True, archivo_sheet = 'Base master Roas')

#Separamos en version cliente
vc_union = union[union.versión.str.contains('VC')]

Escritura_Sheets.Escritura(vc_union , 3, Escribir = 'si', header = True, archivo_sheet = 'Base master Roas')

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
Escritura_Sheets.Escritura(PETCO, 15, header = True, Escribir = 'no')tmp = bien_01.groupby(['cliente','marca','mes_plan','versión','plataforma_x'], as_index = False).agg({
                                                                                                'costo_planeado':'mean',
                                                                                                'kpi_planeado':'mean',
                                                                                                'serving':'mean',
                                                                                                'inversión_plataforma':'mean',
                                                                                                'inversión_total':'mean'})

Escritura_Sheets.Escritura(GICSA, 16, header = True, Escribir = 'no')
Escritura_Sheets.Escritura(GWEP, 17, header = True, Escribir = 'no')
Escritura_Sheets.Escritura(OTROS, 18, header = True, Escribir = 'no')

#Validaciones del momento (borrar)
a = union[union.llave_plataformas.str.contains('2002_odcam')]

tmp = union[union.mes_cruze == 'Febrero']


#Validando mp y fic cifras
bien_01.keys()

tmp_t = bien_01[(bien_01.cliente == 'GICSA') & (bien_01.marca == 'Forum Cuernavaca')]


tmp_c = tmp[tmp.cliente == 'The Home Store']

tmp_t = tmp.groupby('cliente').sum()

tmp.sum()

tmp.plataforma_x.value_counts()

#
Escritura_Sheets.archivos_finales()
