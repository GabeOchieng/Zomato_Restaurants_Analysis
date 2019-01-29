import numpy as np
import pandas as pd
import plotly.offline as plt
import plotly.graph_objs as go
from plotly import tools
import warnings

warnings.filterwarnings("ignore")
pd.set_option('display.max_columns', 21)
data = pd.read_csv('../data/zomato_restaurants.csv')
country_code = {
    'India': 1,
    'Australia': 14,
    'Brazil': 30,
    'Canada': 37,
    'Indonesia': 94,
    'New Zealand': 148,
    'Phillipines': 162,
    'Qatar': 166,
    'Singapore': 184,
    'South Africa': 189,
    'Sri Lanka': 191,
    'Turkey': 208,
    'UAE': 214,
    'United Kingdom': 215,
    'United States': 216
}


def max_min_rating_city_wise(country, write_csv=False):
    country_restaurants = data[data['Country Code'] == country_code[country]]
    min_max_rating = pd.DataFrame()
    country_restaurants.sort_values(['Aggregate rating', 'City'], ascending=False, inplace=True)
    min_max_rating['City'] = np.unique(country_restaurants['City'])
    country_restaurants = country_restaurants.groupby(['City'], as_index=False)  # additional argument -> sort = True
    min_max_rating['Highest Rated Restaurant'] = country_restaurants.first()['Restaurant Name']
    min_max_rating['Highest Rating'] = country_restaurants.first()['Aggregate rating']
    min_max_rating['Lowest Rated Restaurant'] = country_restaurants.last()['Restaurant Name']
    min_max_rating['Lowest Rating'] = country_restaurants.last()['Aggregate rating']
    if write_csv:
        min_max_rating.to_csv("../data/max_min_rating.csv", index=False, index_label=False)
    return min_max_rating


def max_min_rating_plotting(df):
    trace1 = go.Bar(
        x=df['City'],
        y=df['Highest Rating'],
        name='Highest Rating',
        text=df['Highest Rated Restaurant'],
    )
    trace2 = go.Bar(
        x=df['City'],
        y=df['Lowest Rating'],
        name='Lowest Rating',
        text=df['Lowest Rated Restaurant'],
    )

    d = [trace1, trace2]
    layout = go.Layout(
        barmode='group',
    )

    fig = go.Figure(data=d, layout=layout)
    plt.plot(fig, filename='../output_files/max_min_rating_horizontal.html')


def restaurants_density(country, write_csv=False):
    country_restaurants = data[data['Country Code'] == country_code[country]]
    density = country_restaurants.groupby('City', as_index=False).agg({'Restaurant Name': np.count_nonzero})
    print(density)


def cuisine(country):
    df = data['Cuisines'].unique()
    print(df)


def text_rating_analysis():
    return data.groupby('Rating text', as_index=False).agg({'Aggregate rating': np.mean})


def text_rating_plotting(df):
    labels = df['Rating text']
    values = df['Aggregate rating']
    trace = go.Pie(labels=labels, values=values)

    plt.plot([trace], filename='../plots/text_rating_plotting')


def rating_color_analysis():
    df = data.groupby('Rating color').agg({'Aggregate rating': np.mean})
    print(df)


def price_range(country):
    data2 = data[data['Country Code'] == country_code[country]]
    data2 = data2.drop_duplicates(subset='Restaurant Name', keep='last')
    # df = data2.sort_values(['Price range', 'Aggregate rating'], ascending=False).groupby('Price range')
    df = data2.sort_values(['Price range', 'Aggregate rating'], ascending=[True, False]).groupby('Price range')
    return df.head(10)


def price_range_plotting(df):
    df1 = df[df['Price range'] == 1]
    df2 = df[df['Price range'] == 2]
    df3 = df[df['Price range'] == 3]
    df4 = df[df['Price range'] == 4]

    trace1 = go.Bar(y=df1['Aggregate rating'], x=df1['Restaurant Name'], xaxis='x1', yaxis='y1', name='Price Range: 1')
    trace2 = go.Bar(y=df2['Aggregate rating'], x=df2['Restaurant Name'], xaxis='x2', yaxis='y2', name='Price Range: 2')
    trace3 = go.Bar(y=df3['Aggregate rating'], x=df3['Restaurant Name'], xaxis='x3', yaxis='y3', name='Price Range: 3')
    trace4 = go.Bar(y=df4['Aggregate rating'], x=df4['Restaurant Name'], xaxis='x4', yaxis='y4', name='Price Range: 4')

    fig = tools.make_subplots(rows=2, cols=2, subplot_titles=('1', '2', '3', '4'))

    fig.append_trace(trace1, 1, 1)
    fig.append_trace(trace2, 1, 2)
    fig.append_trace(trace3, 2, 1)
    fig.append_trace(trace4, 2, 2)

    fig['layout'].update(height=1200, width=1000, title='Restaurants with Highest Aggregate Rating for all Price Ranges',
                         margin=go.layout.Margin(l=50, r=65, b=150, t=150), showlegend=False,
                         font=dict(family='Times New Roman, monospace', size=14, color='#000000'))

    plt.plot(fig, filename='price_range.html')


if __name__ == '__main__':
    # max_min_rating_plotting(max_min_rating_city_wise('India'))
    price_range_plotting(price_range('India'))
