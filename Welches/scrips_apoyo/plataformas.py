# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 20:06:54 2021

@author: crf005r
"""
import os
import pandas as pd
from datetime import datetime

os.chdir('C:/Users/crf005r/Documents/6_datasense')
os.listdir()

analytics = pd.read_excel('Google Analytics.xlsx', sheet_name = 'Conjunto de datos1')
analytics = analytics.reindex(columns = ['Campaña', 'Google Ads: grupo de anuncios', 'Contenido del anuncio', 'Fecha', 'Ingresos', 'Duración de la sesión', 'Sesiones', 'Usuarios', 'Usuarios nuevos', 'Rebotes','Número de visitas a páginas'])
analytics.columns = ["campaña", "grupo_de_anuncios", "anuncio", "fecha", "ingresos", "duracion_sesion", "sesiones", "usuarios", "usuarios_nuevos", "rebotes","paginas_vistas"]
analytics.fecha = analytics.fecha.astype(str)
analytics.fecha = analytics.fecha.apply(lambda x : datetime.strptime(x, '%Y%m%d').strftime('%Y-%m-%d'))
analytics.grupo_de_anuncios = analytics.grupo_de_anuncios.apply(lambda x: str(x).replace("(not set)",""))
analytics.anuncio = analytics.anuncio.apply(lambda x: str(x).replace("(not set)",""))
analytics["llave_facebook"] =  analytics.campaña + "-" + analytics.anuncio + "-" + analytics.fecha
analytics["llave_google"] =  analytics.campaña + "-" + analytics.grupo_de_anuncios + "-" + analytics.fecha
analytics = analytics.loc[:,["llave_facebook","llave_google","ingresos", "duracion_sesion", "sesiones", "usuarios", "usuarios_nuevos", "rebotes","paginas_vistas"]]

facebook = pd.read_excel('Facebook.xlsx', sheet_name = 'Raw Data Report')
facebook = facebook.iloc[1:].loc[:,["Plataforma", "Nombre de la campaña", "Nombre del conjunto de anuncios", "Nombre del anuncio", "Día", "Divisa", "Clics en el enlace", "Impresiones", "Importe gastado (MXN)", "Reproducciones de video hasta el 100%", "Interacción con una publicación", "Alcance"]]
facebook.columns = ["plataforma", "campaña", "grupo_de_anuncios", "anuncio", "fecha", "moneda", "clics", "impresiones", "dinero_gastado","views", "interacciones","alcance"]
facebook.fecha = pd.to_datetime(facebook.fecha, format = "%Y/%m/%d")
facebook.fecha = facebook.fecha.apply(lambda x : x.strftime('%Y-%m-%d'))
facebook.loc[(facebook['plataforma'].str.contains('audience_network')) | (facebook['plataforma'].str.contains('messenger')) , 'plataforma'] = 'facebook'
facebook = facebook.groupby(['plataforma', 'campaña', 'grupo_de_anuncios', 'anuncio', 'fecha','moneda'], as_index = False).sum()
facebook["llave_facebook"] = facebook.campaña + "-" + facebook.anuncio + "-" + facebook.fecha
facebook["llave_facebook_tmp"] = facebook.campaña + "-" + facebook.anuncio + "-" + facebook.fecha + "-" + facebook.plataforma

tmp = facebook[facebook.llave_facebook.str.contains('ECOM-FB-DPA_PROSPECTING-AON-010520-310520-TR-TRANSACCION_ONLINE-DPA-PROSPECTING-DINAMICO-COSMETICOS-2020-11-01')]
tmp = facebook.groupby(['llave_facebook_tmp','llave_facebook']).agg({'dinero_gastado': 'sum'})
tmp = tmp.groupby(level=1).apply(lambda x: 100 * x / float(x.sum()))
tmp.columns = ['porcentaje_dinero_gastado']

tmp_2 = pd.merge(facebook, tmp, how = 'outer', on = 'llave_facebook_tmp')
facebook = tmp_2.loc[:,['plataforma', 'campaña', 'grupo_de_anuncios', 'anuncio','fecha','moneda', 'clics', 'impresiones', 'dinero_gastado', 'porcentaje_dinero_gastado', 'views','interacciones', 'alcance', 'llave_facebook']]

google_ads = pd.read_csv('Google Ads Plataforma.csv', skiprows = 2, encoding = "latin-1")
google_ads["Plataforma"] = 'Google Ads'
google_ads = google_ads.loc[:, ["Plataforma","Campaña", "Grupo de anuncios", "Día", "Moneda", "Clics", "Impresiones", "Costo", "Vistas"]]
google_ads["porcentaje_dinero_gastado"] = 1
google_ads.columns = ["plataforma", "campaña", "grupo_de_anuncios", "fecha", "moneda", "clics", "impresiones", "dinero_gastado","porcentaje_dinero_gastado","views"]
google_ads.fecha = pd.to_datetime(google_ads.fecha, format = "%d/%m/%Y")
google_ads.fecha = google_ads.fecha.apply(lambda x : x.strftime('%Y-%m-%d'))
google_ads["llave_google"] = google_ads.campaña + "-" + google_ads.grupo_de_anuncios + "-" + google_ads.fecha

tmp_1 = pd.merge(facebook, analytics, how = 'outer', left_on = "llave_facebook", right_on = "llave_facebook")
tmp_1 = tmp_1.fillna(0)
tmp_1 = tmp_1[(tmp_1.ingresos != 0) & (tmp_1.impresiones != 0)]

tmp_2 = pd.merge(google_ads, analytics.iloc[:,1:], how = 'outer', left_on = "llave_google", right_on = "llave_google")
tmp_2 = tmp_2.fillna(0)
tmp_2 = tmp_2[(tmp_2.ingresos != 0) & (tmp_2.impresiones != 0)]

result = pd.concat([tmp_1, tmp_2])
result["ingresos_val"] = result.ingresos
result = result.loc[:,["plataforma", "campaña", "grupo_de_anuncios", "anuncio", "fecha", "moneda", "clics", "impresiones", "dinero_gastado", "porcentaje_dinero_gastado","ingresos", "ingresos_val", "duracion_sesion", "sesiones", "usuarios", "usuarios_nuevos", "rebotes", "views", "interacciones", "paginas_vistas", "alcance"]]
result = result.fillna(0)

#Formato numerico
result.clics = result.clics.apply(lambda x : str(x).replace(',','')).astype('float')
result.impresiones = result.impresiones.apply(lambda x : str(x).replace(',','')).astype('float')
result.dinero_gastado = result.dinero_gastado.apply(lambda x : str(x).replace(',','')).astype('float')
result.porcentaje_dinero_gastado = result.porcentaje_dinero_gastado.apply(lambda x : str(x).replace(',','')).astype('float')
result.views = result.views.apply(lambda x : str(x).replace(',','')).astype('float')

#Distribuir las metricas de Analytics para Facebook
result.ingresos = (result.porcentaje_dinero_gastado/100) * result.ingresos
result.duracion_sesion = (result.porcentaje_dinero_gastado/100) * result.duracion_sesion
result.sesiones = (result.porcentaje_dinero_gastado/100) * result.sesiones
result.usuarios = (result.porcentaje_dinero_gastado/100) * result.usuarios
result.usuarios_nuevos = (result.porcentaje_dinero_gastado/100) * result.usuarios_nuevos
result.rebotes = (result.porcentaje_dinero_gastado/100) * result.rebotes
result.paginas_vistas = (result.porcentaje_dinero_gastado/100) * result.paginas_vistas

#Abriendo la Nomenclatura
tmp_1 = result.loc[:,'campaña'].str.split("-",20,expand = True)
cols = ["unidad_de_negocio", "plataforma", "campaña", "subcampaña","fecha_inicio","fecha_fin","estrategia","objetivo","concatenar","concatenar","concatenar","concatenar"]
tmp_1.columns = cols

tmp_2 = result.loc[:,'grupo_de_anuncios'].str.split("-",20,expand = True)
cols = ["tipo_de_formato", "provedor_de_medio", "tipo_audiencia", "nombre_audiencia"]
tmp_2.columns = cols

tmp_3 = result.loc[:,'anuncio'].str.split("-",20,expand = True)
cols = ["tipo_audiencia", "nombre_audiencia", "formato", "creativo", "dimension"]
tmp_3.columns = cols

tmp_f = pd.concat([tmp_1,tmp_2,tmp_3,result], axis = 1)

#pruebas para validar cruzes
#a = google_ads[google_ads.llave_google.str.contains('ECOM-GA-BUEN_FIN_HARDLINE-2020-091120-201120-CO-VIEW_PRODUCT-DISCOVERY-GOOGLE-CUSTOM_INTENT-COMPETENCIA_RETAIL')]
#b = analytics[analytics.llave_google.str.contains('ECOM-GA-BUEN_FIN_HARDLINE-2020-091120-201120-CO-VIEW_PRODUCT-DISCOVERY-GOOGLE-CUSTOM_INTENT-COMPETENCIA_RETAIL')]
#c = pd.merge(a, b, how = 'outer', left_on = "llave_google", right_on = "llave_google")

tmp_f.to_csv('master_2_python.csv')



