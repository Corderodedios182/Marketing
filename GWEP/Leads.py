#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 11:54:24 2020

@author: carlos
"""

import pandas as pd
import matplotlib as plt
import numpy as np
from matplotlib.dates import DateFormatter

# Import necessary packages
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

Lead_001 = pd.read_csv('Documentos/Adsocial/GWEP/Data/Leads_001.csv', sep = ',', header = 0, skipinitialspace = True)

Lead = Lead_001.loc[:,('Correo electrónico', 'Correo electrónico secundario', 'Fuente de Posible cliente', 'Estado de Posible cliente',
                'Nombre completo', 'Desarrollo', 'Nombre de la campaña de anuncios', 'Nombre del grupo de anuncios', 'Estatus KPI',
                'Descripción', 'Campaña MKT', 'LP', 'Forma de contacto', 'Motivo de perdido',
                'Palabra clave', 'Hora de creacion', 'Hora de modificacion', 'Hora ultima actividad', 'Hora de cita web')]


#Agustín filtra por fecha de creación, Desarrollo, y fuente del Lead

#Conteo hora de creacion
Lead['Hora_creacion'] = pd.to_datetime(Lead.loc[:,'Hora de creacion'], format = '%d/%m/%y')
tmp = pd.DataFrame(Lead.Hora_creacion.value_counts())

plt.scatter(tmp.index.values, tmp.Hora_creacion, s=1)
plt.title("Conteo Leads Hora de Creación")
plt.xlabel("Hora de Creacion")
plt.ylabel("Conteo")
plt.gcf().autofmt_xdate()
plt.show()

#Desarrollo
tmp = pd.DataFrame(Lead['Desarrollo'].value_counts())
plt.bar(tmp.index.values, tmp.Desarrollo)
plt.xticks(rotation=90)
plt.title("Conteo Leads Desarrollo")
plt.xlabel("Desarrollo")
plt.ylabel("Conteo")

#Fuente Lead
tmp = pd.DataFrame(Lead['Fuente de Posible cliente'].value_counts()).reset_index()

tmp['Fuente'] = np.where(tmp['Fuente de Posible cliente'] < 25,'otros',tmp['index'])

plt.bar(tmp['Fuente'], tmp['Fuente de Posible cliente'])
plt.xticks(rotation=90)
plt.title("Fuente de Posible cliente")
plt.xlabel("Fuente")
plt.ylabel("Conteo")

#Por mes 
Lead.index = Lead.Hora_creacion
Lead.index.name = 'Creacion'
tmp = Lead.resample('M').count().reset_index()

plt.plot(tmp.Creacion, tmp.Hora_creacion, marker = 'o',markerfacecolor='blue', markersize=5, color='skyblue', linewidth=4)
plt.xticks(rotation=90)
plt.title("Lead Mensuales")
plt.xlabel("Fecha")
plt.ylabel("Conteo")

#Fuente Posible Cliente
Lead.to_csv("Lead.csv")


Lead['Hora de creacion'] = pd.to_datetime(Lead['Hora de creacion'], format = '%d/%m/%y').dt.to_period('M')

tmp = Lead.loc[:,('Hora de creacion','Fuente de Posible cliente')]
tmp.head()

tmp.to_csv("tmp.csv")

#Hice la grafica con R

#Tipo de Lead
Lead.keys()
Lead.loc[:,'Estado de Posible cliente'].value_counts()

Buenos_Lead = ['Contactado','Contactar en el futuro','Intento de contacto','Visita agendada']

#Tipo de Lead y Fuente de Posible cliente

tmp = Lead.loc[:,('Hora de creacion','Estado de Posible cliente','Fuente de Posible cliente')]
tmp.head()

tmp.to_csv("tmp_1.csv")


#Que palabras clave tiene el CRM

Lead.loc[:,'Palabra clave'].value_counts().count()

Lead.keys()

Lead.loc[:,'Campaña MKT'].value_counts()

Lead.loc[:,'Nombre de la campaña de anuncios'].value_counts()

#¿Que se hace con el Lead?
