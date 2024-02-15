import numpy as np
import pandas as pd

from google_sheets_manager import GoogleSheetsManager

class SpreadsheetReader:
    def __init__(self, google_sheets_manager, sheet_name):
        self.manager = google_sheets_manager
        self.sheet_name = sheet_name
        self.data = None

    def read_data(self):
        if self.manager.connect():
            self.data = self.manager.read_data(self.sheet_name)
            print("Data loaded successfully from the Google Sheet.")
            print("Columns in the DataFrame:", self.data.columns)
        else:
            print("Failed to load data from the Google Sheet.")

class StudentCalculator:
    def __init__(self, data):
        self.data = data

    def calculate_situation(self):
        self.data['Faltas'] = pd.to_numeric(self.data['Faltas'], errors='coerce')

        self.data[['P1', 'P2', 'P3']] = self.data[['P1', 'P2', 'P3']].apply(pd.to_numeric, errors='coerce')

        self.data['Average'] = self.data[['P1', 'P2', 'P3']].mean(axis=1)
        

        self.data['Situação'] = np.where(self.data['Faltas'] > 0.25 * 60, 'Reprovado por Falta',
                                          np.where(self.data['Average'] < 50, 'Reprovado por Nota',
                                                   np.where((self.data['Average'] >= 50) & (self.data['Average'] < 70), 'Exame Final',
                                                            'Aprovado')))

        self.data['Nota para Aprovação Final'] = np.where(self.data['Situação'] == 'Exame Final',
                                                      np.ceil(100 - self.data['Average']).astype(int), 0)


# src/results_display.py
class ResultsDisplay:
    def __init__(self, data):
        self.data = data

    def display_results(self):
        print("\nResults:")
        print(self.data[['Matricula', 'Aluno', 'Faltas', 'P1', 'P2', 'P3', 'Situação', 'Nota para Aprovação Final']])