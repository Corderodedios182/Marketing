import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe, get_as_dataframe
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import logging

def get_auth(secrets_file):
    scope = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive.file',
            'https://www.googleapis.com/auth/drive']

    creds = ServiceAccountCredentials.from_json_keyfile_name(secrets_file, scope)

    try:
        client = gspread.authorize(creds)
        logging.info('Authentication succedd')

    except Exception as e:
        logging.exception('The following error happend when trying to authenticate: ')
        exit(1)

    return client


def get_sheets_file(client, file_name, sheet_name, skip_rows= 0): #, secrets_file):

    # 1. Read sheet file from drive 
    # 2. Create Pandas dataframe and skip rows
    # 3. Set the headers
    # 4. Return pandas dataframe

    try:
        spreadsheet = client.open(file_name)
        sheet = spreadsheet.worksheet(sheet_name)
        logging.info("The file '{}' was successfully accessed".format(file_name))

    except Exception as e:
        logging.exception('The following error happend when trying to access the file: ')
        exit(1)
    
    raw_data = pd.DataFrame(sheet.get_all_values()[skip_rows:])
    headers = raw_data.iloc[0]
    raw_df = raw_data[1:]
    raw_df.columns = headers
    raw_df = raw_df[raw_df.iloc[:,0] != '']
    df_shape = raw_df.shape
    logging.info('File loaded with {} rows and {} columns.'.format(df_shape[0], df_shape[1]))

    return raw_df


def output_format(input_df, source, columns_file, columns_new, to_date, to_numeric):

    # 0. Replace column names data frame
    # 1. Convert headers to lower case
    # 2. Select columns
    # 3. Format columns to date
    # 4. Format columns to numeric and fill NA with 0 
    # 5. Return pandas dataframe
    
    input_df["fuente"] = source
    
    zip_iterator = zip(columns_file, columns_new)
    a_dictionary = dict(zip_iterator)
    input_df.rename(columns=a_dictionary, inplace=True)

    input_df.columns = map(str.lower, input_df.columns)
    formatted_df = input_df.loc[:, columns_new]

    for column in to_date:
        if column in formatted_df.columns:
            formatted_df[column] = (pd.to_datetime(formatted_df[column])).dt.strftime('%Y-%m-%d')
        else:
            logging.error("The column name '{}' was not found".format(column))
    
    for column in to_numeric:
        if column in formatted_df.columns:
            formatted_df[column] = (pd.to_numeric(formatted_df[column].str.replace(',', ''), errors = 'coerce').fillna(0).astype(float))
        else:
            logging.error("The column name '{}' was not found".format(column))

    return formatted_df

