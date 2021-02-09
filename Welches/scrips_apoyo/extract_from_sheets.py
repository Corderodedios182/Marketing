import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
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
        logging.error('The following error happend when trying to authenticate: {}'.format(e))
        exit(1)

    return client


def get_sheets_file(client, file_name, sheet_name, skip_rows= 0): #, secrets_file):
    
    try:
        spreadsheet = client.open(file_name)
        sheet = spreadsheet.worksheet(sheet_name)
        logging.info("The file '{}' was successfully accessed".format(file_name))

    except Exception as e:
        logging.error('The following error happend when trying to access the file: {}'.format(e))
        exit(1)
    
    raw_data = pd.DataFrame(sheet.get_all_values()[skip_rows:])
    headers = raw_data.iloc[0]
    raw_df = raw_data[1:]
    raw_df.columns = headers
    df_shape = raw_df.shape
    logging.info('File loaded with {} rows and {} columns.'.format(df_shape[0], df_shape[1]))

    return raw_df


def output_format(input_df, column_names, to_date):
    formatted_df = input_df.loc[:, column_names]

    for column in to_date:
        if column in formatted_df.columns:
            formatted_df[column] = (pd.to_datetime(formatted_df[column])).dt.strftime('%d/%m/%Y')
        else:
            logging.error("The column name '{}' was not found".format(column))

    return formatted_df


def write_to_sheets(client, file_name, sheet_name, input_df):

    spreadsheet = client.open(file_name)
    sheet = spreadsheet.worksheet(sheet_name)
    current_rows_len = len(sheet.get_all_values())
    try:
        set_with_dataframe(sheet, input_df, include_column_header=True, row= current_rows_len + 1)
    except Exception as e:
        logger.error('The following error happend while trying to write: {}'.format(e))
        exit(1)


def main():
    secrets_file = './welches-5291fb1d6517.json'
    ads_file_name = 'Google Ads Plataforma'
    ads_sheet_name = 'Google Ads Plataforma'
    ads_pfm_columns = ['Campaña','Grupo de anuncios','Día','Moneda','Clics','Impresiones','Costo','Video reproducido al 100%']
    ads_pfm_date = ['Día']
    ads_pfm_skip_rows = 2
    ads_pfm_output_file_name = 'Master Welchs'
    ads_pfm_output_sheet_name= 'Google_ads_pfm'

    client = get_auth(secrets_file)
    raw_df = get_sheets_file(client, ads_file_name, ads_sheet_name, ads_pfm_skip_rows)
    formatted_df = output_format(raw_df, ads_pfm_columns, ads_pfm_date)
    write_to_sheets(client, ads_pfm_output_file_name, ads_pfm_output_sheet_name, formatted_df)
    logger.info('Successful execution')

if __name__ == '__main__':
    main()


