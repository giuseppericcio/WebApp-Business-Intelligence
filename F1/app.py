import pandas as pd
import plotly_express as px
import streamlit as st

pd.options.mode.chained_assignment = None

st.set_page_config(
    page_title = "F1",
    page_icon = ":racing_car:",
    layout = "wide"
)

st.title(':racing_car: F1')

st.image("https://storage.googleapis.com/kaggle-datasets-images/468218/878459/e2b865299a720df627331f8d213eb8f9/dataset-cover.jpg?t=2020-01-07-17-56-51")

def get_constructor():
    circuits = pd.read_csv('./Dataset/circuits.csv')
    circuits.dropna(axis = 1)
    circuits.drop(labels = ['lat','lng','url'], axis = 1, inplace = True)

    status = pd.read_csv('./Dataset/status.csv')

    races = pd.read_csv('./Dataset/races.csv')
    races.dropna(axis = 1)
    races.drop(labels = ['url','fp1_date','fp1_time','fp2_date','fp2_time',
                            'fp3_date','fp3_time','quali_date','quali_time',
                            'sprint_date','sprint_time'], axis = 1, inplace = True)

    constructor_standings = pd.read_csv('./Dataset/constructor_standings.csv')
    constructor_standings.drop(labels = 'positionText', axis = 1, inplace = True)

    constructors = pd.read_csv('./Dataset/constructors.csv')
    constructors.drop(labels = ['constructorRef','url'], axis = 1, inplace = True)

    results = pd.read_csv('./Dataset/results.csv')
    results.dropna(axis = 1)
    results.drop(labels = ['positionText','time','milliseconds','fastestLap',
                            'fastestLapTime','rank','fastestLapSpeed'], 
                            axis = 1, inplace = True)
    
    constructors_df = constructors.merge(results,on='constructorId',how = 'left')
    constructors_df = constructors_df.merge(races,on='raceId',how = 'left')
    constructors_df = constructors_df.merge(status,on='statusId',how = 'left')

    constructors_df.drop(labels = ['constructorId','raceId','statusId',
                                    'resultId','circuitId'], 
                                    axis = 1, inplace = True)

    return constructors_df


def get_drivers():
    circuits = pd.read_csv('./Dataset/circuits.csv')
    circuits.dropna(axis = 1)
    circuits.drop(labels = ['lat','lng','url'], axis = 1, inplace = True)

    status = pd.read_csv('./Dataset/status.csv')

    races = pd.read_csv('./Dataset/races.csv')
    races.dropna(axis = 1)
    races.drop(labels = ['url','fp1_date','fp1_time','fp2_date','fp2_time',
                            'fp3_date','fp3_time','quali_date','quali_time',
                            'sprint_date','sprint_time'], axis = 1, inplace = True)

    driver_standings = pd.read_csv('./Dataset/driver_standings.csv')
    driver_standings.drop(labels = 'positionText', axis = 1, inplace = True)

    drivers = pd.read_csv('./Dataset/drivers.csv')
    drivers.drop(labels = 'url', axis = 1, inplace = True)

    results = pd.read_csv('./Dataset/results.csv')
    results.dropna(axis = 1)
    results.drop(labels = ['positionText','time','milliseconds','fastestLap',
                            'fastestLapTime','rank','fastestLapSpeed'], 
                            axis = 1, inplace = True)
    
    drivers_df = drivers.merge(results,on='driverId',how = 'left')
    drivers_df = drivers_df.merge(races,on='raceId',how = 'left')
    drivers_df = drivers_df.merge(status,on='statusId',how = 'left')

    drivers_df.drop(labels = ['driverId','raceId','statusId',
                                    'resultId','circuitId'], 
                                    axis = 1, inplace = True)
    
    return drivers_df

st.subheader('Classifica Costruttori')

constructor = get_constructor()
st.dataframe(constructor)

st.subheader('Classifica Piloti')

driver = get_drivers()
st.dataframe(driver)