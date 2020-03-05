#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 13:15:34 2020

@author: carlos
"""
#Paqueterías
import pandas as pd
import re

#############################
#Importación de las bases
#   -Limpieza de las bases, formatos, fechas, agrupaciones
#   -Estandarización
#   -Reglas de Fechas
#   -Columnas a ocupar
#   -Ver el nombre de la campaña por rmnt o pi (caso especial)
#
############################

#En caso de querer agregar nuevas validaciones a alguna plataforma corremos por línea
#Y nos traemos los archivos que queremos trabajar
import glob
Mes = 'Enero'

#Archivos_csv = glob.glob('/home/carlos/Dropbox/ROAS 2020/' + Mes + '/Semanal/**/*.csv')
#Archivos_xlsx = glob.glob('/home/carlos/Dropbox/ROAS 2020/' + Mes + '/Semanal/**/*.xlsx')

Archivos_csv = glob.glob('/home/carlos/Dropbox/ROAS 2020/' + Mes + '/Mensual/*.csv')
Archivos_xlsx = glob.glob('/home/carlos/Dropbox/ROAS 2020/' + Mes + '/Mensual/*.xlsx')

def Plataformas_tabla(Archivos_csv, Archivos_xlsx):
    
    Arch_FB = [x for x in Archivos_csv if "FB" in x]
    
    Facebook = []
    
    for csv in Arch_FB:
        
        tmp = pd.read_csv(csv)
        tmp['Archivo'] = csv
        Facebook.append(tmp)
    
    Facebook = pd.concat(Facebook)

    #Revisiones rápidas
    Facebook.Archivo.value_counts()
    Facebook.keys()
    #Columna de interés
    Facebook = Facebook.loc[:,('Archivo','Nombre de la cuenta','Nombre de la campaña','Mes','Inicio','Finalización','Divisa','Importe gastado (MXN)','Impresiones','Clics en el enlace')]
    Facebook['plataforma'] = 'Facebook'
    Facebook = Facebook.reset_index()
    #Con esta columna extraemos la fecha del reporte
    Facebook.Mes
    
    #Fechas 
    def Formato_Fechas(Base, Columna):

        fechas = Base[Columna].astype(str).str.split(" - ",expand = True)
        fechas = pd.DataFrame(fechas)
        fechas.columns = ['inicio_reporte','fin_reporte']
     
        Base['inicio_reporte'] = fechas.iloc[:,0]
        Base['fin_reporte'] = fechas.iloc[:,1]
       
        Base.inicio_reporte = Base.inicio_reporte.apply(lambda x: str(x).replace("['",""))
        Base.fin_reporte = Base.fin_reporte.apply(lambda x: str(x).replace("']",""))
    
        Base.inicio_reporte = pd.to_datetime(Base.inicio_reporte,format = "%Y-%m-%d")
        Base.fin_reporte = pd.to_datetime(Base.fin_reporte,format = "%Y-%m-%d")

        return Base

    Facebook = Formato_Fechas(Facebook, 'Mes')

    Facebook.dtypes
    Facebook['Mes'] = Facebook.inicio_reporte.apply(lambda x : x.month)

       #Extracción del nombre para cruzarlo con ventas
    C_Facebook = Facebook.loc[:,'Nombre de la campaña'].str.split("_",10,expand = True).iloc[:,:5] ; cols = ["Año-Mes","Cliente","Marca","Tipo-1","Tipo-2"]
    C_Facebook.columns = cols
    C_Facebook = C_Facebook[cols].apply(lambda row: '_'.join(row.values.astype(str)), axis=1) ; del cols

    Facebook['llave_plataformas'] = C_Facebook ; del C_Facebook
    Facebook['llave_plataformas'] = Facebook['llave_plataformas'].str.strip()

        #Columnas de interés
    Facebook.keys()
    Facebook = Facebook.loc[:,('Archivo','plataforma','Nombre de la cuenta','Nombre de la campaña','llave_plataformas','Mes','inicio_reporte','fin_reporte',
                               'Inicio','Finalización','Divisa','Importe gastado (MXN)','Impresiones','Clics en el enlace')]

    Facebook.columns = ['archivo','plataforma','cuenta','nombre_campaña','llave_plataformas','mes','inicio_reporte','fin_reporte',
                        'fecha_inicio','fecha_fin','divisa','dinero_gastado','impresiones','clics']

        #Se eliminan las campañas provenientes de estás cuentas puede que no mache con el MP
    Facebook = Facebook.loc[ ~( (Facebook.cuenta.str.contains('Adsocial'))  |  (Facebook.cuenta.str.contains('Dokkoi')) ) ]
    Facebook.llave_plataformas = Facebook.llave_plataformas.str.lower()
    Facebook.llave_plataformas = Facebook.llave_plataformas + str("_FB")

    Facebook['conteo'] = 1
    Facebook['divisa'] = 'mxn'


    #Facebook_0 = Facebook.groupby(['archivo','cuenta','llave_plataformas','mes','inicio_reporte','fin_reporte','fecha_inicio','fecha_fin'], as_index = False).sum()
    Facebook = Facebook.groupby(['plataforma','cuenta','llave_plataformas','mes','inicio_reporte','fin_reporte'], as_index = False).agg({
                                                                               'dinero_gastado':'sum',
                                                                               'impresiones':'sum',
                                                                               'clics':'sum',
                                                                               'conteo':'count'})

    #-- Adwords -- #
    Arch_Adwords = [x for x in Archivos_csv if "Adwords" in x]
    
    Adwords = []
    fallas = []

    for csv in Arch_Adwords:
        try:
            tmp = pd.read_csv(csv, sep = ',', skiprows = 2, encoding='utf-8')
            tmp['Archivo'] = csv
            #Extreamos las fechas del nombre del reporte
            Fechas = list(tmp.Archivo.unique())
            #####Se extrae la fecha de la columna Archivo, para crear Fecha_inicio_reporte y Fecha_fin_reporte
            tmp['Archivo_fechas'] = tmp['Archivo']
            
            tmp['fecha_reporte'] = [re.findall(r"\d{1}-\d{1}-\d{4}|\d{2}-\d{1}-\d{4}|\d{1}-\d{2}-\d{4}|\d{2}-\d{2}-\d{4}", i) 
                                        for i in list(tmp.Archivo_fechas)]
            
            fechas = [re.findall(r"\d{1}-\d{1}-\d{4}|\d{2}-\d{1}-\d{4}|\d{1}-\d{2}-\d{4}|\d{2}-\d{2}-\d{4}", i) for i in list(tmp.Archivo_fechas)]

            fechas = pd.DataFrame(fechas)
            fechas.columns = ['inicio_reporte','fin_reporte']
        
            tmp = pd.concat([tmp.reset_index(drop = True), pd.DataFrame(fechas)], axis = 1)
        
            Adwords.append(tmp)
        except:
            #En ocasiones por el formato no leía el archivo utf-
            fallas.append(csv)
            print("En ocasiones se guardan como UTF-16 excell ocasionando estas fallas : ",fallas)

    Adwords = pd.concat(Adwords).reset_index(drop = True)

    del Fechas, csv, fallas, fechas, tmp
        #Formato correcto para trabajar con las fechas
    
    Adwords = Adwords.rename(columns = {'Campa�a':'Campaña', 'Fecha de finalizaci�n':'Fecha de finalización'})
    
    #ok
    Adwords['Fecha de inicio'] =  pd.to_datetime(Adwords.loc[:,'Fecha de inicio'],errors='ignore',
                                                 format='%Y-%m-%d')
    #ok
    Adwords['Fecha de finalización'] =  pd.to_datetime(Adwords['Fecha de finalización'], errors = 'coerce',
                                                       format='%Y-%m-%d')
    #ok
    Adwords['inicio_reporte'] =  pd.to_datetime(Adwords['inicio_reporte'],
                                                format='%d-%m-%Y')
    
    #ok
    Adwords['fin_reporte'] =  pd.to_datetime(Adwords['fin_reporte'],errors='coerce',
                                             format='%d-%m-%Y')
    
    Adwords.keys()
    
    Adwords = Adwords.loc[:,('Archivo','Cuenta','Campaña','Mes','Fecha de inicio','Fecha de finalización','inicio_reporte','fin_reporte',
                             'Moneda','Costo','Impresiones','Clics')]
    
    Adwords.columns = ('archivo','cuenta','campaña','mes','fecha_inicio','fecha_finalización','inicio_reporte','fin_reporte','divisa','dinero_gastado','impresiones','clics')
    
    Adwords['plataforma'] = 'Adwords'
    
    Adwords['mes'] = Adwords.inicio_reporte.apply(lambda x : x.month)
    
    #Extracción del nombre para cruzar con ventas
    
    C_Adwords = Adwords.loc[:,'campaña'].str.split("_",10,expand = True).iloc[:,:5] ; cols = ["Año-Mes","Cliente","Marca","Tipo-1","Tipo-2"]
    C_Adwords.columns = cols
    C_Adwords = C_Adwords[cols].apply(lambda row: '_'.join(row.values.astype(str)), axis=1) ; del cols
    
    Adwords['llave_plataformas'] = C_Adwords ; del C_Adwords
    Adwords['llave_plataformas'] = Adwords['llave_plataformas'].str.lower()
    Adwords['llave_plataformas'] = Adwords['llave_plataformas'] + str("_SEM")
    
    #Formato numerico
    Adwords.clics = Adwords.clics.apply(lambda x : str(x).replace(',','')).astype('int')
    Adwords.impresiones = Adwords.impresiones.apply(lambda x: str(x).replace(',','')).astype('int')
    Adwords.dinero_gastado = Adwords.dinero_gastado.apply(lambda x: str(x).replace(',','')).astype('float')
    
    Adwords['plataforma'] = 'Adwords'
    Adwords['conteo'] = 1
    
    Adwords = Adwords.groupby(['plataforma','cuenta','llave_plataformas','mes','inicio_reporte','fin_reporte'], as_index = False).sum()
    
    #-- Adform --#
    Arch_Adform = [x for x in Archivos_xlsx if "Adform" in x]
    
    Adform = pd.read_excel(Arch_Adform[0], sheet_name = 'Sheet', skiprows = 2)
    Adform['Archivo'] = Arch_Adform[0] 
    
    Adform['Archivo_fechas'] = Adform['Archivo']
    
    Adform['fecha_reporte'] = [re.findall(r"\d{1}-\d{1}-\d{4}|\d{2}-\d{1}-\d{4}|\d{1}-\d{2}-\d{4}|\d{2}-\d{2}-\d{4}", i) 
                                        for i in list(Adform.Archivo_fechas)]
    
    fechas = [re.findall(r"\d{1}-\d{1}-\d{4}|\d{2}-\d{1}-\d{4}|\d{1}-\d{2}-\d{4}|\d{2}-\d{2}-\d{4}", i) for i in list(Adform.Archivo_fechas)]
    fechas = pd.DataFrame(fechas)
    fechas.columns = ['inicio_reporte','fin_reporte']
            
    Adform = pd.concat([Adform.reset_index(drop = True), pd.DataFrame(fechas)], axis = 1)
    
    Adform = Adform.iloc[:-1,].loc[:, ('Archivo','Client','Campaign','Month','Campaign Start Date','Campaign End Date','inicio_reporte',
                                       'fin_reporte','Sales (All)','Tracked Ads','Clicks')]
    
    Adform.columns = ('archivo','cuenta','campaña','mes','fecha_inicio','fecha_finalización','inicio_reporte','fin_reporte','dinero_gastado',
                      'impresiones','clics')
    
    Adform['plataforma'] = 'Adform'
    Adform['divisa'] = 'MXN'
    
    Adform = Adform.loc[:,('archivo','cuenta','campaña','mes','fecha_inicio','fecha_finalización','inicio_reporte','fin_reporte','divisa',
                           'dinero_gastado','impresiones','clics','plataforma')]
    
        #Fechas 
    Adform.fecha_inicio = pd.to_datetime(Adform.fecha_inicio, format = "%Y-%m-%d")
    Adform.fecha_finalización = pd.to_datetime(Adform.fecha_finalización,format = "%Y-%m-%d")
    
    Adform.inicio_reporte = pd.to_datetime(Adform.inicio_reporte, format = '%d-%m-%Y')
    Adform.fin_reporte = pd.to_datetime(Adform.fin_reporte,format = '%d-%m-%Y')
    
    Adform['mes'] = Adform.inicio_reporte.apply(lambda x : x.month)
    
    #Extracción del nombre para cruzarlo con ventas
    C_Adform = Adform.loc[:,'campaña'].str.split("_",10,expand = True).iloc[:,:5] ; cols = ["Año-Mes","Cliente","Marca","Tipo-1","Tipo-2"]
    C_Adform.columns = cols
    C_Adform = C_Adform[cols].apply(lambda row: '_'.join(row.values.astype(str)), axis=1)
    
    Adform['llave_plataformas'] = C_Adform ; del C_Adform
    Adform['llave_plataformas'] = Adform['llave_plataformas'].str.strip()
    
    #Se eliminan las campañas provenientes de estás cuentas puede que no mache con el MP
    #Facebook = Facebook.loc[ ~( (Facebook.Nombre_Cuenta.str.contains('Adsocial'))  |  (Facebook.Nombre_Cuenta.str.contains('Dokkoi')) ) ]
    Adform.llave_plataformas = Adform.llave_plataformas.str.lower()
    Adform.llave_plataformas = Adform.llave_plataformas + str("_DSP")
    
    #Formato numerico
    Adform.clics = Adform.clics.apply(lambda x : str(x).replace(',','')).astype('int')
    Adform.impresiones = Adform.impresiones.apply(lambda x: str(x).replace(',','')).astype('int')
    Adform.dinero_gastado = Adform.dinero_gastado.apply(lambda x: str(x).replace(',','')).astype('float')
    
    Adform['conteo'] = 1
    
    Adform = Adform.groupby(['plataforma','cuenta','llave_plataformas','mes','inicio_reporte','fin_reporte'], as_index = False).sum()
    
    #Unión de las Bases
    # -Unión de todo
    Facebook.shape[0] + Adwords.shape[0] + Adform.shape[0]
    Plataformas = pd.concat([Facebook, Adwords,Adform])
    
    return Plataformas









