#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 14:00:15 2019

@author: carlos
"""
Base_master_final = []

tmp = Base_master_final.Nombre_Campaña.unique()

Base_master_final.loc[Base_master_final.Nombre_Campaña.str.contains('AO'), 'Tipo_campaña'] = 'AO'
Base_master_final.loc[Base_master_final.Nombre_Campaña.str.contains('AO'), 'Tipo_campaña'] = 'AO'



tmp = Base_master_final.groupby(['Año','Mes']).count()
tmp = Base_master_final[(Base_master_final.Año == 2019.0) & (Base_master_final.Mes == 12.0)]
Union_FB.groupby(['Archivo']).count()

Union_FB.keys()

tmp = Union_FB[Union_FB.Archivo == 'RadioShack-Campañas-1-nov-2019-30-nov-2019.csv']

tmp = Base_master_final[Base_master_final.Archivo == 'Office-Depot-Campañas-1-nov-2019-30-nov-2019.csv']

tmp = Base_master[Base_master.Nombre_Campaña == '1911_OD_iZettle_FB']
tmp = Base_master[Base_master.Plataforma == 'Facebook']







