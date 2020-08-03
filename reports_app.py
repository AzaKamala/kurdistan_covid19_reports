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
            id='getSulaymaniTable',
            tab='Sulaymani',
        ),
        dict(
            type='html',
            id='getHalabjaTable',
            tab='Halabja',
        ),
        dict(
            type='html',
            id='getDuhokTable',
            tab='Duhok',
        ),
    ]

    def getErbilInfo(self, params):
        return '<div><h2>{} Reports</h2><h4>Active Cases: {}</h4><h4>New Cases Per Day: {}</h4><h4>Recoveries Per day: {}</h4><h4>Deaths Per day: {}</h4></div>'.format('Erbil', 0, 0, 0, 0)

    def getErbilTable(self, params):
        data = data_helper.formatGovernorateData(governorates_data['erbil'])
        return data_helper.renderHtml(data)

    def getSulaymaniTable(self, params):
        data = data_helper.formatGovernorateData(governorates_data['sulaymani'])
        return data_helper.renderHtml(data)

    def getHalabjaTable(self, params):
        data = data_helper.formatGovernorateData(governorates_data['halabja'])
        return data_helper.renderHtml(data)

    def getDuhokTable(self, params):
        data = data_helper.formatGovernorateData(governorates_data['duhok'])
        return data_helper.renderHtml(data)
    

app = SimpleApp()
app.launch()