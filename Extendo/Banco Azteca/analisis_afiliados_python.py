# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 21:13:42 2021

@author: crf005r
"""
import pandas as pd
import sqldf #Libreria de python que nos ayuda a introducir codigo SQL
import os
import plotly.express as px

pd.set_option('display.float_format', lambda x: '%.2f' % x) #Opcion para notación científica

#Definimos la ruta para poder trabajar con los diferentes Scripts de apoyo
os.chdir('C:/Users/crf005r/Downloads')
os.listdir()

df_1 = pd.read_csv('bq-results-mes-dia-hora-segundos.csv')
catalogo = pd.read_csv('catalogo.csv')
#Limpieza de nulos
df_1.isnull().sum()

df_1.loc[(df_1.media_source.isnull()) | (df_1.media_source == "None"), "media_source"] = "vacio"
df_1.loc[(df_1.af_prt.isnull()) | (df_1.af_prt == "None"), "af_prt"] = "vacio"
df_1 = df_1.fillna(0)
df_1.isnull().sum()

tmp = df_1.media_source.value_counts()
tmp = df_1.af_prt.value_counts()

#Etiquetados
df_1["Equipo"] = ""
df_1["Nombre"] = ""

for i in range(0,86):
    df_1.loc[(df_1['af_prt'].str.contains(catalogo["af_prt"][i])) & (df_1['media_source'].str.contains(catalogo["media_source"][i])), 'Equipo'] = catalogo["Equipo"][i]

for i in range(0,86):
    df_1.loc[(df_1['af_prt'].str.contains(catalogo["af_prt"][i])) & (df_1['media_source'].str.contains(catalogo["media_source"][i])), 'Nombre'] = catalogo["Nombre"][i]

tmp = df_1.groupby(["media_source","af_prt","Equipo","Nombre"]).count()

df_1.to_csv("bq-result-etiquetados.csv")

df = pd.read_csv("bq-result-etiquetados.csv")
df = df.iloc[:,1:]
df.head()

#Transormaciones Rangos Tiempos
df["SEGUNDOS"] = df["SEGUNDOS"].astype(int)
df = df[df.SEGUNDOS >= 0]

#Analizando el 26 de Abril
df["minutos"] = df["SEGUNDOS"]/60
df["minutos"] = round(df["minutos"],1)

df["horas"] = df["minutos"]/60
df["horas"] = round(df["horas"],1)

df["dias"] = round(df["horas"]/24,4)

tmp = df.head()

################################################################################
#Cuál es el tiempo promedio en que después de un click se genera la instalación#

#Contamos con muchos Outliers
df.describe()

#Promedio minutos, horas, dias
tmp = df.groupby(["MES","DIA","HORA"],as_index =False).agg({"SEGUNDOS":"mean",
                                                               "minutos":"mean",
                                                               "horas":"mean",
                                                               "dias":"mean"})

fig = px.bar(tmp, x = "HORA",y="horas",text="horas",color="HORA")
fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', title_text = "Tiempo Promedio por Hora del día - no se tienen un patrón por alguna hora del día")
fig.write_html('grafica_1.html', auto_open=True)

#####################################################
#Mayor detalle de la información por Equipo y Nombre#
tmp = df.groupby(["MES","DIA","Equipo"],as_index =False).agg({"SEGUNDOS":"mean",
                                                               "minutos":"mean",
                                                               "horas":"mean",
                                                               "dias":"mean"})

fig = px.bar(tmp, x = "Equipo",y="horas",text="horas",color="Equipo")
fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', title_text = "Tiempo promedio de horas por Equipo - afiliados tienen mayor etiquetado con media source y af prt")
fig.write_html('grafica_2.html', auto_open=True)
#
tmp = df.groupby(["MES","DIA","Equipo","Nombre"],as_index =False).agg({"SEGUNDOS":"mean",
                                                                       "minutos":"mean",
                                                                       "horas":"mean",
                                                                       "dias":"mean"})

fig = px.bar(tmp, x = "Nombre", color = "Equipo",y="horas",text="horas")
fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', title_text = "Tiempo promedio de horas por Equipo y Nombre - desglozando los Nombres que pertenecen a cada Equipo")
fig.write_html('grafica_3.html', auto_open=True)

############################################################################################
#Que porcentaje de esas installs esta entre los 0-30 segundos, 30-1 min y arriba de 5 horas#
df.loc[df.SEGUNDOS < 30, "cs_seg"] = "-30 seg"
df.loc[(df.SEGUNDOS > 30) & (df.SEGUNDOS <= 60), "cs_seg"] = "30-60 seg"
df.loc[df.SEGUNDOS > 60, "cs_seg"] = "+60 seg"
df.cs_seg.value_counts(normalize = True)

df.loc[(df.horas >= 5) & (df.horas < 24), "cs_hrs"] = "5-24 hrs"
df.loc[df.horas > 24, "cs_hrs"] = "+ 24 hrs"
df.loc[df.horas < 5, "cs_hrs"] = "- 5 hrs"
df.cs_hrs.value_counts(normalize = True)

############################################################################################
#Rangos de tiempo con 0-30 segundos, 30-1 minuto y arriaba de 5 horas por Equipos y Nombres#
tmp = df.groupby(["Equipo","cs_seg"],as_index =False).agg({"SEGUNDOS":"mean",
                                                           "minutos":"mean",
                                                           "horas":"mean",
                                                           "dias":"mean"})

fig = px.bar(tmp, x = "Equipo",y="SEGUNDOS",text="SEGUNDOS",color="Equipo", facet_row = "cs_seg")
fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', title_text = "Rangos de tiempo 30-60 seg (1%) , -30 seg (4%) y +60 seg (95%)")
fig.write_html('grafica_4.html', auto_open=True)

tmp = df.groupby(["Equipo","cs_hrs"],as_index =False).agg({"SEGUNDOS":"mean",
                                                           "minutos":"mean",
                                                           "horas":"mean",
                                                           "dias":"mean"})

fig = px.bar(tmp, x = "Equipo",y="horas",text="horas",color="Equipo", facet_row = "cs_hrs")
fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', title_text = "Rangos de tiempo +24 hrs (37%) , -5 hrs (27%) y 5-24 hrs (36%)")
fig.write_html('grafica_5.html', auto_open=True)
#
tmp = df.groupby(["Equipo","Nombre","cs_seg"],as_index =False).agg({"SEGUNDOS":"mean",
                                                           "minutos":"mean",
                                                           "horas":"mean",
                                                           "dias":"mean"})

fig = px.bar(tmp, x = "Nombre",y="SEGUNDOS",text="SEGUNDOS",color="Equipo", facet_row = "cs_seg")
fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', title_text = "Rangos de tiempo 30-60 seg (1%) , -30 seg (4%) y +60 seg (95%)")
fig.write_html('grafica_6.html', auto_open=True)

tmp = df.groupby(["Equipo","Nombre","cs_hrs"],as_index =False).agg({"SEGUNDOS":"mean",
                                                           "minutos":"mean",
                                                           "horas":"mean",
                                                           "dias":"mean"})

fig = px.bar(tmp, x = "Nombre",y="horas",text="horas",color="Equipo", facet_row = "cs_hrs")
fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', title_text = "Rangos de tiempo +24 hrs (37%) , -5 hrs (27%) y 5-24 hrs (36%)")
fig.write_html('grafica_7.html', auto_open=True)
















