# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.
"""
#Importación
from datetime import datetime

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

from librerias import Escritura_Sheets #Escribe la información en Google Sheets


#
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













