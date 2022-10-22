import pandas as pd
import plotly_express as px
import streamlit as st

pd.options.mode.chained_assignment = None

st.set_page_config(
    page_title = "Recensioni Film",
    page_icon = ":film_frames:",
    layout = "wide"
)

localfile = "imdb_top_1000.csv"
def get_dataset():
    df = pd.read_csv(localfile)
    df['Gross'] = df['Gross'].str.replace(',','')
    df['Gross'] = df['Gross'].astype(float)
    df.drop(labels = ['Poster_Link','Certificate'], axis = 1, inplace = True)
    df = df[df['Gross'].notna() & df['Meta_score'].notna()]
    return df

df = get_dataset()

st.title(":film_frames: Recensioni Film")

left_column, center_column, right_column = st.columns(3)

avg_rating = df['IMDB_Rating'].mean()
avg_metacritic = df['Meta_score'].mean()
avg_gross = "{:e}".format(df['Gross'].mean())

left_column.subheader('Average IMDb rating: ' + str(round(avg_rating,2)) + '/10')
center_column.subheader('Average Metacritic score: ' + str(round(avg_metacritic,2)) + '/100')
right_column.subheader('Average grossing: ' + str(avg_gross))

st.sidebar.title(body = "Filtri")

film_name = st.sidebar.text_input(
    label = 'Nome Film'
)

actor_name = st.sidebar.text_input(
    label = 'Nome Attore'
)

genre_name = st.sidebar.text_input(
    label = 'Nome Genere'
)

start_year = st.sidebar.select_slider(
    label = 'Anno di inizio',
    options = (df['Released_Year'].sort_values())
)

minimum_imdb_rating = st.sidebar.select_slider(
    label = 'IMDb rating minimo',
    options = (df['IMDB_Rating'].sort_values())
)

minimum_metacritic_score = st.sidebar.select_slider(
    label = 'Punteggio Metacritic minimo',
    options = (df['Meta_score'].sort_values())
)

minimum_grossing = st.sidebar.select_slider(
    label = 'Gross minimo',
    options = (df['Gross'].sort_values())
)

df_filtered = df[(df['Series_Title'].str.contains(film_name, na = False, case = False)) & 
                (df['Star1'].str.contains(actor_name, na = False, case = False) | 
                df['Star2'].str.contains(actor_name, na = False, case = False) | 
                df['Star3'].str.contains(actor_name, na = False, case = False) | 
                df['Star4'].str.contains(actor_name, na = False, case = False)) & 
                (df['Genre'].str.contains(genre_name, na = False, case = False)) &
                (df['Released_Year'] >= start_year) &
                (df['IMDB_Rating'] >= minimum_imdb_rating) &
                (df['Meta_score'] >= minimum_metacritic_score) &
                (df['Gross'] >= minimum_grossing)]

st.dataframe(df_filtered)

left_chart, right_chart = st.columns(2)

df_filtered['Genre'] = df_filtered['Genre'].str.split(', ')

genre_chart = px.pie(
    df_filtered.explode('Genre'),
    names= 'Genre',
    title='Percentuale film per genere',
    width = 400,
    height = 400
)

rating_chart = px.pie(
    df_filtered,
    names= 'IMDB_Rating',
    title='Percentuale film per IMDb Rating',
    width = 380,
    height = 380
)

left_chart.plotly_chart(genre_chart)
right_chart.plotly_chart(rating_chart)