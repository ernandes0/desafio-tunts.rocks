from google_sheets_manager import GoogleSheetsManager
from student import SpreadsheetReader, StudentCalculator, ResultsDisplay

google_sheets_manager = GoogleSheetsManager('1ceCeXbDGE9xANyFg5oyWs8ljCLDNnSOGF_je-fcF63s')

spreadsheet_reader = SpreadsheetReader(google_sheets_manager, 'engenharia_de_software')

spreadsheet_reader.read_data()

data = spreadsheet_reader.data

student_calculator = StudentCalculator(data)
student_calculator.calculate_situation()

results_display = ResultsDisplay(data)
results_display.display_results()

google_sheets_manager.write_data('engenharia_de_software', data)
