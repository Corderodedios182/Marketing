#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 22:13:19 2019

@author: dianabarquera

Descripcion: Visualización de la información de Google Analytics:
    
    Productos más vendidos por mes
    1.General
    2.Edad
    3.Región
    4.Sexo

Solo tomar 2019, agregar homestore

Primero se importan todos los archivos -> se limpian y agrupan -> se grafican

"""
#Paqueterías
import os 
import re 
import pandas as pd
import plotly.offline as pyo
import plotly.express as px
import plotly.graph_objects as go
import glob
import random

pd.set_option('display.float_format', lambda x: '%.f' % x)

#--          UNION DE LOS DIFERENTES ARCHIVOS DE GOOGLE ANALYTICS       --#

#Une todos los archivos de productos de las cuentas.
def union_archivos(Cuenta, analysis):
    
    analytics_union = []
    
    for i in range(len(Cuenta)):
        archivos = glob.glob("/home/carlos/Dropbox/Históricos GG/Históricos GG/" + Cuenta[i] + "/G Analytics/Productos/" + analysis + "/*.xlsx")
        
        # Productos por Campaña #
        for xls in archivos:
                tmp = pd.ExcelFile(xls)
                tmp = pd.read_excel(xls, 'Conjunto de datos1')
                tmp['archivo'] = xls
                tmp = tmp.iloc[:-1]
                tmp['cuenta'] = Cuenta[i]
                analytics_union.append(tmp)

    analytics_union = pd.concat(analytics_union)

    analytics_union['fechas'] = [ re.findall( r"\d{8}-\d{8}" ,i) for i in analytics_union.archivo ]
    
    return analytics_union

# Uso de la función union archivos #
analytics_productos = union_archivos(Cuenta = ['Office Depot','Petco','RadioShack','Home Store'], analysis = 'General') ; tmp = analytics_productos.head()

analytics_region = union_archivos(Cuenta = ['Office Depot','Petco','RadioShack','Home Store'], analysis = 'Región') ; tmp = analytics_region.head()

analytics_edad = union_archivos(Cuenta = ['Office Depot','Petco','RadioShack','Home Store'], analysis = 'Edad') ; tmp = analytics_edad.head()

analytics_sexo = union_archivos(Cuenta = ['Office Depot','Petco','RadioShack','Home Store'], analysis = 'Sexo') ; tmp = analytics_sexo.head()

analytics_productos.archivo.value_counts()
analytics_productos.dtypes
analytics_productos.notnull().all()
analytics_productos.cuenta.value_counts()

###############################################################################################
#
#                                               LIMPIEZA DE DATOS
#
# 1.Formato de fechas, colocamos la fecha del reporte para extraer el mes del reporte
# 2.Reducción del nombre del producto tomando las primeras 3 palabras
# 3.Agrupacion por mes, cuenta, producto_nuevo
# 4.Limpiamos la fuente de medios
#
# Objetivo: tenero mayor claridad de los datos.
###############################################################################################

#Fechas
def Formato_Fechas_analytics(Base, Columna):

    fechas = Base[Columna].astype(str).str.split("-",expand = True)
    fechas = pd.DataFrame(fechas)
    fechas.columns = ['Fecha_inicio','Fecha_fin']
     
    Base['Fecha_inicio'] = fechas.iloc[:,0]
    Base['Fecha_fin'] = fechas.iloc[:,1]
       
    Base.Fecha_inicio = Base.Fecha_inicio.apply(lambda x: str(x).replace("['",""))
    Base.Fecha_fin = Base.Fecha_fin.apply(lambda x: str(x).replace("']",""))
    
    Base.Fecha_inicio = pd.to_datetime(Base.Fecha_inicio,format = "%Y%m%d")
    Base.Fecha_fin = pd.to_datetime(Base.Fecha_fin,format = "%Y%m%d")

    return Base

#Reduccion del nombre de los productos
def Formato_Producto(Base):

    #Base.Producto[Base.Producto.isnull()] = ""
    Base.Producto = Base.Producto.str.lower()
    tmp = Base.Producto.str.split(" ", 20, expand=True).iloc[:,:3]
    tmp.fillna(value=" ", inplace=True)
    Producto_nueva = tmp.iloc[:,0] + " " + tmp.iloc[:,1] + " " +  tmp.iloc[:,2]

    return Producto_nueva

#Base analytics_productos
analytics_productos = Formato_Fechas_analytics(analytics_productos, 'fechas')

analytics_productos['mes'] = pd.DatetimeIndex(analytics_productos['Fecha_inicio']).month.map(str)

analytics_productos.Fecha_inicio.value_counts()

analytics_productos = analytics_productos[analytics_productos.Fecha_inicio > '2018-12-01T00:00:00.000000000'] #solo 2019

analytics_productos.Fecha_inicio.value_counts()

analytics_productos['Producto_nueva'] = Formato_Producto(analytics_productos)

#Reduccion de la fuente de medios
analytics_productos.keys()
analytics_productos = analytics_productos.rename(columns = {'Fuente/Medio':'Fuente_Medio'})
analytics_productos.notnull().all()
analytics_productos = analytics_productos.fillna('vacio')
analytics_productos['Fuente_Medio'] = analytics_productos['Fuente_Medio'].str.lower()

#Conteo de registros por cliente
analytics_productos.cuenta.value_counts()

conteo_FuenteMedios = pd.DataFrame(analytics_productos.Fuente_Medio.value_counts()).reset_index()
#Agrupación una ves limpia la base para reducir su tamaño y claridad
analytics_productos_limpio = analytics_productos.groupby(['mes','cuenta','Fuente_Medio','Producto_nueva'], as_index = False).sum()
analytics_productos_limpio['Fuente_categoria'] = analytics_productos_limpio['Fuente_Medio']

def Fuente_categoria(Base):
    #Adsocial
    Base.loc[Base['Fuente_categoria'].str.contains('adsocial'), 'Fuente_categoria'] = 'Adsocial'

    #Otros sitios
    Base.loc[Base['Fuente_categoria'].str.contains('referral'), 'Fuente_categoria'] = 'otros_sitios_web'

    #Organico
    Base.loc[( (Base['Fuente_categoria'].str.contains('organic')) |
               (Base['Fuente_categoria'].str.contains('bin')) |
               (Base['Fuente_categoria'].str.contains('google / cpc'))), 'Fuente_categoria'] = 'organico'

    #Email
    Base.loc[Base['Fuente_categoria'].str.contains('email', case=False), 'Fuente_categoria'] = 'email'

    #Tiendeo
    Base.loc[Base['Fuente_categoria'].str.contains('tiendeo', case=False), 'Fuente_categoria'] = 'tiendeo'

    #direct
    Base.loc[Base['Fuente_categoria'].str.contains('direct', case=False), 'Fuente_categoria'] = 'direct'

    #Otros
    Base.loc[ (~(Base['Fuente_categoria'].str.contains('Adsocial')) &
               ~(Base['Fuente_categoria'].str.contains('otros_sitios')) &
               ~(Base['Fuente_categoria'].str.contains('organico')) &
               ~(Base['Fuente_categoria'].str.contains('email')) &
               ~(Base['Fuente_categoria'].str.contains('tiendeo')) & 
               ~(Base['Fuente_categoria'].str.contains('direct')) ) , 'Fuente_categoria'] = 'otros'
    
    return Base
    
#Reduccion de la información por cuenta
analytics_productos_limpio.cuenta.value_counts()

#Validación de alguna fuente categoria
validacion = analytics_productos_limpio[analytics_productos_limpio.Fuente_categoria == 'otros_sitios_web']
tmp = validacion.Fuente_Medio.value_counts().reset_index().sort_values('index')

analytics_productos_limpio.Fuente_categoria.value_counts()
analytics_productos_limpio.groupby(['cuenta','Fuente_categoria']).count()

###errores en la información
#los archivos no contienen la columna fuente medio
tmp = analytics_productos[analytics_productos.cuenta == 'Home Store']
###

#--------------------------#Trabajar las demás bases de datos#----------------------------------------------------------#

Estados = ["Aguascalientes","Baja California","Baja California Sur","Campeche","Chiapas","Chihuahua","Mexico City","Coahuila","Colima","Durango","State of Mexico","Guanajuato","Guerrero","Hidalgo","Jalisco","Michoacan","Morelos","Nayarit","Nuevo Leon","Oaxaca","Puebla","Queretaro","Quintana Roo","San Luis Potosi","Sinaloa","Sonora","Tabasco","Tamaulipas","Tlaxcala","Veracruz","Yucatan","Zacatecas"]


###########################################
##              Gráficas                ###
###########################################
random.seed(1)
analytics_productos_limpio['mes_jitter'] = [random.randint(10,70) for i in range(analytics_productos_limpio.shape[0])]
analytics_productos_limpio['mes_jitter'] = analytics_productos_limpio.mes.astype(str) + "." + analytics_productos_limpio.mes_jitter.astype(str)

#nube de puntos productos google analytics
analytics_productos_limpio.Fuente_categoria.value_counts()
analytics_productos_limpio.groupby(['cuenta','Fuente_categoria']).count()

analytics_productos.cuenta.unique()

#Todas las fuentes
datos_interes = analytics_productos_limpio[analytics_productos_limpio['cuenta'] == 'Office Depot']

#animation_frame = 'mes'
fig = px.scatter(datos_interes, x="mes_jitter", y="Ingresos del producto", color="Fuente_categoria",
                 size="Compras únicas", hover_name ="Producto_nueva",color_continuous_scale=px.colors.sequential.Viridis) 

fig.update_layout(
    title="2019 productos Google Analytics, todas las Fuentes " + str(datos_interes.cuenta.unique()[0]),
    font=dict(size=10),
    annotations = [dict(xref='paper',
                        yref='paper',
                        x=0.5, y=1.05,
                        showarrow=False,
                        text ='¿Como se distribuye en porcentajes las fuentes de medios?')],
                        template = 'ggplot2'
)

pyo.plot(fig)

#Solo Adsocial
datos_interes = analytics_productos_limpio[(analytics_productos_limpio['Fuente_categoria'] == 'Adsocial') & (analytics_productos_limpio['cuenta'] == 'Office Depot')]

fig = px.scatter(datos_interes, x="mes_jitter", y="Ingresos del producto", color="Cantidad",
                 size="Compras únicas", hover_name ="Producto_nueva",color_continuous_scale=px.colors.sequential.Viridis) 

fig.update_layout(
    title="2019 productos Google Analytics, Fuente Adsocial " + str(datos_interes.cuenta.unique()[0]),
    font=dict(size=10),
    annotations = [dict(xref='paper',
                        yref='paper',
                        x=0.5, y=1.05,
                        showarrow=False,
                        text ='')],
                        template = 'ggplot2'
)

pyo.plot(fig)


#caja y bigotes google analytics
#analytics_productos_limpio[analytics_productos_limpio['Ingresos del producto'] < 200] 
fig_2 = go.Figure()

fig_2.add_trace(go.Box(
    y=datos_interes['Ingresos del producto'],
    x=datos_interes['mes_jitter'],
    jitter=0.5,
    whiskerwidth=0.2,
    marker_size=2,
    line_width=1)
    )

fig_2.update_layout(
    title = 'Histórico de ingresos productos Google Analytics '  + str(datos_interes.cuenta.unique()[0]),
    title_x = 0.50,
    yaxis_title='Estadisticos mínimo, máximo, promedio, cuantiles',
    template = 'ggplot2'
    )

#fig.update_yaxes(tickprefix="$")
pyo.plot(fig_2)




# Bolitas

### Genero

fig = px.scatter(Genero, x="mes", y="Ingresos del producto", color="Sexo", 
                 size="Cantidad", hover_name ="Producto_nueva")
                        
fig.update_layout(
    title="Productos comprados por Género",
    font=dict(
        size=10
    )
)

fig.update_yaxes(tickprefix="$")
pyo.plot(fig)


#### Edad

fig = px.scatter(Edad, x="mes", y="Ingresos del producto", color="Edad", 
                 size="Cantidad", hover_name ="Producto_nueva")
                        
fig.update_layout(
    title="Productos comprados por Edad",
    font=dict(
        size=10
    )
)

fig.update_yaxes(tickprefix="$")
pyo.plot(fig)

#### Geo

fig = px.scatter(Geo, x="mes", y="Ingresos del producto", color="Región", 
                 size="Cantidad", hover_name ="Producto_nueva")
                        
fig.update_layout(
    title="Productos comprados por Región",
    font=dict(
        size=10
    )
)

fig.update_yaxes(tickprefix="$")
pyo.plot(fig)

########### Cruce??? ########


#Base_Sexo[Base_Sexo.Producto.str.contains('CAJA')]

tmp_edad = Base_Edad.loc[Base_Edad.Producto == 'PANTALLA SANSUI SMX32Z1 (32 PULG., HD)',:]
tmp_sexo = Base_Sexo.loc[Base_Sexo.Producto == 'PANTALLA SANSUI SMX32Z1 (32 PULG., HD)',:]
tmp_union = pd.merge(tmp_edad, tmp_sexo, on = 'Producto', how = 'left')















































