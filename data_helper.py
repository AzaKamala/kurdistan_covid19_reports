import pandas as pd

# this html variable is for the info section
html = '<div><h2 style="text-align: center;">{} Report</h2><h4>Active Cases: {}</h4><h4>New Cases Per Day: {}</h4><h4>Recoveries Per day: {}</h4><h4>Deaths Per day: {}</h4></div>'

tableStyle = [
    dict(
        selector='',
        props=[('border-collapse', 'collapse')]
    ),
    dict(
        selector='thead tr',
        props=[
            ('background-color', 'gray'),
            ('color', 'white'),
            ('font-wieght', 'bold')
        ]
    ),
    dict(
        selector='th, td',
        props=[
            ('padding', '5px 8px'),
            ('text-align', 'center')
        ]
    ),
    dict(
        selector='tbody tr',
        props=[('border-bottom', '1px solid #f5f5f5')]
    ),
    dict(
        selector='tbody tr:nth-of-type(even)',
        props=[('background-color', '#f1f1f1')]
    ),
    dict(
        selector='tbody tr:hover',
        props=[('background-color', '#ddedfd')]
    ),
    dict(
        selector='tbody tr:last-of-type',
        props=[('border-bottom', '2px solid gray')]
    )
]

def changeIndexToDate(dataframe):
    dataframe['Month & Year'] = dataframe.Date
    dataframe['Day'] = dataframe.Date
    dataframe['Month & Year'] = dataframe['Month & Year'].apply(lambda x: x.strftime('%B %Y'))
    dataframe['Day'] = dataframe['Day'].apply(lambda x: x.day)
    dataframe = dataframe.drop('Date', axis=1)
    dataframe = dataframe.set_index(['Month & Year', 'Day'])
    return dataframe

def formatGovernorateData(dataframe):
    columns = [
        'Male',
        'Female',
        'Age0To19',
        'Age20To29',
        'Age30To39',
        'Age40To49',
        'Age50To59',
        'Age60To69',
        'Age70OrMore',
        'TotalConfirmedCases',
        'TotalRecovered',
        'TotalDeaths',
        'ActiveCases'
    ]
    dataframe = dataframe.drop(columns, axis=1)
    dataframe = dataframe.rename(columns={'TotalNewCases': 'New Cases'})

    dataframe = changeIndexToDate(dataframe)

    dataframe = dataframe.reindex(index=dataframe.index[::-1])
    return dataframe

def formatSummaryData(dataframe):
    columns = [
        'RunningSum',
        'Active',
    ]
    dataframe = dataframe.drop(columns, axis=1)

    dataframe = changeIndexToDate(dataframe)

    dataframe = dataframe.reindex(index=dataframe.index[::-1])
    return dataframe

def renderCityHtml(dataframe):
    return dataframe.style.set_table_styles(tableStyle).applymap(
        lambda x: 'color: ' + ('#ff5252' if x >= (dataframe['New Cases'].mean() / 2) and x < dataframe['New Cases'].mean() else 'red' if x >= dataframe['New Cases'].mean() else 'black'),
        subset=pd.IndexSlice[:, ['New Cases', 'Deaths']]
    ).applymap(
        lambda x: 'color: ' + ('#65b866' if x >= (dataframe['New Cases'].mean() / 2) and x < dataframe['New Cases'].mean() else '#018003' if x >= dataframe['New Cases'].mean() else 'black'),
        subset=pd.IndexSlice[:, ['Recovered']]
    ).render()

def renderSummaryHtml(dataframe):
    return dataframe.style.set_table_styles(tableStyle).applymap(
        lambda x: 'color: ' + ('#ff5252' if x >= (dataframe['Total'].mean() / 2) and x < dataframe['Total'].mean() else 'red' if x >= dataframe['Total'].mean() else 'black'),
        subset=pd.IndexSlice[:, ['Erbil', 'Sulaymani', 'Halabja', 'Duhok', 'Deaths']]
    ).applymap(
        lambda x: 'color: ' + ('#65b866' if x >= (dataframe['Total'].mean() / 2) and x < dataframe['Total'].mean() else '#018003' if x >= dataframe['Total'].mean() else 'black'),
        subset=pd.IndexSlice[:, ['Recovered']]
    ).render()

def getCityInfo(cityName, dataframe):
    return html.format(cityName.title(), int(dataframe.loc[len(dataframe)-1, ['ActiveCases']]), round(dataframe['TotalNewCases'].mean()), round(dataframe['Recovered'].mean()), round(dataframe['Deaths'].mean()))

def getSummaryInfo(dataframe):
    return html.format('Summary', int(dataframe.loc[len(dataframe)-1, ['Active']]), round(dataframe['Total'].mean()), round(dataframe['Recovered'].mean()), round(dataframe['Deaths'].mean()))