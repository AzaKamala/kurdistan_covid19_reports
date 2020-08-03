from spyre import server
import requests
import pandas as pd
import io
import datetime
import data_helper

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
    title = "Kurdistan Covid-19 Reports"
    inputs = []

    tabs = ['Erbil', 'Sulaymani', 'Halabja', 'Duhok']

    outputs = [
        dict(
            type='html',
            id='getErbilInfo',
            tab='Erbil',
        ),
        dict(
            type='html',
            id='getErbilTable',
            tab='Erbil',
        ),
        dict(
            type='html',
            id='getSulaymaniInfo',
            tab='Sulaymani',
        ),
        dict(
            type='html',
            id='getSulaymaniTable',
            tab='Sulaymani',
        ),
        dict(
            type='html',
            id='getHalabjaInfo',
            tab='Halabja',
        ),
        dict(
            type='html',
            id='getHalabjaTable',
            tab='Halabja',
        ),
        dict(
            type='html',
            id='getDuhokInfo',
            tab='Duhok',
        ),
        dict(
            type='html',
            id='getDuhokTable',
            tab='Duhok',
        ),
    ]

    def getErbilInfo(self, params):
        return data_helper.getCityInfo('erbil', governorates_data['erbil'])

    def getErbilTable(self, params):
        data = data_helper.formatGovernorateData(governorates_data['erbil'])
        return data_helper.renderHtml(data)

    def getSulaymaniInfo(self, params):
        return data_helper.getCityInfo('sulaymani', governorates_data['sulaymani'])

    def getSulaymaniTable(self, params):
        data = data_helper.formatGovernorateData(governorates_data['sulaymani'])
        return data_helper.renderHtml(data)

    def getHalabjaInfo(self, params):
        return data_helper.getCityInfo('halabja', governorates_data['halabja'])

    def getHalabjaTable(self, params):
        data = data_helper.formatGovernorateData(governorates_data['halabja'])
        return data_helper.renderHtml(data)

    def getDuhokInfo(self, params):
        return data_helper.getCityInfo('duhok', governorates_data['duhok'])

    def getDuhokTable(self, params):
        data = data_helper.formatGovernorateData(governorates_data['duhok'])
        return data_helper.renderHtml(data)
    

app = SimpleApp()
app.launch()