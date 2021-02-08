import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import logging

def get_sheets_file(file_name, sheet_name, skip_rows= 0, credentials_file):
    
    scope = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive.file',
            'https://www.googleapis.com/auth/drive']

    creds = ServiceAccountCredentials.from_json_keyfile_name(file_name, scope)

    try:
        client = gspread.authorize(creds)
        spreadsheet = client.open(file_name)
        sheet = spreadsheet.worksheet(sheet_name)
        logging.info('The file {} was successfully accessed'.format(file_name))

    except Exception as e:
        logging.error('The following error happend when trying to access the file: {}'.format(e))
        exit(1)
    
    raw_data = pd.DataFrame(sheet.get_all_values()[skip_rows:])
    headers = raw_data[0]
    raw_df = pd.DataFrame(raw_data[1:], columns= headers)

    return raw_df


def main():
    print(get_sheets_file('Master Welchs', 'Raw', './welches-5291fb1d6517.json'))


if __name__ == '__main__':
    main()