def master_format(facebook, google_ads, analytics):
    
    result = pd.concat([facebook, google_ads])
    result = result.fillna(0)
    
    """Etiquetado de datos, agrupaciones, campos calculados especiales"""    
    
    result.loc[(result['plataforma_reporte'].str.contains('audience_network')) | (result['plataforma_reporte'].str.contains('messenger')) , 'plataforma_reporte'] = 'facebook'
    result.loc[result['plataforma_reporte'] == 0, 'plataforma_reporte'] = 'google ads'
    result = result.groupby(['plataforma_reporte', 'campaña', 'grupo_de_anuncios', 'anuncio', 'fecha','moneda'], as_index = False).sum()

    a = result.groupby(["plataforma_reporte","campaña","grupo_de_anuncios","anuncio","fecha"]).agg({'dinero_gastado': 'sum'})
    a = a.groupby(["campaña","grupo_de_anuncios","anuncio","fecha"]).apply(lambda x: x / float(x.sum())).reset_index().rename(columns = {"dinero_gastado":"porcentaje_dinero_gastado"})
    result = pd.merge(result, a, on = ["plataforma_reporte","campaña","grupo_de_anuncios","anuncio","fecha"])
    
    analytics = analytics.fillna('')
    analytics.campaña = analytics.campaña.apply(lambda x: str(x).replace("(not set)",""))
    analytics.grupo_de_anuncios = analytics.grupo_de_anuncios.apply(lambda x: str(x).replace("(not set)",""))
    analytics.anuncio = analytics.anuncio.apply(lambda x: str(x).replace("(not set)",""))
    analytics = analytics.groupby(["campaña","grupo_de_anuncios","anuncio","fecha"], as_index = False).sum()
    
    #--Cruzes de Informacion Facebook, Google con Analytics--#
    tmp_f = pd.merge(result[result.plataforma_reporte != 'google ads'], analytics, how = 'left', on = ['campaña','anuncio','fecha'])
    tmp_f = tmp_f.fillna(0)
    tmp_f = tmp_f.loc[:,['plataforma_reporte', 'campaña', 'grupo_de_anuncios_x', 'anuncio', 'fecha','moneda', 'clics', 'impresiones', 'dinero_gastado', 'views','interacciones', 'alcance', 'porcentaje_dinero_gastado','ingresos', 'duracion_sesion', 'sesiones','usuarios', 'usuarios_nuevos','rebotes', 'paginas_vistas']]
    tmp_f.columns = ['plataforma_reporte', 'campaña', 'grupo_de_anuncios', 'anuncio', 'fecha','moneda', 'clics', 'impresiones', 'dinero_gastado', 'views','interacciones', 'alcance', 'porcentaje_dinero_gastado','ingresos', 'duracion_sesion', 'sesiones','usuarios', 'usuarios_nuevos','rebotes', 'paginas_vistas']
    
    #Tenemos duplicados por los de analytics, se debe agrupar solo por campaña y grupo de anuncios
    analytics.anuncio = ''
    analytics = analytics.groupby(["campaña","grupo_de_anuncios","anuncio","fecha"], as_index = False).sum()
    
    tmp_a = pd.merge(result[result.plataforma_reporte == 'google ads'], analytics, how = 'left', on = ['campaña','grupo_de_anuncios','fecha'])
    tmp_a = tmp_a.fillna(0)
    tmp_a = tmp_a.loc[:,['plataforma_reporte', 'campaña', 'grupo_de_anuncios', 'anuncio_y', 'fecha',
                         'moneda', 'clics', 'impresiones', 'dinero_gastado', 'views',
                         'interacciones', 'alcance', 'porcentaje_dinero_gastado',
                         'ingresos', 'duracion_sesion', 'sesiones', 'usuarios',
                         'usuarios_nuevos', 'rebotes', 'paginas_vistas']]
    tmp_a.columns = ['plataforma_reporte', 'campaña', 'grupo_de_anuncios', 'anuncio', 'fecha',
                     'moneda', 'clics', 'impresiones', 'dinero_gastado', 'views',
                     'interacciones', 'alcance', 'porcentaje_dinero_gastado',
                     'ingresos', 'duracion_sesion', 'sesiones', 'usuarios',
                     'usuarios_nuevos', 'rebotes', 'paginas_vistas']
    
    master_df = pd.concat([tmp_f, tmp_a])
    
    #Distribuir las metricas de Analytics de acuerdo al porcentaje de dinero Gastado, sobre todo para Facebook que tiene campañas de Instagram y Facebook
    master_df["ingresos_validacion"] = master_df.ingresos
    master_df.ingresos = (master_df.porcentaje_dinero_gastado) * master_df.ingresos
    master_df.duracion_sesion = (master_df.porcentaje_dinero_gastado) * master_df.duracion_sesion
    master_df.sesiones = (master_df.porcentaje_dinero_gastado) * master_df.sesiones
    master_df.usuarios = (master_df.porcentaje_dinero_gastado) * master_df.usuarios
    master_df.usuarios_nuevos = (master_df.porcentaje_dinero_gastado) * master_df.usuarios_nuevos
    master_df.rebotes = (master_df.porcentaje_dinero_gastado) * master_df.rebotes
    master_df.paginas_vistas = (master_df.porcentaje_dinero_gastado) * master_df.paginas_vistas
    
    #Abriendo la Nomenclatura
    tmp_1 = master_df.loc[:,'campaña'].str.split("-",20,expand = True)
    cols = ["unidad_de_negocio", "plataforma", "campaña", "subcampaña","fecha_inicio","fecha_fin","estrategia","objetivo","concatenar","concatenar","concatenar","concatenar","concatenar"]
    tmp_1.columns = cols
    
    tmp_2 = master_df.loc[:,'grupo_de_anuncios'].str.split("-",20,expand = True)
    cols = ["tipo_de_formato", "provedor_de_medio", "tipo_audiencia", "nombre_audiencia","concatenar"]
    tmp_2.columns = cols
    
    tmp_3 = master_df.loc[:,'anuncio'].str.split("-",20,expand = True)
    cols = ["tipo_audiencia", "nombre_audiencia", "formato", "creativo", "dimension"]
    tmp_3.columns = cols
    
    master_df = pd.concat([tmp_1,tmp_2,tmp_3,master_df], axis = 1)
    
    master_df['ultima_actualizacion'] = datetime.now()
    
    return master_df 


