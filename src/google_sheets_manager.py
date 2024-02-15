import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

class GoogleSheetsManager:
    def __init__(self, spreadsheet_key):
        self.scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name('config/credentials.json', self.scope)
        self.gc = gspread.authorize(self.credentials)
        self.spreadsheet_key = spreadsheet_key
        self.sheet = None

    def connect(self):
        try:
            self.sheet = self.gc.open_by_key(self.spreadsheet_key)
            return True
        except Exception as e:
            print(f"Error connecting to the Google Sheet: {e}")
            return False

    def read_data(self, sheet_name, start_row=3, expected_headers=None):
        if self.sheet:
            worksheet = self.sheet.worksheet(sheet_name)
            data = worksheet.get_all_values()
            headers = data[start_row - 1]
            
            if expected_headers:
                assert headers == expected_headers, "Unexpected headers in the worksheet."
                
            data = data[start_row:]
            df = pd.DataFrame(data, columns=headers)
            print(df)
            
            return df
        else:
            print("Not connected to the Google Sheet.")
            return None

    def write_data(self, sheet_name, data, start_row=4):
        if self.sheet:
            worksheet = self.sheet.worksheet(sheet_name)
            existing_data = worksheet.get_all_records(head=start_row-1)
        
            for idx, row in enumerate(existing_data):
                if row['Situação'] == '' or row['Nota para Aprovação Final'] == '':
                    if row['Situação'] == '':
                        worksheet.update_cell(start_row + idx, data.columns.get_loc('Situação') + 1, data.at[idx, 'Situação'])
                    
                    if row['Nota para Aprovação Final'] == '':
                        worksheet.update_cell(start_row + idx, data.columns.get_loc('Nota para Aprovação Final') + 1, int(data.at[idx, 'Nota para Aprovação Final']))
        
            print("Data written successfully to the Google Sheet.")
        else:
            print("Not connected to the Google Sheet.")


##google_sheets_manager = GoogleSheetsManager('1ceCeXbDGE9xANyFg5oyWs8ljCLDNnSOGF_je-fcF63s')
##google_sheets_manager.connect()
##data = google_sheets_manager.read_data('engenharia_de_software')
