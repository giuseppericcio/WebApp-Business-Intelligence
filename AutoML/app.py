import streamlit as st
import pandas_profiling
import pandas as pd
from streamlit_pandas_profiling import st_profile_report
import os

# Se il dataset è già stato caricato faccio il retrieval di questo
if os.path.exists('./dataset.csv'):
    df = pd.read_csv('dataset.csv', index_col=None)

# Menu laterale per la selezione del tipo di problema e per le fasi di ML
with st.sidebar:
    st.image("https://www.onepointltd.com/wp-content/uploads/2020/03/inno2.png")
    st.title("Scopri il tuo modello ML")
    type = st.selectbox("Tipo di problema", options = ["Classificazione", "Regressione"])
    choice = st.radio("Fasi ML:", ["Carica Dataset","Analisi dei Dati","Modellazione", "Scarica Modello"])
    st.info("Questa applicazione di esempio ti aiuta a capire qual'è il miglior modello di Machine Learning per i tuoi dati.")

# Importo la libreria corrispondente al problema che voglio risolvere
if type == "Classificazione":
    from pycaret.classification import setup, compare_models, pull, save_model
else:
    from pycaret.regression import setup, compare_models, pull, save_model

# Carico il mio Dataset
if choice == "Carica Dataset":
    st.title("Carica il tuo Dataset")
    file = st.file_uploader("Carica il tuo Dataset")
    if file:
        df = pd.read_csv(file, index_col=None)
        df.to_csv('dataset.csv', index=None)
        st.dataframe(df)

# Analizzo i dati presenti nel Dataset
if choice == "Analisi dei Dati": 
    st.title("Analisi esplorativa dei dati")
    profile_df = df.profile_report()
    st_profile_report(profile_df)

# Faccio il train del Modello ed effettuo delle comparazioni per prendere il migliore
if choice == "Modellazione":
    chosen_target = st.selectbox('Scegli la colonna target', df.columns)
    if st.button('Esegui Modellazione'): 
        setup(df, target=chosen_target, silent=True)
        best_model = compare_models()
        compare_df = pull()
        st.dataframe(compare_df)
        save_model(best_model, 'best_model')

# Scarico il miglior Modello
if choice == "Scarica Modello":
    with open('best_model.pkl', 'rb') as f:
        st.download_button('Scarica Modello', f, file_name="best_model.pkl")
