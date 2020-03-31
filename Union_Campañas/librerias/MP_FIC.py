#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 13:14:05 2020

@author: carlos

Descripción: Este script contiene la función MP_FIC_tabla la cual limpia el archivo de KPIS de Pepe
y une el MP (planes clientes) y FIC (planes internos).

Aun se deben hacer cambios para que escriba las validaciones:
    Duplicados
    Faltantes FIC

"""
#Paqueterías
import os
import pandas as pd
from librerias import Escritura_Sheets

pd.set_option('display.float_format', lambda x: '%.5f' % x)

#En caso de querer agregar nuevas validaciones a alguna plataforma corremos por línea
#Y nos traemos los archivos que queremos trabajar
# Aquí descargo el nuevo archivo de KPIS
os.chdir('/home/carlos/Dropbox/ROAS 2020')
Archivos = os.listdir()

#-- MP_FIC (KPI) --#
Arch_MP_FIC = [x for x in Archivos if "KPI" in x]

#################################################################
#Importación de las bases
#   -Ver el nombre de la campaña por rmnt o pi (caso especial)
#
#################################################################

def MP_FIC_tabla(Arch_MP_FIC):
    
    """limpia el archivo de KPIS de Pepe y une el MP (planes clientes) y FIC (planes internos),
        - le da formato de fechas, formato de numeros, formato en la llave (añomes_cliente_campaña_presupuesto_tipo_plataforma)
        - cruza el mp y fic
        - realiza agrupaciones del mp y fic, ya que la llave no es unica por que tenemos distintos formatos por campaña.
    
    :Arch_MP_FIC: nombre del archivo kpis 2020
    :return: La base mp_fic
    
    >>> MP_FIC_tabla(Arch_MP_FIC)
        MP_FIC
    """
    
    #MP Son unicos
    MP = pd.read_excel(Arch_MP_FIC[0], sheet_name = 'KPIS MP 2020', skiprows = 2)
    MP = MP.fillna('')
    MP.loc[:,'NOMENCLATURA'] = MP.loc[:,'NOMENCLATURA'].str.lower()
    MP['Archivo'] = Arch_MP_FIC[0] 

    #Validaciones MP
    #MP.shape[0] - MP[MP.Versión.str.contains('VC')].shape[0]

    #Filtro sobre el MP 
    #MP = MP[~MP['Versión'].str.contains('VC')]

    #FIC
    FIC = pd.read_excel(Arch_MP_FIC[0], sheet_name = 'KPIS FIC 2020', skiprows = 2)
    FIC = FIC.fillna('')
    FIC.loc[:,'NOMENCLATURA'] = FIC.loc[:,'NOMENCLATURA'].str.lower()
    FIC['Archivo'] = Arch_MP_FIC[0] 

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
    #Limpieza fechas
    MP.loc[:,'Inicio'] = Formato_Fechas(MP, 'Inicio')
    MP.loc[:,'Fin'] = Formato_Fechas(MP, 'Fin')
    
    FIC.loc[:,'Inicio'] = Formato_Fechas(FIC, 'Inicio')
    FIC.loc[:,'Fin'] = Formato_Fechas(FIC, 'Fin')
    #Limpieza columnas numericas
    MP.loc[:,'Costo Planeado'] = Formato_numerico(MP, 'Costo Planeado')
    MP.loc[:,'KPI Planeado'] = Formato_numerico(MP, 'KPI Planeado')
    MP.loc[:,'Serving'] = Formato_numerico(MP, 'Serving')
    MP.loc[:,'Inversión Plataforma'] = Formato_numerico(MP, 'Inversión Plataforma')
    MP.loc[:,'Inversión Total'] = Formato_numerico(MP, 'Inversión Total')

    FIC.loc[:,'Inversión AdOps'] = Formato_numerico(FIC, 'Inversión AdOps')
    FIC.loc[:,'Operativo AdOps'] = Formato_numerico(FIC, 'Operativo AdOps')
    FIC.loc[:,'Serving AdOps'] = Formato_numerico(FIC, 'Serving AdOps')
    FIC.loc[:,'Costo Operativo'] = Formato_numerico(FIC, 'Costo Operativo')
    
    #Para poder trabajar mejor con la nomeclatura, le agregamos su plataforma para cruzar con la información de plataformas
    MP['Plt'] = MP.loc[:,'Plataforma']
    
    MP.loc[MP['Plataforma'].str.contains('Instagram') , 'Plt'] = 'IG'
    MP.loc[MP['Plataforma'].str.contains('Facebook') , 'Plt'] = 'FB'
    MP.loc[MP['Plataforma'].str.contains('Facebook / Instagram') , 'Plt'] = 'FB'
    MP.loc[MP['Plataforma'].str.contains('Google') , 'Plt'] = 'SEM'
    MP.loc[(MP['Plataforma'].str.contains('Programmatic')) | (MP['Plataforma'].str.contains('Display'))  , 'Plt'] = 'DSP'
    MP.loc[(MP['Plataforma'].str.contains('Waze')) | (MP['Plataforma'].str.contains('AdsMovil')) , 'Plt'] = 'PV'
    
    FIC.loc[FIC['Plataforma'].str.contains('Instagram') , 'Plt'] = 'IG'
    FIC.loc[FIC['Plataforma'].str.contains('Facebook') , 'Plt'] = 'FB'
    FIC.loc[FIC['Plataforma'].str.contains('Facebook / Instagram') , 'Plt'] = 'FB'
    FIC.loc[FIC['Plataforma'].str.contains('Google') , 'Plt'] = 'SEM'
    FIC.loc[(FIC['Plataforma'].str.contains('Programmatic')) | (FIC['Plataforma'].str.contains('Display'))  , 'Plt'] = 'DSP'
    FIC.loc[(FIC['Plataforma'].str.contains('Waze')) | (FIC['Plataforma'].str.contains('AdsMovil')) , 'Plt'] = 'PV'
    
    MP['llave_ventas'] = MP.loc[:,'NOMENCLATURA'] + str("_") + MP['Plt']
    MP["llave_ventas"].str.strip()
    
    FIC['llave_ventas'] = FIC.loc[:,'NOMENCLATURA'] + str("_") + FIC['Plt']
    FIC["llave_ventas"].str.strip()

    MP = MP.loc[:, ('Archivo','NOMENCLATURA','llave_ventas','CLIENTE','MARCA','CAMPAÑA','Mes','Versión','Plataforma','Plt','Formato','Inicio','Fin','TDC','Objetivo','Costo Planeado','KPI Planeado','Serving','Inversión Plataforma','Inversión Total')]
    MP_Duplicados = MP.loc[:, ('Archivo','NOMENCLATURA','llave_ventas','CLIENTE','MARCA','CAMPAÑA','Mes','Versión','Plataforma','Plt','Formato','Inicio','Fin','TDC','Objetivo','Costo Planeado','KPI Planeado','Serving','Inversión Plataforma','Inversión Total')]
    FIC = FIC.loc[:, ('Archivo','NOMENCLATURA','llave_ventas','CLIENTE','MARCA','CAMPAÑA','Mes','Versión','Plataforma','Plt','Formato','Inicio','Fin','TDC','Objetivo','Inversión AdOps','Operativo AdOps', 'Serving AdOps','Costo Operativo')]
    FIC_Duplicados = FIC.loc[:, ('Archivo','NOMENCLATURA','llave_ventas','CLIENTE','MARCA','CAMPAÑA','Mes','Versión','Plataforma','Plt','Formato','Inicio','Fin','TDC','Objetivo','Costo Planeado','KPI Planeado','Serving','Inversión Plataforma','Inversión Total')]
    #Campañas unicas
    MP = MP.groupby(['CLIENTE','MARCA','llave_ventas','Plt','Plataforma','Versión','Inicio','Fin','Mes'], as_index = False).agg(
                                                                               {'Costo Planeado':'mean',
                                                                               'KPI Planeado':'sum',
                                                                               'Serving':'sum',
                                                                               'Inversión Plataforma':'sum',
                                                                               'Inversión Total':'sum',
                                                                               'NOMENCLATURA':'count'})
    MP['Plan'] = 'MP'
    #Se tienen estos duplicados en el MP soló es necesario eliminarlos o ajustarlos, 
    #Los duplicados pueden existir por el nombre de la campaña es distinto pero la nomeclatura es la misma
    MP_Duplicados = MP_Duplicados[MP_Duplicados.llave_ventas.isin(MP[MP.NOMENCLATURA > 1].llave_ventas)]
    MP_Duplicados = MP_Duplicados.sort_values(['llave_ventas'])

    #Campañas unicas
    FIC_1 = FIC.groupby(['CLIENTE','MARCA','llave_ventas','Plt','Plataforma','Versión','Inicio','Fin','Mes'], as_index = False).sum()
    .agg({'Inversión AdOps':'sum',
                                                                               'Operativo AdOps':'sum',
                                                                               'Serving AdOps':'sum',
                                                                               'Costo Operativo':'mean',
                                                                               'NOMENCLATURA':'count'})
    FIC['Plan'] = 'FIC'
    #Se tienen estos duplicados en el FIC soló es necesario eliminarlos o ajustarlos
    FIC_Duplicados = FIC_Duplicados[FIC_Duplicados.llave_ventas.isin(FIC[FIC.NOMENCLATURA > 1].llave_ventas)]
    FIC_Duplicados = FIC_Duplicados.sort_values(['llave_ventas'])

    
    #Importación google sheets
    Escritura_Sheets.Escritura(MP_Duplicados, 0, header = True, Escribir = 'no')
    Escritura_Sheets.Escritura(FIC_Duplicados, 1, header = True, Escribir = 'no')

    #Cruze MP y FIC
    #Primero lo que debe de cruzar
    MP_FIC = pd.merge(MP, FIC, how = 'left', left_on = 'llave_ventas', right_on = 'llave_ventas')

    #Analisis de lo que no debe cruzar
    MP_FIC[MP_FIC.Plan_y.isnull() & MP_FIC.Versión_x.str.contains('VC')].Versión_x.value_counts()
    Faltantes_FIC = MP_FIC[MP_FIC.Plan_y.isnull() & ~MP_FIC.Versión_x.str.contains('VC')]

    Escritura_Sheets.Escritura(Faltantes_FIC, 3, header = True, Escribir = 'no') 

    #Me quedo con lo que cruzo
    MP_FIC = MP_FIC[~MP_FIC.Plan_y.isnull()]

    #Base final MP_FIC
    MP_FIC = pd.merge(MP, FIC, how = 'left', left_on = 'llave_ventas', right_on = 'llave_ventas')

    MP_FIC.keys()
    
    MP_FIC = MP_FIC.iloc[:, [0,1,2,3,4,5,6,7,8,9,10,11,12,13,15,24,25,26,27,28,29]]
    
    MP_FIC.columns = ['cliente','marca','llave_ventas','plataforma_abreviacion','plataforma','versión','fecha_inicio_plan',
                      'fecha_fin_plan','mes_plan','costo_planeado','kpi_planeado','serving','inversión_plataforma','inversión_total'
                      ,'plan_x','inversión_AdOps','Operativo_AdOps','Serving_AdOps','costo_operativo','conteo_MP_FIC','plan_y']
    
    return MP_FIC


