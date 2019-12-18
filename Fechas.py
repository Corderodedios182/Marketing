import numpy as np

Base_master = []

Base_master.Nombre_Campaña.value_counts()

tmp = Base_master[Base_master.Nombre_Campaña == '1901_OD_Payclip_SEM']

tmp = Base_master.groupby(['Nombre_Campaña','t_fecha_fin','t_fecha_inicio','t_fecha_inicio_reporte','t_fecha_fin_reporte']).count()


tmp = Base_master[(Base_master.Plataforma == 'Facebook') & (Base_master.Marca == 'Office Depot MEX')]


tmp = Base_master[(Base_master.Plataforma == 'Facebook') & (Base_master.Marca == 'Office Depot MEX') & (Base_master.t_fecha_inicio_reporte == '2019-01-01' )]

tmp_0 = Base_master[(Base_master.Nombre_Campaña == '1901_OD_3M-BTS_FB')]



len(tmp.Nombre_Campaña.value_counts())


Base_master.groupby(['Plataforma']).count()


tmp_1 = Base_master_final

tmp = tmp_1[(tmp_1.Plataforma == 'Facebook') & (tmp_1.Marca == 'Office Depot MEX') & (tmp_1.t_fecha_inicio_reporte == '2019-01-01' )]


Base_master


#Fecha inicio reporte
def fechas_inicio(x,y):
    if x <= y:
        return y
    else:
        return x
    
Base_master['inicio'] = [fechas_inicio(x,y) for x, y in zip(Base_master.t_fecha_inicio_reporte,Base_master.t_fecha_inicio)] #Este es el bueno

#Fecha fin reporte
def fechas_fin(x,y):
    if x <= y:
        return x
    else:
        return y
    
Base_master['fin'] = [fechas_fin(x,y) for x, y in zip(Base_master.t_fecha_fin_reporte,Base_master.t_fecha_fin)] #Este es el bueno

Base_master['dias'] = Base_master.fin - Base_master.inicio

#Tengo días negativos

#Columna mes
Base_master['Mes'] = Base_master.inicio.apply(lambda x : x.month)



#¿Que regla debo tener para mantener cierta fecha de inicio y fin?

#Validacion
tmp_1 = Base_master.groupby(['Nombre_Campaña','Mes','Marca','Plataforma'], as_index = False).sum()

tmp = tmp_1[(tmp_1.Plataforma == 'Facebook') & (tmp_1.Marca == 'Office Depot MEX') & (tmp_1.Mes == 1.0 )]


################################
#Pegar la información en sheets#
################################
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe #,get_as_dataframe

#Conexion con Google Sheets, usando las paqueterias gspread, oauth2client, gspread_dataframe
#Credenciales cred.json
os.chdir('/home/carlos/Documentos/Adsocial')
os.listdir()
#Autentificacion con google cloud platform correo analytics.adsocial@gmail.com
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)

#Exportacion de la informacion
sh = client.open('Copy of DASHBOARD GG - Reporte ROAS MES A MES') #Recordar que el archivo que deseamos leer tiene que tener el correo de la api como persona compartida
worksheet = sh.get_worksheet(1) #Base_master_python
set_with_dataframe(worksheet, Base_master_final)


#Pegar lo nuevo que se corra abajo de las info que ya esta creada
worksheet = sh.get_worksheet(2) #Union_Analytics_python


#Extraccion de datos sheets
#datos = worksheet.get_all_values()
#datos = pd.DataFrame(datos)

#Extraccion con get_as_dataframe
#df2 = get_as_dataframe(worksheet)
#df = get_as_dataframe(worksheet, parse_dates=True, usecols=[0,2], skiprows=1, header=None)

Mes	inicio dias	t_fecha_inicio_reporte	t_fecha_fin_reporte

tmp = Base_master[.Plataforma == 'Adform']
import os
os.getcwd()
Base_master_final.to_csv('base_master_final.csv')

#Fechas faltantes en Adform
#Modificar el archivo de Acumulado para que lea las fechas, no va a colocar las fechas por el nombre del archivo
tmp = Base_master_final[Base_master_final.Plataforma == 'Adform']

tmp_fechas = tmp.groupby(['inicio']).count()

#Filtros dianis





