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
analytics = pd.read_excel('Google Analytics.xlsx', sheet_name = 'Conjunto de datos1',names=["campaña", "anuncio", "grupo_de_anuncios", "fecha", "sesiones", "usuarios", "usuarios_nuevos","rebotes", "transacciones","ingresos", "duracion_sesion","paginas_vistas"])

#--Seleccion y renombrado de columnas--#
facebook = facebook.loc[:,["Plataforma", "Nombre de la campaña", "Nombre del conjunto de anuncios", "Nombre del anuncio", "Día", "Divisa", "Clics en el enlace", "Impresiones", "Importe gastado (MXN)", "Reproducciones de video hasta el 100%", "Interacción con una publicación", "Alcance"]]
facebook.columns = ["plataforma", "campaña", "grupo_de_anuncios", "anuncio", "fecha", "moneda", "clics", "impresiones", "dinero_gastado","views", "interacciones","alcance"]

google_ads = google_ads.loc[:, ["Campaña", "Grupo de anuncios", "Día", "Moneda", "Clics", "Impresiones", "Costo", "Vistas"]]
google_ads.columns = ["campaña", "grupo_de_anuncios", "fecha", "moneda", "clics", "impresiones", "dinero_gastado","views"]

analytics = analytics.loc[:,["campaña", "grupo_de_anuncios", "anuncio", "fecha", "ingresos", "duracion_sesion", "sesiones", "usuarios", "usuarios_nuevos", "rebotes","paginas_vistas"]]
analytics.columns = ["campaña", "grupo_de_anuncios", "anuncio", "fecha", "ingresos", "duracion_sesion", "sesiones", "usuarios", "usuarios_nuevos", "rebotes","paginas_vistas"]

#--Formato de Columnas--#
#Fechas
facebook.fecha = pd.to_datetime(facebook.fecha, format = "%Y/%m/%d")
facebook.fecha = facebook.fecha.apply(lambda x : x.strftime('%Y-%m-%d'))

google_ads.fecha = pd.to_datetime(google_ads.fecha, format = "%d/%m/%Y")
google_ads.fecha = google_ads.fecha.apply(lambda x : x.strftime('%Y-%m-%d'))

