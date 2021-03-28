# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 20:06:54 2021

@author: crf005r
#Mejoras: 
    - Incluir Aire
    - Importar los datos directo de Sheets
    - Limpiar y estructurar codigo repetitivo
    - Crear Validador (Lo que no cruza, Las que al abrir nomenclatura no encajan, Diagram de Ven Euler con los cruzes)
    - Exportar Archivo de Validaciones
"""
import os
import pandas as pd
from datetime import datetime
pd.options.mode.chained_assignment = None

os.chdir('C:/Users/crf005r/Documents/6_datasense')
os.listdir()


#--Lectura de archivos--#
facebook = pd.read_excel('Facebook.xlsx', sheet_name = 'Raw Data Report', skiprows=1,names=['Nombre de la campaña', 'Nombre del conjunto de anuncios','Nombre del anuncio', 'Plataforma', 'Día', 'Impresiones', 'Divisa','Importe gastado (MXN)', 'Alcance', 'Clics en el enlace','Reproducciones de video hasta el 100%','Interacción con una publicación', 'Inicio del informe','Fin del informe'])
google_ads = pd.read_csv('Google Ads Plataforma.csv', skiprows = 2, encoding = "latin-1")

#--Seleccion y renombrado de columnas--#
facebook = facebook.loc[:,["Plataforma", "Nombre de la campaña", "Nombre del conjunto de anuncios", "Nombre del anuncio", "Día", "Divisa", "Clics en el enlace", "Impresiones", "Importe gastado (MXN)", "Reproducciones de video hasta el 100%", "Interacción con una publicación", "Alcance"]]
facebook.columns = ["plataforma", "campaña", "grupo_de_anuncios", "anuncio", "fecha", "moneda", "clics", "impresiones", "dinero_gastado","views", "interacciones","alcance"]

google_ads = google_ads.loc[:, ["Campaña", "Grupo de anuncios", "Día", "Moneda", "Clics", "Impresiones", "Costo", "Vistas"]]
google_ads.columns = ["campaña", "grupo_de_anuncios", "fecha", "moneda", "clics", "impresiones", "dinero_gastado","views"]


#--Formato de Columnas--#
#Fechas
facebook.fecha = pd.to_datetime(facebook.fecha, format = "%Y/%m/%d")
facebook.fecha = facebook.fecha.apply(lambda x : x.strftime('%Y-%m-%d'))

google_ads.fecha = pd.to_datetime(google_ads.fecha, format = "%d/%m/%Y")
google_ads.fecha = google_ads.fecha.apply(lambda x : x.strftime('%Y-%m-%d'))

#Numericas
result = pd.concat([facebook, google_ads])

result.clics = result.clics.apply(lambda x : str(x).replace(',','')).astype('float')
result.impresiones = result.impresiones.apply(lambda x : str(x).replace(',','')).astype('float')
result.dinero_gastado = result.dinero_gastado.apply(lambda x : str(x).replace(',','')).astype('float')
result.views = result.views.apply(lambda x : str(x).replace(',','')).astype('float')
result.interacciones = result.interacciones.apply(lambda x : str(x).replace(',','')).astype('float')
result.alcance = result.alcance.apply(lambda x : str(x).replace(',','')).astype('float')
result = result.fillna(0)

#--Transformaciones--#
#Etiquetado de datos, agrupaciones, campos calculados especiales

result.loc[(result['plataforma'].str.contains('audience_network')) | (result['plataforma'].str.contains('messenger')) , 'plataforma'] = 'facebook'
result.loc[result['plataforma'] == 0, 'plataforma'] = 'google ads'
result = result.groupby(['plataforma', 'campaña', 'grupo_de_anuncios', 'anuncio', 'fecha','moneda'], as_index = False).sum()

a = result.groupby(["plataforma","campaña","grupo_de_anuncios","anuncio","fecha"]).agg({'dinero_gastado': 'sum'})
a = a.groupby(["campaña","grupo_de_anuncios","anuncio","fecha"]).apply(lambda x: x / float(x.sum())).reset_index().rename(columns = {"dinero_gastado":"porcentaje_dinero_gastado"})
result = pd.merge(result, a, on = ["plataforma","campaña","grupo_de_anuncios","anuncio","fecha"])

#--Analytics--#

analytics = pd.read_excel('Google Analytics.xlsx', sheet_name = 'Conjunto de datos1')
analytics = analytics.reindex(columns = ['Campaña', 'Google Ads: grupo de anuncios', 'Contenido del anuncio', 'Fecha', 'Ingresos', 'Duración de la sesión', 'Sesiones', 'Usuarios', 'Usuarios nuevos', 'Rebotes','Número de visitas a páginas'])
analytics.columns = ["campaña", "grupo_de_anuncios", "anuncio", "fecha", "ingresos", "duracion_sesion", "sesiones", "usuarios", "usuarios_nuevos", "rebotes","paginas_vistas"]
analytics.fecha = analytics.fecha.astype(str)
analytics.fecha = analytics.fecha.apply(lambda x : datetime.strptime(x, '%Y%m%d').strftime('%Y-%m-%d'))
analytics.campaña = analytics.campaña.apply(lambda x: str(x).replace("(not set)",""))
analytics.grupo_de_anuncios = analytics.grupo_de_anuncios.apply(lambda x: str(x).replace("(not set)",""))
analytics.anuncio = analytics.anuncio.apply(lambda x: str(x).replace("(not set)",""))

analytics["llave_facebook"] =  analytics.campaña + "-" + analytics.anuncio + "-" + analytics.fecha
analytics["llave_google"] =  analytics.campaña + "-" + analytics.grupo_de_anuncios + "-" + analytics.fecha
analytics = analytics.loc[:,["llave_facebook","llave_google","ingresos", "duracion_sesion", "sesiones", "usuarios", "usuarios_nuevos", "rebotes","paginas_vistas"]]

#--Cruzes de Informacion Facebook, Google con Analytics--#

#Facebook con Analytics

#--Toda la información--#
tmp = pd.merge(facebook, analytics, how = 'outer', on = ['campaña','anuncio','fecha'])
tmp ['comentario'] = ""

#-Generamos 2 casos para ver la calidad de informacion
#Caso 1 queremos campañas que tengan algo en dinero gastado e ingresos
tmp_a = tmp[ (tmp.dinero_gastado != 0) | (tmp.impresiones != 0) | (tmp.ingresos != 0) | (tmp.duracion_sesion != 0)]
#Caso 2 muestra campañas basura que no gastaron ni generaron ingresos
tmp_b = tmp[ (tmp.dinero_gastado == 0) & (tmp.impresiones == 0) & (tmp.ingresos == 0) & (tmp.duracion_sesion == 0)]

#-Revisando lo que Cruza correctamente
tmp_c = tmp_a[ ~(tmp_a.dinero_gastado.isnull()) & ~(tmp_a.ingresos.isnull()) ]
tmp_c['comentario'] = "información correcta"

#-Lo que debo revisar 
tmp_d = tmp_a[ (tmp_a.dinero_gastado.isnull()) | (tmp_a.ingresos.isnull()) ]

#-Tengo analytics y no las encontro en plataforma
tmp_d_1 = tmp_d[ tmp_d.dinero_gastado.isnull() ]

 #Son unicas y no todas deben estar en las plataformas
len(tmp_d_1.llave_facebook.unique())
 #Dividimos en casos campañas de Fb y Google
tmp_d_1_1 = tmp_d_1[ ~(tmp_d_1.llave_facebook.str.contains('GA')) ] 
tmp_d_1_2 = tmp_d_1[ (tmp_d_1.llave_facebook.str.contains('GA')) ] 
tmp_d_1_2['comentario'] = "información que sabemos es de Google Ads"

#-Tengo en las plataformas y no las encontre en analytics
tmp_d_2 = tmp_d[ tmp_d.ingresos.isnull() ]

#--¿Con que me debo quedar?--#
#El objetivo actual es tener un monitoreo de las campañas.
#Por lo tanto solo me quedo con campañas que cruzan bien.
tmp_f = pd.concat([ tmp_c]) 
tmp_f.comentario.value_counts()
tmp_f = tmp_f.fillna(0)

#Los valores unicos deben ser de información correcta, que tenemos en el mp y en las plataformasa
tmp_f.llave_facebook.value_counts()
validacion = tmp_f.groupby(['llave_facebook', 'plataforma']).count()
#validacion es correcto ese duplicado por el grupo de anuncio
tmp_f[tmp_f.llave_facebook.str.contains("COOP-FB-DECORACION_INTEGRAL-YVES_SAINT_LAURENT-201020-021120-AW-ENGAGEMENT-NATIVAS_LAL-COMPRADORES_DE_PERFUMERIA-STORIE-01-1920X1080-2020-11-02")]

#--¿Toda la información cruzo?--#
#
# No, se debe revisar que es lo que no esta cruzando y ¿por que?
# Una ves que se corrija volvemos a correr el código.
#¿Qué debemos revisar sobre la nomenclatura? #
tmp_revision = pd.concat([tmp_d_2,tmp_d_1_1])

#Google con Analytics
#Analisis de Google Ads
google_ads["llave_google"] = google_ads.campaña + "-" + google_ads.grupo_de_anuncios + "-" + google_ads.fecha

tmp = pd.merge(google_ads, analytics, how = 'outer', on = 'llave_google')
tmp ['comentario'] = ""

#-Generamos 2 casos para ver la calidad de informacion
#Caso 1 queremos campañas que tengan algo en dinero gastado e ingresos
tmp_a = tmp[ (tmp.dinero_gastado != 0) | (tmp.impresiones != 0) | (tmp.ingresos != 0) | (tmp.duracion_sesion != 0)]
#Caso 2 muestra campañas basura que no gastaron ni generaron ingresos
tmp_b = tmp[ (tmp.dinero_gastado == 0) & (tmp.impresiones == 0) & (tmp.ingresos == 0) & (tmp.duracion_sesion == 0)]

#-Revisando lo que Cruza correctamente
tmp_c = tmp_a[ ~(tmp_a.dinero_gastado.isnull()) & ~(tmp_a.ingresos.isnull()) ]
tmp_c['comentario'] = "información correcta"

#-Lo que debo revisar 
tmp_d = tmp_a[ (tmp_a.dinero_gastado.isnull()) | (tmp_a.ingresos.isnull()) ]

#-Tengo analytics y no las encontro en plataforma
tmp_d_1 = tmp_d[ tmp_d.dinero_gastado.isnull() ]

 #Son unicas y no todas deben estar en las plataformas
len(tmp_d_1.llave_facebook.unique())
 #Dividimos en casos campañas de Fb y Google
tmp_d_1_1 = tmp_d_1[ ~(tmp_d_1.llave_facebook.str.contains('GA')) ] 
tmp_d_1_2 = tmp_d_1[ (tmp_d_1.llave_facebook.str.contains('GA')) ] 
tmp_d_1_2['comentario'] = "información que sabemos es de Google Ads"

#-Tengo en las plataformas y no las encontre en analytics
tmp_d_2 = tmp_d[ tmp_d.ingresos.isnull() ]

#--¿Con que me debo quedar?--#
#El objetivo actual es tener un monitoreo de las campañas.
#Por lo tanto solo me quedo con campañas que cruzan bien.
tmp_f = pd.concat([ tmp_c]) 
tmp_f.comentario.value_counts()
tmp_f = tmp_f.fillna(0)

#Los valores unicos deben ser de información correcta, que tenemos en el mp y en las plataformasa
tmp_f.llave_facebook.value_counts()
validacion = tmp_f.groupby(['llave_facebook', 'plataforma']).count()
#validacion es correcto ese duplicado por el grupo de anuncio
tmp_f[tmp_f.llave_facebook.str.contains("COOP-FB-DECORACION_INTEGRAL-YVES_SAINT_LAURENT-201020-021120-AW-ENGAGEMENT-NATIVAS_LAL-COMPRADORES_DE_PERFUMERIA-STORIE-01-1920X1080-2020-11-02")]

#--¿Toda la información cruzo?--#
#
# No, se debe revisar que es lo que no esta cruzando y ¿por que?
# Una ves que se corrija volvemos a correr el código.
#¿Qué debemos revisar sobre la nomenclatura? #
tmp_revision = pd.concat([tmp_d_2,tmp_d_1_1])
















result = pd.concat([tmp_f, tmp_2])
result["ingresos_val"] = result.ingresos
result = result.loc[:,["plataforma", "campaña", "grupo_de_anuncios", "anuncio", "fecha", "moneda", "clics", "impresiones", "dinero_gastado", "porcentaje_dinero_gastado","ingresos", "ingresos_val", "duracion_sesion", "sesiones", "usuarios", "usuarios_nuevos", "rebotes", "views", "interacciones", "paginas_vistas", "alcance"]]
result = result.fillna(0)

#Formato numerico
result.clics = result.clics.apply(lambda x : str(x).replace(',','')).astype('float')
result.impresiones = result.impresiones.apply(lambda x : str(x).replace(',','')).astype('float')
result.dinero_gastado = result.dinero_gastado.apply(lambda x : str(x).replace(',','')).astype('float')
result.porcentaje_dinero_gastado = result.porcentaje_dinero_gastado.apply(lambda x : str(x).replace(',','')).astype('float')
result.views = result.views.apply(lambda x : str(x).replace(',','')).astype('float')

#Distribuir las metricas de Analytics de acuerdo al porcentaje de dinero Gastado, sobre todo para Facebook que tiene campañas de Instagram y Facebook
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

#

