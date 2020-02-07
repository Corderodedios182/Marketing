#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 19:13:23 2019

@author: carlos
"""

import plotly.offline as pyo
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

datos = pd.read_csv('/home/carlos/Documentos/Adsocial/e-commerce/Acumulado_DSP.csv')

marca = datos[datos.Marca == 'RadioShack']

####Una Marca

fig = px.scatter(marca, x="Inversion Planeada", y="Revenue",
                        color="Marca",size = 'Impresiones Entregadas',
                        hover_name='Campaña')

fig.add_trace(go.Scatter(x=marca.loc[:,'Inversion Planeada'], y=marca.loc[:,'Inversion Planeada'],
                         name='Buen ROA si se encuentra por encima de la línea roja'
                         ))

fig.update_layout(
    title="Historico Campañas ROAS:  " + str(marca.Marca.unique()[0]),
    font=dict(
        size=10
    )
)

fig.update_yaxes(tickprefix="$")
fig.update_xaxes(tickprefix="$")

pyo.plot(fig)

####Una Marca desglosada por Mes

fig = px.scatter(marca, x="Inversion Planeada", y="Revenue", facet_col="Mes",
                        color="Marca",size = 'Impresiones Entregadas',
                        hover_name='Campaña',category_orders={"Mes": list(datos.Mes.unique())})

fig.update_layout(
    title="Historico Campañas por Mes ROAS:  " + str(marca.Marca.unique()[0]),
    font=dict(
        size=10
    )
)

fig.update_yaxes(tickprefix="$")
fig.update_xaxes(tickprefix="$")

pyo.plot(fig)

#### Por Mes y todas las Marcas

fig = px.scatter(datos, x="Inversion Planeada", y="Revenue",
                        facet_row="Marca", facet_col="Mes",
                        color="ROA",size = 'Impresiones Entregadas',
                        hover_name='Campaña',color_continuous_scale=px.colors.cyclical.HSV,
          category_orders={"Mes": list(datos.Mes.unique())})

fig.update_layout(
    title="Historico ROAS todas las Marcas",
    font=dict(
        size=10
    )
)

fig.update_yaxes(tickprefix="$")
fig.update_xaxes(tickprefix="$")

pyo.plot(fig)
