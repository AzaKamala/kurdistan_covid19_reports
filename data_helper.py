import pandas as pd

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

    dataframe['Month & Year'] = dataframe.Date
    dataframe['Day'] = dataframe.Date
    dataframe['Month & Year'] = dataframe['Month & Year'].apply(lambda x: x.strftime('%B %Y'))
    dataframe['Day'] = dataframe['Day'].apply(lambda x: x.day)
    dataframe = dataframe.drop('Date', axis=1)

    dataframe = dataframe.set_index(['Month & Year', 'Day'])
    dataframe = dataframe.reindex(index=dataframe.index[::-1])
    return dataframe

def renderHtml(dataframe):
    return dataframe.style.set_table_styles([
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
    ]).applymap(
        lambda x: 'color: ' + ('#ff5252' if x >= (dataframe['New Cases'].mean() / 2) and x < dataframe['New Cases'].mean() else 'red' if x >= dataframe['New Cases'].mean() else 'black'),
        subset=pd.IndexSlice[:, ['New Cases', 'Deaths']]
    ).applymap(
        lambda x: 'color: ' + ('#65b866' if x >= (dataframe['New Cases'].mean() / 2) and x < dataframe['New Cases'].mean() else '#018003' if x >= dataframe['New Cases'].mean() else 'black'),
        subset=pd.IndexSlice[:, ['Recovered']]
    ).render()