analytics.fecha = analytics.fecha.astype(str)
analytics.fecha = analytics.fecha.apply(lambda x : datetime.strptime(x, '%Y%m%d').strftime('%Y-%m-%d'))

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
def master_format(result, analytics):
    
    """Etiquetado de datos, agrupaciones, campos calculados especiales"""    
    
    result.loc[(result['plataforma'].str.contains('audience_network')) | (result['plataforma'].str.contains('messenger')) , 'plataforma'] = 'facebook'
    result.loc[result['plataforma'] == 0, 'plataforma'] = 'google ads'
    result = result.groupby(['plataforma', 'campaña', 'grupo_de_anuncios', 'anuncio', 'fecha','moneda'], as_index = False).sum()

    a = result.groupby(["plataforma","campaña","grupo_de_anuncios","anuncio","fecha"]).agg({'dinero_gastado': 'sum'})
    a = a.groupby(["campaña","grupo_de_anuncios","anuncio","fecha"]).apply(lambda x: x / float(x.sum())).reset_index().rename(columns = {"dinero_gastado":"porcentaje_dinero_gastado"})
    result = pd.merge(result, a, on = ["plataforma","campaña","grupo_de_anuncios","anuncio","fecha"])
    
    analytics = analytics.fillna('')
    analytics.campaña = analytics.campaña.apply(lambda x: str(x).replace("(not set)",""))
    analytics.grupo_de_anuncios = analytics.grupo_de_anuncios.apply(lambda x: str(x).replace("(not set)",""))
    analytics.anuncio = analytics.anuncio.apply(lambda x: str(x).replace("(not set)",""))
    analytics = analytics.groupby(["campaña","grupo_de_anuncios","anuncio","fecha"], as_index = False).sum()
    
    #--Cruzes de Informacion Facebook, Google con Analytics--#
    tmp_f = pd.merge(result[result.plataforma != 'google ads'], analytics, how = 'left', on = ['campaña','anuncio','fecha'])
    tmp_f = tmp_f.fillna(0)
    tmp_f = tmp_f.loc[:,['plataforma', 'campaña', 'grupo_de_anuncios_x', 'anuncio', 'fecha','moneda', 'clics', 'impresiones', 'dinero_gastado', 'views','interacciones', 'alcance', 'porcentaje_dinero_gastado','ingresos', 'duracion_sesion', 'sesiones','usuarios', 'usuarios_nuevos','rebotes', 'paginas_vistas']]
    tmp_f.columns = ['plataforma', 'campaña', 'grupo_de_anuncios', 'anuncio', 'fecha','moneda', 'clics', 'impresiones', 'dinero_gastado', 'views','interacciones', 'alcance', 'porcentaje_dinero_gastado','ingresos', 'duracion_sesion', 'sesiones','usuarios', 'usuarios_nuevos','rebotes', 'paginas_vistas']
    
    #Tenemos duplicados por los de analytics, se debe agrupar solo por campaña y grupo de anuncios
    analytics.anuncio = ''
    analytics = analytics.groupby(["campaña","grupo_de_anuncios","anuncio","fecha"], as_index = False).sum()
    
    tmp_a = pd.merge(result[result.plataforma == 'google ads'], analytics, how = 'left', on = ['campaña','grupo_de_anuncios','fecha'])
    tmp_a = tmp_a.fillna(0)
    tmp_a = tmp_a.loc[:,['plataforma', 'campaña', 'grupo_de_anuncios', 'anuncio_y', 'fecha',
                         'moneda', 'clics', 'impresiones', 'dinero_gastado', 'views',
                         'interacciones', 'alcance', 'porcentaje_dinero_gastado',
                         'ingresos', 'duracion_sesion', 'sesiones', 'usuarios',
                         'usuarios_nuevos', 'rebotes', 'paginas_vistas']]
    tmp_a.columns = ['plataforma', 'campaña', 'grupo_de_anuncios', 'anuncio', 'fecha',
                     'moneda', 'clics', 'impresiones', 'dinero_gastado', 'views',
                     'interacciones', 'alcance', 'porcentaje_dinero_gastado',
                     'ingresos', 'duracion_sesion', 'sesiones', 'usuarios',
                     'usuarios_nuevos', 'rebotes', 'paginas_vistas']
    
    base_master = pd.concat([tmp_f, tmp_a])
    
    #Distribuir las metricas de Analytics de acuerdo al porcentaje de dinero Gastado, sobre todo para Facebook que tiene campañas de Instagram y Facebook
    base_master["ingresos_validacion"] = base_master.ingresos
    base_master.ingresos = (base_master.porcentaje_dinero_gastado) * base_master.ingresos
    base_master.duracion_sesion = (base_master.porcentaje_dinero_gastado) * base_master.duracion_sesion
    base_master.sesiones = (base_master.porcentaje_dinero_gastado) * base_master.sesiones
    base_master.usuarios = (base_master.porcentaje_dinero_gastado) * base_master.usuarios
    base_master.usuarios_nuevos = (base_master.porcentaje_dinero_gastado) * base_master.usuarios_nuevos
    base_master.rebotes = (base_master.porcentaje_dinero_gastado) * base_master.rebotes
    base_master.paginas_vistas = (base_master.porcentaje_dinero_gastado) * base_master.paginas_vistas
    
    #Abriendo la Nomenclatura
    tmp_1 = base_master.loc[:,'campaña'].str.split("-",20,expand = True)
    cols = ["unidad_de_negocio", "plataforma", "campaña", "subcampaña","fecha_inicio","fecha_fin","estrategia","objetivo","concatenar","concatenar","concatenar","concatenar","concatenar"]
    tmp_1.columns = cols
    
    tmp_2 = base_master.loc[:,'grupo_de_anuncios'].str.split("-",20,expand = True)
    cols = ["tipo_de_formato", "provedor_de_medio", "tipo_audiencia", "nombre_audiencia","concatenar"]
    tmp_2.columns = cols
    
    tmp_3 = base_master.loc[:,'anuncio'].str.split("-",20,expand = True)
    cols = ["tipo_audiencia", "nombre_audiencia", "formato", "creativo", "dimension"]
    tmp_3.columns = cols
    
    base_master = pd.concat([tmp_1,tmp_2,tmp_3,base_master], axis = 1)
    
    return base_master

base_master = master_format(result, analytics)

base_master.to_csv('master_2_python.csv')




#--Validaciones--#
tmp = google_ads[(google_ads.campaña.str.contains("ECOM-GA-BRAND TERM_EXACTA-AON-160720-311220-TR-TRANSACCION_ONLINE")) & (google_ads.grupo_de_anuncios.str.contains("SEARCH-GOOGLE-COMBINADO-1ST_&_IN_MARKET_&_AFFINITY_&_SIMILARES"))]
tmp_1 = analytics[(analytics.campaña.str.contains("ECOM-GA-BRAND TERM_EXACTA-AON-160720-311220-TR-TRANSACCION_ONLINE")) & (analytics.grupo_de_anuncios.str.contains("SEARCH-GOOGLE-COMBINADO-1ST_&_IN_MARKET_&_AFFINITY_&_SIMILARES"))]

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

#

