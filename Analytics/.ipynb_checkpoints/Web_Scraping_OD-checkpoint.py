#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 12:14:28 2020

@author: carlos
"""
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import pandas as pd
import re

#llamada
url = 'https://www.officedepot.com.mx'
req = Request(url , headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()

#formato beatifulsoup
page_soup = BeautifulSoup(webpage)
page_soup.prettify()

page_soup.find('a',{'class':'nav__link js_nav__link'}) #un elemento

#---Categorias principales---#
links = page_soup.findAll('a',{'class':'nav__link js_nav__link'}) #todos los elementos

Categoria = []
href = []

for link in links:
    Categoria.append(link.get('title'))
    href.append(link.get('href'))

datos_1 = pd.DataFrame(Categoria,href).reset_index().drop_duplicates()
datos_1.columns = ('href','categoria')
datos_1['Nivel'] = 'Categoria_principal'

#---Sub categoria---#
links = page_soup.findAll('a',{'class':'motherlink'}) #todos los elementos

sub_categoria = []
href = []

for link in links:
    href.append(link.get('href'))
    sub_categoria.append(link.text)
    
datos_2 = pd.DataFrame(sub_categoria,href).reset_index().drop_duplicates()
datos_2.columns = ('href','sub_categoria')
datos_2['Nivel'] = 'sub_categoria'


#---sub_categoria_secundaria---#
links = page_soup.findAll('li',{'class':'nav__link--secondary'}) #todos los elementos

sub_categoria_secundaria = []
href = []

for i in range(0,len(links)):
    href.append(links[i].findAll('a')[0].get('href'))
    sub_categoria_secundaria.append(links[i].findAll('a')[0].get('title'))

datos_3 = pd.DataFrame(sub_categoria_secundaria,href).reset_index().drop_duplicates()
datos_3.columns = ('href','sub_categoria_secundaria')
datos_3['Nivel'] = 'sub_categoria_secundaria'

#--Union de las bases--#
datos_1['href_keys'] = [re.findall(r"\d{2}", i) for i in list(datos_1.href)]
datos_1['href_keys'] = datos_1['href_keys'].astype(str)

datos_2['href_keys'] = [re.findall(r"\W\d{2}\W", i) for i in list(datos_2.href)]
datos_2['href_keys'] = datos_2['href_keys'].apply(lambda x : str(x).replace('/','')).apply(lambda x : str(x).replace('-',''))
datos_2 = datos_2[ ~datos_2['href_keys'].str.contains('08')]
datos_2 = datos_2[ ~datos_2['href_keys'].str.contains('09')]

datos_2['href_keys_t'] = [re.findall(r"\W\d{3}\W", i) for i in list(datos_2.href)]
datos_2['href_keys'] = datos_2['href_keys'].apply(lambda x : str(x).replace('/','')).apply(lambda x : str(x).replace('-',''))


datos_3['href_keys'] = [re.findall(r"\W\d{2}\W", i) for i in list(datos_3.href)]
datos_3['href_keys'] = datos_3['href_keys'].apply(lambda x : str(x).replace('/','')).apply(lambda x : str(x).replace('-',''))

datos_3 = datos_3[ ~datos_3['href_keys'].str.contains('08')]
datos_3 = datos_3[ ~datos_3['href_keys'].str.contains('09')]

datos_3['href_keys_t'] = [re.findall(r"\W\d{3}\W", i) for i in list(datos_3.href)]

tmp = pd.merge(datos_1, datos_2, how = 'outer', left_on = 'href_keys', right_on = 'href_keys')

tmp["href_keys_t"] = tmp.href_keys_t.astype(str)
datos_3["href_keys_t"] = datos_3.href_keys_t.astype(str)

tmp = pd.merge(tmp, datos_3, how = 'outer', left_on = 'href_keys_t', right_on = 'href_keys_t')

#--info dashbord--##
#Definimos la ruta para poder trabajar con los diferentes Scripts de apoyo
import os
os.chdir('/home/carlos/Documentos/3_Adsocial/Marketing/Union_Campañas')
os.listdir()

from librerias import Escritura_Sheets #Escribe la información en Google Sheets

Escritura_Sheets.Escritura(tmp , 4, Escribir = 'si', header = True, archivo_sheet = 'Dashboard Competencias')

