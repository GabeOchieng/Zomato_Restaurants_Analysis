import numpy as np
import pandas as pd
import plotly.offline as plt
import plotly.graph_objs as go
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
        text=df['Highest Rated Restaurant']
    )
    trace2 = go.Bar(
        x=df['City'],
        y=df['Lowest Rating'],
        name='Lowest Rating',
        text=df['Lowest Rated Restaurant']
    )

    d = [trace1, trace2]
    layout = go.Layout(
        barmode='group',
    )

    fig = go.Figure(data=d, layout=layout)
    plt.plot(fig, filename='../plots/max_min_rating')


def restaurants_density(country, write_csv=False):
    country_restaurants = data[data['Country Code'] == country_code[country]]
    density = country_restaurants.groupby('City', as_index=False).agg({'Restaurant Name': np.count_nonzero})
    print(density)


def cuisine(country):
    df = data['Cuisines'].unique()
    print(df)
    # cuisines = data[data['Country Code'] == country_code['Australia']]
    # cuisines = cuisines.groupby('Cuisines', as_index=False).agg({'Restaurant Name': np.count_nonzero})
    # print(cuisines.sort_values(['Restaurant Name'], ascending=False))


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
    df = data2.groupby('Price range', as_index=False).agg({'Restaurant Name': 'count'})
    print(df)


if __name__ == '__main__':
    print(data[data['Aggregate rating'] > 3])
    # text_rating_plotting(text_rating_analysis())
    # max_min_rating_plotting(max_min_rating_city_wise('India'))
