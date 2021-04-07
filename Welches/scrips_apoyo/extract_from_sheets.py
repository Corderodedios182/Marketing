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
    df_shape = raw_df.shape
    logging.info('File loaded with {} rows and {} columns.'.format(df_shape[0], df_shape[1]))

    return raw_df


def output_format(input_df, column_names, to_date, to_numeric):

    # 1. Convert headers to lower case
    # 2. Select columns
    # 3. Format columns to date
    # 4. Format columns to numeric and fill NA with 0 
    # 5. Return pandas dataframe

    input_df.columns = map(str.lower, input_df.columns)
    formatted_df = input_df.loc[:, column_names]

    for column in to_date:
        if column in formatted_df.columns:
            formatted_df[column] = (pd.to_datetime(formatted_df[column])).dt.strftime('%Y/%m/%d')
        else:
            logging.error("The column name '{}' was not found".format(column))
    
    for column in to_numeric:
        if column in formatted_df.columns:
            formatted_df[column] = (pd.to_numeric(formatted_df[column].str.replace(',', '')).fillna(0))
        else:
            logging.error("The column name '{}' was not found".format(column))

    return formatted_df


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

def master_format(input_df, column_names, source):
    
    # 1. Column name mapping definition
    # 2. Create empty pandas dataframe with standar columns name -> master_df
    # 3. Column name mappign for input_df
    # 4. Append values from input_df to master_df
    # 5. Add column fuente
    # 6. Return pandas dataframe

    columns_map = {
        'fuente': [],
        'campaña': ['nombre de la campaña'],
        'grupo_de_anuncios': ['grupo de anuncios', 'nombre del conjunto de anuncios'],
        'anuncio': ['nombre del anuncio'],
        'fecha': ['fecha', 'día'],
        'moneda': ['divisa'],
        'clics': ['clics en el enlace'],
        'impresiones': [],
        'dinero_gastado': ['importe gastado (mxn)', 'costo', 'ingresos'],
        'duracion_sesion': ['duración de la sesión'],
        'sesiones': [],
        'usuarios': [],
        'usuarios_nuevos': ['usuarios nuevos'],
        'rebotes': [],
        'vistas': ['reproducciones de video hasta el 100%', 'vistas'],
        'visitas': ['número de visitas a páginas'] 
            }
    
    master_df = pd.DataFrame(columns= columns_map.keys())
    
    for column_name in input_df.columns:
        if column_name not in columns_map.keys():
            for item in columns_map.items():
                if column_name in item[1]:
                    input_df.rename(columns={column_name: item[0]}, inplace= True)

    master_df = master_df.append(input_df, sort= True)
    master_df['fuente'] = source

    return master_df 

def main():
    #To fix: the file must have headers for the 1st run
    #To add: log file | convert xlsx to spreadsheet

    logging.basicConfig(level=logging.DEBUG)
    secrets_file = '' #path to secrets file
    output_file_name = 'Master Welchs'
    output_sheet_name = 'master'

    config_values = {
        'Analytics': {
            'file_name': 'Analytics',
            'sheet_name': 'Raw', 
            'columns': ['campaña', 'google ads: grupo de anuncios', 'contenido del anuncio', 'fecha', 'ingresos', 'duración de la sesión', 'sesiones', 'usuarios', 'usuarios nuevos', 'rebotes', 'número de visitas a páginas'],
            'columns_to_date': ['fecha'],
            'columns_to_numeric': ['ingresos', 'sesiones', 'usuarios', 'usuarios nuevos', 'rebotes', 'número de visitas a páginas'],
            'skip_rows': 0,
            'output_sheet_name': 'analytics'
            },
        'Google Ads': {
            'file_name': 'Google Ads Plataforma',
            'sheet_name': 'Raw',
            'columns': ['campaña','grupo de anuncios','día','moneda','clics','impresiones','costo','vistas'],
            'columns_to_date': ['día'],
            'columns_to_numeric': ['clics', 'impresiones', 'costo', 'vistas'],
            'skip_rows': 2,
            'output_sheet_name': 'google_ads'
            },
        'Facebook': {
            'file_name': 'Facebook',
            'sheet_name': 'Raw',
            'columns': ['nombre de la campaña', 'nombre del conjunto de anuncios', 'nombre del anuncio', 'día', 'impresiones', 'divisa', 'importe gastado (mxn)', 'clics en el enlace', 'alcance', 'reproducciones de video hasta el 100%', 'interacción con una publicación'],
            'columns_to_date': ['día'],
            'columns_to_numeric': ['impresiones', 'importe gastado (mxn)', 'clics en el enlace', 'alcance', 'reproducciones de video hasta el 100%', 'interacción con una publicación'],
            'skip_rows': 0,
            'output_sheet_name': 'facebook'
            }
    }
    
    input_source = 'Google Ads'

    client = get_auth(secrets_file)

    raw_df = get_sheets_file(client, 
                             config_values[input_source]['file_name'], 
                             config_values[input_source]['sheet_name'], 
                             config_values[input_source]['skip_rows'])

    formatted_df = output_format(raw_df, 
                                 config_values[input_source]['columns'], 
                                 config_values[input_source]['columns_to_date'],
                                 config_values[input_source]['columns_to_numeric'])

    write_to_sheets(client, 
                    output_file_name, 
                    config_values[input_source]['output_sheet_name'], 
                    formatted_df)
    
    master_df = master_format(formatted_df,
                              config_values[input_source]['columns'],
                              input_source)
    
    write_to_sheets(client, 
                    output_file_name, 
                    output_sheet_name, 
                    master_df)

    logging.info('Successful execution')

if __name__ == '__main__':
    main()


