# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 19:19:37 2021

@author: crf005r
"""

v = df.loc[df['media_source'] == '', :]

df.loc[df['media_source'].str.contains('ACAI'), 'media_source'] = 'ACAI'
df.loc[df['media_source'].str.contains('ad4screen_int'), 'media_source'] = 'Ad4screen'
df.loc[df['af_prt'].str.contains('ad4screen'), 'af_prt'] = 'Ad4screen'
df.loc[df['media_source'].str.contains('altea'), 'media_source'] = 'Altea'
df.loc[df['media_source'].str.contains('antevenio_int'), 'media_source'] = 'Antevenio'
df.loc[df['media_source'].str.contains('arde_int'), 'media_source'] = 'Arde'
df.loc[df['media_source'].str.contains('ardeagency'), 'media_source'] = 'Arde'
df.loc[df['media_source'].str.contains('arkeero'), 'media_source'] = 'Arkeero'
df.loc[df['media_source'].str.contains('arkeero_int'), 'media_source'] = 'Arkeero'
df.loc[df['media_source'].str.contains('askrobin'), 'media_source'] = 'Ask Robin'
df.loc[df['media_source'].str.contains('bankarte'), 'media_source'] = 'Bankarte'
df.loc[df['media_source'].str.contains('bt_group'), 'media_source'] = 'BT Group'
df.loc[df['media_source'].str.contains('central_funnel'), 'media_source'] = 'Central Funnel'
df.loc[df['media_source'].str.contains('yahoogemini_int'), 'media_source'] = 'CMI'
df.loc[df['media_source'].str.contains('CORU'), 'media_source'] = 'CORU'
df.loc[df['media_source'].str.contains('trafficcontrol_int'), 'media_source'] = 'Credy'
df.loc[df['media_source'].str.contains('digitalturbine_int'), 'media_source'] = 'Digital Turbine'
df.loc[df['media_source'].str.contains('epa'), 'media_source'] = 'EPA'
df.loc[df['media_source'].str.contains('fiizy_int'), 'media_source'] = 'Fiizy'
df.loc[df['af_prt'].str.contains('gnogmedia'), 'af_prt'] = 'Gnog'
df.loc[df['media_source'].str.contains('LEADGENIOS'), 'media_source'] = 'Lead Genios'
df.loc[df['media_source'].str.contains('leadgenios_int'), 'media_source'] = 'Lead Genios'
df.loc[df['media_source'].str.contains('leadgenios_int_channel'), 'media_source'] = 'Lead Genios'
df.loc[df['media_source'].str.contains('lemmonetmobile_int'), 'media_source'] = 'Lemmonet'
df.loc[df['media_source'].str.contains('multired'), 'media_source'] = 'Multired'
df.loc[df['media_source'].str.contains('ojo7_int'), 'media_source'] = 'Ojo 7'
df.loc[(df['media_source'].str.contains('Apple Search Ads')) & (df['af_prt'].str.contains('rankmyapp')), 'media_source'] = 'Rank my app'
df.loc[(df['media_source'].str.contains('rankmyapp_int')) & (df['af_prt'].str.contains('rankmyapp')), 'media_source'] = 'Rank my app'
df.loc[df['media_source'].str.contains('rankmyapp_int'), 'media_source'] = 'Rank my app'
df.loc[df['media_source'].str.contains('trademob_int'), 'media_source'] = 'Rank my app'
df.loc[(df['media_source'].str.contains('vungle_int')) & (df['af_prt'].str.contains('rankmyapp')), 'media_source'] = 'Rank my app'
df.loc[df['media_source'].str.contains('appreciateappoffers_int'), 'media_source'] = 'Rocket Lab'
df.loc[df['media_source'].str.contains('rocketlab_int'), 'media_source'] = 'Rocket Lab'
df.loc[df['media_source'].str.contains('mobusi_int'), 'media_source'] = 'Sunnmedia'
df.loc[df['media_source'].str.contains('teads_int'), 'media_source'] = 'Teads'
df.loc[df['media_source'].str.contains('techido_int'), 'media_source'] = 'Techido'
df.loc[df['af_prt'].str.contains('thingortwo'), 'af_prt'] = 'Thing or Two'
df.loc[df['media_source'].str.contains('transidmedia_int'), 'media_source'] = 'Transidmedia'
df.loc[df['af_prt'].str.contains('winclap'), 'af_prt'] = 'Winclap'
df.loc[df['media_source'].str.contains('zuggy'), 'media_source'] = 'zuggy'
df.loc[df['af_prt'].str.contains('lemmonet'), 'af_prt'] = 'Lemmonet'
df.loc[df['media_source'].str.contains('trending'), 'media_source'] = 'Trending Media'
df.loc[df['af_prt'].str.contains('rocket'), 'af_prt'] = 'Rocket Lab'
df.loc[df['af_prt'].str.contains('rocket'), 'af_prt'] = 'Koneo'
df.loc[df['af_prt'].str.contains('mobuppagency'), 'af_prt'] = 'Mob up'
df.loc[df['af_prt'].str.contains('mobuppagency'), 'af_prt'] = 'Papaya'
df.loc[df['media_source'].str.contains('oneenginemedia_int'), 'media_source'] = 'One engine'
df.loc[df['media_source'].str.contains('leadaki'), 'media_source'] = 'Lead Aki'
df.loc[df['media_source'].str.contains('adtiming_int'), 'media_source'] = 'Adtiming'
df.loc[df['af_prt'].str.contains('3dot14'), 'af_prt'] = '3dot14'
df.loc[df['media_source'].str.contains('kosmos'), 'media_source'] = 'Kosmos'
df.loc[df['media_source'].str.contains('taboola_int'), 'media_source'] = 'Taboola'
df.loc[df['media_source'].str.contains('opmobile_int'), 'media_source'] = 'Won Digital'
df.loc[df['media_source'].str.contains('moblin_int'), 'media_source'] = 'Zoom D'
df.loc[df['af_prt'].str.contains('htrsolutions'), 'af_prt'] = 'HTR Solutions'
df.loc[(df['af_prt'].str.contains('entravision')) | df['media_source'].str.contains('mobrain_int'), 'af_prt'] = 'Headway'

#Conociendo los datos
df.dtypes
afiliados = df.media_source.value_counts().reset_index()
afiliados_r = df.media_source_remplazo.value_counts().reset_index()
af_prt = df.af_prt.value_counts()
fecha = df.fecha.value_counts()

query = open('Banco Azteca/query_1.sql', 'r').read().split(';')[0]
filtro = sqldf.run(query)

#Query que clasifique los media source con los CASE 
#Rangos de tiempo
#Transformacion de datos: Si media_source está vacio tomar
