#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 11:30:53 2019

@author: carlos
"""
import os 
import re 
import pandas as pd

###########
#Analytics#
###########

Dianis = []

#Este for va entrando en cada carpeta para solo trabajar con los arhivos de cada Marca
for Analytics in os.listdir('/home/carlos/Documentos/Adsocial/Sheets/Analytics/'):

    os.chdir('/home/carlos/Documentos/Adsocial/Sheets/Analytics/' + str(Analytics))
    Archivos = pd.Series(os.listdir())
    
    #Conversiones Asistidas
    tmp_conversiones = list(Archivos[Archivos.str.contains('Conver')])

    Union_conversiones = []
    
    #Trabaja solo los archivos de conversiones
    for csv in tmp_conversiones:
        tmp = pd.read_csv(csv, skiprows = 6)
        tmp = tmp.iloc[:-3,:]
        tmp['archivo'] = csv
        Union_conversiones.append(tmp)

    Union_conversiones = pd.concat(Union_conversiones)

    Union_conversiones = Union_conversiones.loc[:,('archivo','Fuente/Medio','Campaña','Conversiones asistidas','Valor de las conversiones asistidas','Conversiones asistidas/de último clic o directas')]
    Union_conversiones.columns = ['archivo','Fuente_Medio','Nombre_Campaña','Conversiones','Revenue','Conversiones_asistidas/de_último_clic_o_directas']

    Union_conversiones['Tipo'] = 'Asistida'

    Union_conversiones.Conversiones = Union_conversiones.Conversiones.astype('int')

    Union_conversiones.Revenue = Union_conversiones.Revenue.apply(lambda x : str(x).replace('.',''))
    Union_conversiones.Revenue = Union_conversiones.Revenue.apply(lambda x : str(x).replace(',','.'))
    Union_conversiones.Revenue = Union_conversiones.Revenue.apply(lambda x : str(x).replace('MXN','')).astype('float')

    Union_conversiones['Marca'] = Analytics

    Dianis.append(Union_conversiones)

Dianis = pd.concat(Dianis)

Dianis['fechas'] = [ re.findall( r"\d{8}-\d{8}" ,i) for i in Dianis.archivo ]

Dianis['Plataforma'] = ''

Analytics_asistida = Dianis.loc[:,('fechas', 'Plataforma', 'Marca','Fuente_Medio','Nombre_Campaña','Conversiones_asistidas/de_último_clic_o_directas')]

pd.to_csv()

import os
import pandas as pd
os.getcwd()

os.chdir('/home/carlos/Documentos/Adsocial')
Analytics_asistida.to_csv("Analytics_asistida.csv")







