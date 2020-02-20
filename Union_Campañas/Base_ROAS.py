#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 12:13:57 2020

El siguiente script creará la Base de los ROAS

Los Archivos se encuentran en: /home/carlos/Dropbox/ROAS 2020 (Cada mes se crea la base del Mes y se colocan los reportes de las Plataformas)

- Facebook: FB-AdSocial-Jan-1-2020-Jan-31-2020

- Adwords:  Adwords 1-01-2020 al 31-01-2020-2

- Adform: 

- MP_FIC: KPIS 2020 - AdSocial

@author: carlos
"""
#Paqueterías
import os
import pandas as pd

#Formato números
pd.set_option('display.float_format', lambda x: '%.5f' % x)

#Rutas
#Ruta = input("Coloca la ruta donde se encuentran tus archivos: ") #Ejemplo: /home/carlos/Dropbox/ROAS 2020
os.chdir('/home/carlos/Dropbox/ROAS 2020')
#Mes = input("¿Qué mes deseas actualizar? " + str(os.listdir( )) + " : " )
os.chdir('Enero')
Archivos = os.listdir()

#############################
#Importación de las bases
#   -Estandarización
#   -Reglas de Fechas
#   -Columnas a ocupar
#   -Ver el nombre de la campaña por rmnt o pi (caso especial)
#
############################

#-- MP_FIC (KPI) --#

Arch_MP_FIC = [x for x in Archivos if "KPI" in x]
#MP
MP = pd.read_excel(Arch_MP_FIC[0], sheet_name = 'KPIS MP 2020', skiprows = 2)
MP.loc[:,'NOMENCLATURA'] = MP.loc[:,'NOMENCLATURA'].str.lower()
MP['Archivo'] = Arch_MP_FIC[0] 


#FIC
FIC = pd.read_excel(Arch_MP_FIC[0], sheet_name = 'KPIS FIC 2020', skiprows = 2)
FIC.loc[:,'NOMENCLATURA'] = FIC.loc[:,'NOMENCLATURA'].str.lower()
FIC['Archivo'] = Arch_MP_FIC[0] 

def Formato_Fechas(Base, Columna):
    Base.loc[:,Columna] = pd.to_datetime(Base.loc[:,Columna], errors = 'ignore', format = '%d/%m/%y')
    return Base.loc[:,Columna]

def Formato_numerico(Base, Columna):
    Base.loc[:,Columna] = Base.loc[:,Columna].apply(lambda x : str(x).replace('$',''))
    Base.loc[:,Columna] = Base.loc[:,Columna].apply(lambda x : str(x).replace(',',''))
    Base.loc[:,Columna] = Base.loc[:,Columna].apply(lambda x : str(x).strip())
    Base.loc[:,Columna] = Base.loc[:,Columna].apply(lambda x : str(x).replace('-','0'))
    Base.loc[:,Columna] = Base.loc[:,Columna].astype('float')
    Base.loc[:,Columna] = round(Base.loc[:,Columna],2)
    return Base.loc[:,Columna]
#Limpieza fechas
MP.loc[:,'Inicio'] = Formato_Fechas(MP, 'Inicio')
MP.loc[:,'Fin'] = Formato_Fechas(MP, 'Fin')

FIC.loc[:,'Inicio'] = Formato_Fechas(FIC, 'Inicio')
FIC.loc[:,'Fin'] = Formato_Fechas(FIC, 'Fin')
#Limpieza columnas numericas
MP.loc[:,'Costo Planeado'] = Formato_numerico(MP, 'Costo Planeado')
MP.loc[:,'KPI Planeado'] = Formato_numerico(MP, 'KPI Planeado')
MP.loc[:,'Serving'] = Formato_numerico(MP, 'Serving')
MP.loc[:,'Inversión Plataforma'] = Formato_numerico(MP, 'Inversión Plataforma')
MP.loc[:,'Inversión Total'] = Formato_numerico(MP, 'Inversión Total')

FIC.loc[:,'Inversión AdOps'] = Formato_numerico(FIC, 'Inversión AdOps')
FIC.loc[:,'Operativo AdOps'] = Formato_numerico(FIC, 'Operativo AdOps')
FIC.loc[:,'Serving AdOps'] = Formato_numerico(FIC, 'Serving AdOps')
FIC.loc[:,'Costo Operativo'] = Formato_numerico(FIC, 'Costo Operativo')

#Para poder trabajar mejor con la nomeclatura, le agregamos su plataforma para cruzar con la información de plataformas
MP['Plt'] = MP.loc[:,'Plataforma']

MP.loc[MP['Plataforma'].str.contains('Instagram') , 'Plt'] = 'IG'
MP.loc[MP['Plataforma'].str.contains('Facebook') , 'Plt'] = 'FB'
MP.loc[MP['Plataforma'].str.contains('Google') , 'Plt'] = 'SEM'
MP.loc[(MP['Plataforma'].str.contains('Programmatic')) | (MP['Plataforma'].str.contains('Display'))  , 'Plt'] = 'DSP'
MP.loc[(MP['Plataforma'].str.contains('Waze')) | (MP['Plataforma'].str.contains('AdsMovil')) , 'Plt'] = 'PV'

FIC.loc[FIC['Plataforma'].str.contains('Instagram') , 'Plt'] = 'IG'
FIC.loc[FIC['Plataforma'].str.contains('Facebook') , 'Plt'] = 'FB'
FIC.loc[FIC['Plataforma'].str.contains('Google') , 'Plt'] = 'SEM'
FIC.loc[(FIC['Plataforma'].str.contains('Programmatic')) | (FIC['Plataforma'].str.contains('Display'))  , 'Plt'] = 'DSP'
FIC.loc[(FIC['Plataforma'].str.contains('Waze')) | (FIC['Plataforma'].str.contains('AdsMovil')) , 'Plt'] = 'PV'

MP['llave_ventas'] = MP.loc[:,'NOMENCLATURA'] + str("_") + MP['Plt']
MP["llave_ventas"].str.strip()

FIC['llave_ventas'] = FIC.loc[:,'NOMENCLATURA'] + str("_") + FIC['Plt']
FIC["llave_ventas"].str.strip()

MP = MP.loc[:, ('Archivo','NOMENCLATURA','llave_ventas','CAMPAÑA','CLIENTE','MARCA','Mes','Versión','Plataforma','Plt','Formato','Inicio','Fin','TDC','Objetivo','Costo Planeado','KPI Planeado','Serving','Inversión Plataforma','Inversión Total')]
FIC = FIC.loc[:, ('Archivo','NOMENCLATURA','llave_ventas','CAMPAÑA','CLIENTE','MARCA','Mes','Versión','Plataforma','Plt','Formato','Inicio','Fin','TDC','Objetivo','Inversión AdOps','Operativo AdOps', 'Serving AdOps','Costo Operativo')]

#Filtro sobre el MP
MP = MP[~MP['Versión'].str.contains('VC')]

#Campañas unicas
MP = MP.groupby(['llave_ventas','Plt','Inicio','Fin'], as_index = False).agg({'Costo Planeado':'mean',
                                                                               'KPI Planeado':'sum',
                                                                               'Serving':'sum',
                                                                               'Inversión Plataforma':'sum',
                                                                               'Inversión Total':'sum',
                                                                               'NOMENCLATURA':'count'})

MP.groupby(['Plt']).count()['llave_ventas'].reset_index()

FIC = FIC.groupby(['llave_ventas','Plt','Inicio','Fin'], as_index = False).agg({'Inversión AdOps':'sum',
                                                                               'Operativo AdOps':'sum',
                                                                               'Serving AdOps':'sum',
                                                                               'Costo Operativo':'sum',
                                                                               'NOMENCLATURA':'count'})
FIC.groupby(['Plt']).count()['llave_ventas'].reset_index()

#############################
#Importación de las bases
#   -Limpieza de las bases, formatos, fechas, agrupaciones
#   -Estandarización
#   -Reglas de Fechas
#   -Columnas a ocupar
#   -Ver el nombre de la campaña por rmnt o pi (caso especial)
#
############################

#-- Facebook -- #
Arch_FB = [x for x in Archivos if "FB" in x]

Facebook = []

for csv in Arch_FB:
    
    tmp = pd.read_csv(csv)
    tmp['Archivo'] = csv
    Facebook.append(tmp)
    
Facebook = pd.concat(Facebook)

Facebook = Facebook.loc[:,('Archivo','Nombre de la cuenta','Nombre de la campaña','Mes','Inicio','Finalización','Divisa','Importe gastado (MXN)','Impresiones','Clics en el enlace')]
Facebook['plataforma'] = 'Facebook'
Facebook.Mes
    
#Fechas 
def Formato_Fechas(Base, Columna):

    fechas = Base[Columna].astype(str).str.split(" - ",expand = True)
    fechas = pd.DataFrame(fechas)
    fechas.columns = ['inicio_reporte','fin_reporte']
     
    Base['inicio_reporte'] = fechas.iloc[:,0]
    Base['fin_reporte'] = fechas.iloc[:,1]
       
    Base.inicio_reporte = Base.inicio_reporte.apply(lambda x: str(x).replace("['",""))
    Base.fin_reporte = Base.fin_reporte.apply(lambda x: str(x).replace("']",""))
    
    Base.inicio_reporte = pd.to_datetime(Base.inicio_reporte,format = "%Y-%m-%d")
    Base.fin_reporte = pd.to_datetime(Base.fin_reporte,format = "%Y-%m-%d")

    return Base

Facebook = Formato_Fechas(Facebook, 'Mes')

    #Extracción del nombre para cruzarlo con ventas
C_Facebook = Facebook.loc[:,'Nombre de la campaña'].str.split("_",10,expand = True).iloc[:,:5] ; cols = ["Año-Mes","Cliente","Marca","Tipo-1","Tipo-2"]
C_Facebook.columns = cols
C_Facebook = C_Facebook[cols].apply(lambda row: '_'.join(row.values.astype(str)), axis=1) ; del cols

Facebook['Llave_Facebook'] = C_Facebook ; del C_Facebook
Facebook['Llave_Facebook'] = Facebook['Llave_Facebook'].str.strip()

    #Columnas de interés
Facebook.keys()
Facebook = Facebook.loc[:,('Archivo','Nombre de la cuenta','Nombre de la campaña','Llave_Facebook','Mes','inicio_reporte','fin_reporte','Inicio','Finalización','Divisa','Importe gastado (MXN)','Impresiones','Clics en el enlace')]
Facebook.columns = ['Archivo','Nombre_Cuenta','Nombre_campaña','llave_facebook','mes','inicio_reporte','fin_reporte','Fecha_Inicio','Fecha_Fin','divisa','dinero_gastado','impresiones','clics_enlace']

    #Se eliminan las campañas provenientes de estás cuentas puede que no mache con el MP
Facebook = Facebook.loc[ ~( (Facebook.Nombre_Cuenta.str.contains('Adsocial'))  |  (Facebook.Nombre_Cuenta.str.contains('Dokkoi')) ) ]
Facebook.llave_facebook = Facebook.llave_facebook.str.lower()
Facebook.llave_facebook = Facebook.llave_facebook + str("_FB")

#tmp = Facebook.groupby(['Nombre_Cuenta','llave_facebook','Nombre_campaña'], as_index = False).count()
#tmp_0 = Facebook[Facebook['llave_facebook'] == '2001_gicsa_explanadapuebla_pi_mkt_FB']
Facebook = Facebook.groupby(['Nombre_Cuenta','llave_facebook','inicio_reporte','fin_reporte'], as_index = False).sum()

#-- Adwords -- #
Arch_Adwords = [x for x in Archivos if "Adwords" in x]

Adwords = []
fallas = []

for csv in Arch_Adwords:
    try:
        tmp = pd.read_csv(csv, sep = ',', skiprows = 2)
        tmp['Archivo'] = csv
        Adwords.append(tmp)
    except:
        #En ocasiones por el formato no leía el archivo utf-
        fallas.append(csv)
    print("En ocasiones se guardan como UTF-16 excell ocasionando estas fallas : ",fallas)

Adwords = pd.concat(Adwords).reset_index(drop = True)

Adwords = Adwords.loc[:,('Archivo','Cuenta','Campaña','Mes','Fecha de inicio','Fecha de finalización',
                           'Moneda','Costo','Impresiones','Clics')]

Adwords.columns = ('archivo','cuenta','campaña','mes','fecha_inicio','fecha_finalización','divisa','dinero_gastado','impresiones','clics')
Adwords['plataforma'] = 'Adwords'

#-- Adform --#
Arch_Adform = [x for x in Archivos if "Adform" in x]

Adform = pd.read_excel(Arch_Adform[0], sheet_name = 'Sheet', skiprows = 2)
Adform['Archivo'] = Arch_Adform[0] 

Adform = Adform.iloc[:-1,].loc[:, ('Archivo','Client','Campaign','Campaign Start Date','Campaign End Date',
                                               'Sales (All)','Tracked Ads','Clicks')]

Adform.columns = ('archivo','cuenta','campaña','fecha_inicio','fecha_finalización','dinero_gastado','impresiones','clics')

Adform['plataforma'] = 'Adform'
Adform['divisa'] = 'MXN'
Adform['mes'] = ''

Adform = Adform.loc[:,('archivo','cuenta','campaña','mes','fecha_inicio','fecha_finalización','divisa','dinero_gastado','impresiones','clics','plataforma')]

#############################
#Unión de las Bases
# -Unión de todo
#
####
####################################
#Separación del MP ó FIC Plataforma#
####################################

FIC_FB = FIC[FIC.llave_ventas.str.contains('_FB')]
MP_FB = MP[MP.llave_ventas.str.contains('_FB')]

########
#Cruzes#
########
#MP
FB_MP = pd.merge(Facebook, MP_FB, how = 'left', left_on = 'llave_facebook', right_on = 'llave_ventas')
FB_MP_NO = FB_MP[pd.isnull(FB_MP.llave_ventas)]
#¿Cuantos cruzaron?
FB_MP = FB_MP[~pd.isnull(FB_MP.llave_ventas)]

MP_FB = pd.merge(MP_FB, Facebook, how = 'left', left_on = 'llave_ventas', right_on = 'llave_facebook')
MP_FB_NO = MP_FB[pd.isnull(MP_FB.llave_facebook)]
#¿Cuantos cruzaron? 
MP_FB = MP_FB[~pd.isnull(MP_FB.llave_facebook)]

#FIC
FB_FIC = pd.merge(Facebook, FIC_FB, how = 'left', left_on = 'llave_facebook', right_on = 'llave_ventas')
FB_FIC_NO = FB_FIC[pd.isnull(FB_FIC.llave_ventas)]
#¿Cuantos cruzaron?
FB_FIC = FB_FIC[~pd.isnull(FB_FIC.llave_ventas)]

FIC_FB = pd.merge(FIC_FB, Facebook, how = 'left', left_on = 'llave_ventas', right_on = 'llave_facebook')
FIC_FB_NO = FIC_FB[pd.isnull(FIC_FB.llave_facebook)]
#¿Cuantos cruzaron?
FIC_FB = FIC_FB[~pd.isnull(FIC_FB.llave_facebook)]

###########################
#Validacion de lo faltante#
###########################
#FB_MP

FB_MP_NO_1 = FB_MP_NO.llave_facebook.str.split("_", 10,expand = True)
FB_MP_NO_1.columns = ["Año-Mes","Cliente","Marca","Tipo-1","Tipo-2",""]
FB_MP_NO_1['archivo'] = 'FB_MP'
FB_MP_NO_1['Nombre_Campaña'] = FB_MP_NO.llave_facebook

MP_FB_NO_1 = MP_FB_NO.llave_ventas.str.split("_", 10,expand = True)
MP_FB_NO_1.columns = ["Año-Mes","Cliente","Marca","Tipo-1","Tipo-2",""]
MP_FB_NO_1['archivo'] = 'MP'
MP_FB_NO_1['Nombre_Campaña'] = MP_FB_NO.llave_ventas

Union = []
Union.append(FB_MP_NO_1)
Union.append(MP_FB_NO_1)

#FB_FIC
FB_FIC_NO_1 = FB_FIC_NO.llave_facebook.str.split("_", 10,expand = True)
FB_FIC_NO_1.columns = ["Año-Mes","Cliente","Marca","Tipo-1","Tipo-2",""]
FB_FIC_NO_1['archivo'] = 'FB_FIC'
FB_FIC_NO_1['Nombre_Campaña'] = FB_FIC_NO.llave_facebook

FIC_FB_NO_1 = FIC_FB_NO.llave_ventas.str.split("_", 10,expand = True)
FIC_FB_NO_1.columns = ["Año-Mes","Cliente","Marca","Tipo-1","Tipo-2",""]
FIC_FB_NO_1['archivo'] = 'FIC'
FIC_FB_NO_1['Nombre_Campaña'] = FIC_FB_NO.llave_ventas

Union.append(FB_FIC_NO_1)
Union.append(FIC_FB_NO_1)
Union = pd.concat(Union)

Union["Nombre_Campaña"] = Union["Nombre_Campaña"].str.replace("_FB","")

Union.archivo.value_counts()

#Desglose por cliente
OD = Union.loc[ Union.Cliente.str.contains('od', na = False) & ~Union.Cliente.str.contains('sodexo', na = False)]
RS = Union.loc[ Union.Cliente.str.contains('rs', na = False)]
THS = Union.loc[ Union.Cliente.str.contains('ths', na = False)]
PETCO = Union.loc[ Union.Cliente.str.contains('petco', na = False)]
GICSA = Union.loc[ Union.Cliente.str.contains('gicsa', na = False)]
GWEP = Union.loc[ Union.Cliente.str.contains('gwep', na = False)]

OD.shape[0] + RS.shape[0] + THS.shape[0] + PETCO.shape[0] + GICSA.shape[0] + GWEP.shape[0]

OTROS = Union.loc[ ~Union.Cliente.str.contains('od', na = False) & ~Union.Cliente.str.contains('rs', na = False) & ~Union.Cliente.str.contains('sodexo', na = False) & ~Union.Cliente.str.contains('ths', na = False) &
                  ~Union.Cliente.str.contains('petco', na = False) & ~Union.Cliente.str.contains('gicsa', na = False) & ~Union.Cliente.str.contains('gicsa', na = False) & ~Union.Cliente.str.contains('gwep', na = False)]



#Base_ROAS = pd.concat([Facebook, Adwords, Adform], axis = 0)

#Base_ROAS.plataforma.value_counts()

######################
#Exportación a Sheets#
######################
#Colocar la base completa en sheets
#   - Validar que no se puede colocar un archivo repetido
#   - 

