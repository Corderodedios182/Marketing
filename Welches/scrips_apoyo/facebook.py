# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 20:06:54 2021

@author: crf005r
"""
import os
from scrips_apoyo import google_sheets

os.chdir('C:/Users/crf005r/Documents/3_GitHub/Marketing/Welches')
os.listdir()

def datos_facebook():
    
    #Importar datos
    df_facebook = google_sheets.importar_sheets(hoja = 2)
    
    #Limpieza y estructura
    
    
    #Exportar la base final
    return df_facebook
    



