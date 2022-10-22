import datetime
import pandas as pd
import plotly_express as px
import streamlit as st
from urllib import request

st.set_page_config(
    page_title = "Covid19 in Italia",
    page_icon = "syringe",
    layout = "wide"
)

localfile = "covid19.csv"
@st.cache()
def load_dataset():
    request.urlretrieve("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv", filename = localfile)
    return localfile

def get_dataset():
    file = load_dataset()
    df = pd.read_csv(file)
    df['data'] = pd.to_datetime(df['data'])
    df['data'] = df['data'].dt.date
    return df

df = get_dataset()
df.dropna(axis = 1)

latest_date = max(df['data'])
st.title(":syringe: Covid19 in Italia")
st.text("Dati aggiornati al " + str(latest_date))

st.sidebar.title(body = "Filtri")
states = st.sidebar.multiselect(
    label = "Seleziona regione",
    options = df['denominazione_regione'].unique(),
    default = df['denominazione_regione'].unique()
)

start_date = st.sidebar.date_input(
    label = "Seleziona data d'inizio",
    value = datetime.date(2022,1,1),
    min_value = min(df['data']),
    max_value = max(df['data'])
)

end_date = st.sidebar.date_input(
    label = "Seleziona data di fine",
    value = max(df['data']),
    min_value = min(df['data']),
    max_value = max(df['data'])
)

df_filtered = df[df['denominazione_regione'].isin(states) & (df['data'] <= end_date) & (df['data'] >= start_date)]

st.dataframe(df_filtered)

left_column, right_column = st.columns(2)

positive_plot = px.line(
    data_frame = df_filtered,
    x = "data",
    y = "totale_positivi",
    color = 'denominazione_regione',
    title = 'Totale positivi per Regione',
    width = 400,
    height = 400
)

healed_plot = px.line(
    data_frame = df_filtered,
    x = "data",
    y = "dimessi_guariti",
    color = 'denominazione_regione',
    title = 'Totale dimessi/guariti per Regione',
    width = 400,
    height = 400
)

left_column.plotly_chart(positive_plot)
right_column.plotly_chart(healed_plot)

lat_roma = 41.9027835
long_roma = 12.4963655

positive_bubble = px.scatter_geo(
    df_filtered,
    lat = df_filtered['lat'],
    lon = df_filtered['long'],
    title = "Mappa dei contagi per Regione",
    scope = "europe",
    center = dict(lon = long_roma, lat = lat_roma),
    size = "totale_positivi",
    color = "denominazione_regione",
    animation_frame = "data",
    hover_name = "denominazione_regione",
    width = 800,
    height = 800,
    size_max = 50,
    fitbounds = 'locations'
)

st.plotly_chart(positive_bubble)