def write_to_sheets(client, file_name, sheet_name, input_df):

    # 1. Open the specified google sheet (file_name, sheet_name)
    # 2. Append input_df to sheet 
    # 3. Write to google sheet

    sheet = client.open(file_name).worksheet(sheet_name)
    try:
        current_df = get_as_dataframe(sheet)
        updated_df = current_df.append(input_df, sort= True)
        set_with_dataframe(sheet, updated_df, include_column_header= True)
    except Exception as e:
        logging.exception('The following error happend while trying to write: ')
        exit(1)

def main():
    #To fix: the file must have headers for the 1st run
    #To add: log file | convert xlsx to spreadsheet

    logging.basicConfig(level=logging.DEBUG)
    secrets_file = 'C:/Users/crf005r/Documents/3_GitHub/api_service_secrets.json' #path to secrets file
    output_file_name = 'Master Welchs'
    output_sheet_name = 'master_2'

    config_values = {
        'Analytics': {
            'file_name': 'Google Analytics',
            'sheet_name': 'Conjunto de datos1', 
            'source':'analytics',
            'columns_file': ["fuente","Campaña", "Contenido del anuncio", "Google Ads: grupo de anuncios", "Fecha", "Sesiones", "Usuarios", "Usuarios nuevos", "Rebotes", "Transacciones", "Ingresos", "Duración de la sesión", "Número de visitas a páginas"],
            'columns_new': ["fuente","campaña", "anuncio", "grupo_de_anuncios", "fecha", "ingresos", "duracion_sesion", "sesiones", "usuarios", "usuarios_nuevos", "rebotes","paginas_vistas"],
            'columns_to_date': ['fecha'],
            'columns_to_numeric': ["ingresos", "duracion_sesion", "sesiones", "usuarios", "usuarios_nuevos", "rebotes","paginas_vistas"],
            'skip_rows': 0,
            'output_sheet_name': 'analytics'
            },
        'Google Ads': {
            'file_name': 'Google Ads Plataforma',
            'sheet_name': 'Google Ads Plataforma',
            'source':'google ads',
            'columns_file': ["fuente","Campaña", "Grupo de anuncios", "Día", "Moneda", "Clics", "Impresiones", "Costo", "Vistas"],
            'columns_new': ["fuente","campaña", "grupo_de_anuncios", "fecha", "moneda", "clics", "impresiones", "dinero_gastado","views"],
            'columns_to_date': ['fecha'],
            'columns_to_numeric': ["clics", "impresiones", "dinero_gastado","views"],
            'skip_rows': 2,
            'output_sheet_name': 'google_ads'
            },
        'Facebook': {
            'file_name': 'Facebook',
            'sheet_name': 'Raw',
            'source':'facebook',
            'columns_file': ["fuente","Plataforma", "Nombre de la campaña", "Nombre del conjunto de anuncios", "Nombre del anuncio", "Día", "Divisa", "Clics en el enlace", "Impresiones", "Importe gastado (MXN)", "Reproducciones de video hasta el 100%", "Interacción con una publicación", "Alcance"],
            'columns_new': ["fuente","plataforma_reporte", "campaña", "grupo_de_anuncios", "anuncio", "fecha", "moneda", "clics", "impresiones", "dinero_gastado","views", "interacciones","alcance"],
            'columns_to_date': ['fecha'],
            'columns_to_numeric': ["clics", "impresiones", "dinero_gastado","views", "interacciones","alcance"],
            'skip_rows': 0,
            'output_sheet_name': 'facebook'
            }
    }
    
    input_source = ['Facebook','Google Ads','Analytics']
    data = []
    
    client = get_auth(secrets_file)

    for input_source in input_source:
        
        raw_df = get_sheets_file(client, 
                                 config_values[input_source]['file_name'], 
                                 config_values[input_source]['sheet_name'], 
                                 config_values[input_source]['skip_rows'])
        
        #les da un adecuado formato a cada archivo#
        formatted_df = output_format(raw_df, 
                                     config_values[input_source]['source'],
                                     config_values[input_source]['columns_file'], 
                                     config_values[input_source]['columns_new'],
                                     config_values[input_source]['columns_to_date'],
                                     config_values[input_source]['columns_to_numeric'])
        
        data.append(formatted_df)
    
    #realiza las transformaciones y uniones de los datos
    master_df = master_format(facebook = data[0], google_ads = data[1], analytics = data[2])
    
    master_df.to_csv('master_2_python.csv')
    
    write_to_sheets(client, 
                    output_file_name, 
                    output_sheet_name, 
                    master_df)

    logging.info('Successful execution')

if __name__ == '__main__':
    main()


