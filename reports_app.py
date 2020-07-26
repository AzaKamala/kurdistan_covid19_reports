from spyre import server
import requests
import pandas as pd
import io
import datetime

links = [
    'https://raw.githubusercontent.com/DevelopersTree/Kovid19/master/data/governorates/erbil.csv',
    'https://raw.githubusercontent.com/DevelopersTree/Kovid19/master/data/governorates/sulaymaniyah.csv',
    'https://raw.githubusercontent.com/DevelopersTree/Kovid19/master/data/governorates/halabja.csv',
    'https://raw.githubusercontent.com/DevelopersTree/Kovid19/master/data/governorates/duhok.csv',
]

governorates = [
    'erbil',
    'sulaymani',
    'halabja',
    'duhok'
]

governorates_data = dict()
for i in range(4):
    response = requests.get(links[i])
    covid_df = pd.read_csv(io.StringIO(response.text), parse_dates=['Date'])
    governorates_data[governorates[i]] = covid_df

class SimpleApp(server.App):
    title = "Kurdistan Covid19 Reports"
    inputs = []

    tabs = ['Erbil', 'Sulaymani', 'Halabja', 'Duhok']

    outputs = [
        dict(
            type='table',
            id='getErbilTable',
            tab='Erbil',
            sortable=True,
        ),
        dict(
            type='table',
            id='getSulaymaniTable',
            tab='Sulaymani',
            sortable=True,
        ),
        dict(
            type='table',
            id='getHalabjaTable',
            tab='Halabja',
            sortable=True,
        ),
        dict(
            type='table',
            id='getDuhokTable',
            tab='Duhok',
            sortable=True,
        ),
    ]

    def getErbilTable(self, params):
        return governorates_data['erbil']

    def getSulaymaniTable(self, params):
        return governorates_data['sulaymani']

    def getHalabjaTable(self, params):
        return governorates_data['halabja']

    def getDuhokTable(self, params):
        return governorates_data['duhok']
    

app = SimpleApp()
app.launch()