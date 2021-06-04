# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 17:19:56 2021

@author: crf005r
"""

import os

#Definimos la ruta para poder trabajar con los diferentes Scripts de apoyo
os.chdir('C:/Users/crf005r/Documents/3_GitHub/Marketing/Welches/scrips_apoyo')
os.listdir()

from Google import Create_Service #importar y limpiar los datos de facebook
import pandas as pd

os.chdir('C:/Users/crf005r/Documents/')
os.listdir()

CLIENT_SECRET_FILE = '' #aqui va el json
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

print(dir(service))

#Creacion de Folders
carpeta_pruebas = ['Charly']

for carpeta in carpeta_pruebas:
    file_metadata = {
        'name':carpeta,
        'mimeType': 'application/vnd.google-apps.folder' 
        }
    service.files().create(body = file_metadata).execute()

#Cargar archivos
from googleapiclient.http import MediaFileUpload

folder_id = '1IHA3UrqsK8wCbGgW0h_f2x9JWYbQyFeC'
files_names = ['Solicitud de Datos.xls']
mime_types = ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']

for file_name, mime_type in zip(files_names, mime_types):
    file_metadata = {
        'name':file_name,
        'parents':[folder_id]
        }
    
    media = MediaFileUpload('C:/Users/crf005r/Documents/{0}'.format(file_name), mimetype=mime_type)
    
    service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id').execute()
    
    
    
    
    
    
    
    
    