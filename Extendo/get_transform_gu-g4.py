# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 22:06:34 2021

@author: crf005r
"""

import os
import json
import pandas as pd

os.chdir("C:\\Users\\crf005r\\Desktop")
os.listdir()

tmp = [{'id': '28905845', 'kind': 
        'analytics#accountSummary',
        'name': 'Abaco Metrics',
        'webProperties': [{'kind': 'analytics#webPropertySummary',
                           'id': 'UA-28905845-1',
                           'name': 'Extendo Company',
                           'internalWebPropertyId': '54809049',
                           'level': 'PREMIUM',
                           'websiteUrl': 'https://extendo.company',
                           'profiles': [{'kind': 'analytics#profileSummary', 
                                         'id': '101809727',
                                         'name': 'Abaco Metrics User Id Report',
                                         'type': 'WEB'},
                                        {'kind': 'analytics#profileSummary',
                                         'id': '104019925',
                                         'name': 'Abaco metrics- perfil de pruebas offline',
                                         'type': 'WEB'},
                                        {'kind': 'analytics#profileSummary',
                                         'id': '98431944',
                                         'name': 'abacoacademy.com', 
                                         'type': 'WEB'},
                                        {'kind': 'analytics#profileSummary',
                                         'id': '90133406',
                                         'name': 'abacometrics - master',
                                         'type': 'WEB'},
                                        {'kind': 'analytics#profileSummary',
                                         'id': '55826206',
                                         'name': 'abacometrics.com - backup',
                                         'type': 'WEB'},
                                        {'kind': 'analytics#profileSummary',
                                         'id': '194915170',
                                         'name': 'Aeromexico',
                                         'type': 'WEB'},
                                        {'kind': 'analytics#profileSummary',
                                         'id': '194875082',
                                         'name': 'Aeromexico - Test',
                                         'type': 'WEB'},
                                        {'kind': 'analytics#profileSummary', 
                                         'id': '219189069',
                                         'name': 'EXTENDO',
                                         'type': 'WEB'},
                                        {'kind': 'analytics#profileSummary',
                                         'id': '55768954',
                                         'name': 'EXTENDO - Testing',
                                         'type': 'WEB'},
                                        {'kind': 'analytics#profileSummary',
                                         'id': '238038355',
                                         'name': 'Extendo Filters Test', 
                                         'type': 'WEB'}]}]},
       {'id': '3879175',
        'kind': 'analytics#accountSummary',
        'name': 'Xcaret',
        'webProperties': [{'kind': 'analytics#webPropertySummary',
                           'id': 'UA-3879175-12',
                           'name': 'Xcaret.com',
                           'internalWebPropertyId': '138698446',
                           'level': 'PREMIUM',
                           'websiteUrl': 'https://www.xcaret.com',
                           'profiles': [{'kind': 'analytics#profileSummary',
                                         'id': '143017449',
                                         'name': 'Back-Up',
                                         'type': 'WEB'},
                                        {'kind': 'analytics#profileSummary',
                                         'id': '143017750',
                                         'name': 'Master - Xcaret',
                                         'type': 'WEB'},
                                        {'kind': 'analytics#profileSummary',
                                         'id': '142998051',
                                         'name': 'PRUEBAS - Xcaret',
                                         'type': 'WEB'},
                                        {'kind': 'analytics#profileSummary',
                                         'id': '142977560',
                                         'name': 'Xcaret Español - Sin Filtros',
                                         'type': 'WEB'},
                                        {'kind': 'analytics#profileSummary',
                                         'id': '142994949',
                                         'name': 'Xcaret Español - Sin Tráfico Interno',
                                         'type': 'WEB'},
                                        {'kind': 'analytics#profileSummary',
                                         'id': '142975471',
                                         'name': 'Xcaret Inglés - Sin Filtros',
                                         'type': 'WEB'},
                                        {'kind': 'analytics#profileSummary',
                                         'id': '143000464',
                                         'name': 'Xcaret Inglés - Sin Tráfico Interno', 'type': 'WEB'},
                                        {'kind': 'analytics#profileSummary',
                                         'id': '143010667',
                                         'name': 'Xcaret Portugués - Sin Filtros', 'type': 'WEB'},
                                        {'kind': 'analytics#profileSummary',
                                         'id': '143030627',
                                         'name': 'Xcaret Portugués - Sin Tráfico Interno',
                                         'type': 'WEB'}]}]
        }]

tmp = pd.DataFrame(tmp)

l = []

for i in range(tmp.shape[0]):
    
    l.append(pd.DataFrame(tmp['webProperties'][i]))
    
l = pd.concat(l).reset_index()
    
tmp = pd.concat([tmp,l], axis = 1)

l = []

for i in range(tmp.shape[0]):
    
    df = pd.DataFrame(tmp['profiles'][i])
    df["GU_id"] = tmp["id"].iloc[i,1]
    
    l.append(df)

    
l = pd.concat(l).reset_index()





