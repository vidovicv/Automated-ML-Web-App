from operator import index
import streamlit as st
import plotly.express as px
from pycaret.regression import setup, compare_models, pull, save_model, load_model
import pandas_profiling
import pandas as pd
from streamlit_pandas_profiling import st_profile_report
import os

#this makes the imported datafile accesible accross the app
if os.path.exists('./dataset.csv'):
    df = pd.read_csv('dataset.csv', index_col=None)

with st.sidebar:
    st.image("https://i.pinimg.com/originals/02/6d/30/026d305da36a37cfc64db20a3c310ecc.gif")
    st.title("Menu")
    choice = st.radio("Navigation", ["Upload","Profiling","Modelling", "Download"])
    st.info("This app will help you explore your dataset.")

if choice == "Upload":
    st.title("Upload Your Dataset")
    file = st.file_uploader("Upload Your Dataset")
    if file:
        df = pd.read_csv(file, index_col=None)
        df.to_csv('dataset.csv', index=None) #saves the file to the app
        st.dataframe(df)
# here the automated analysis of data takes place
if choice == "Profiling":
    st.title("Exploratory Data Analysis")
    profile_df = df.profile_report()
    st_profile_report(profile_df)

if choice == "Modelling":
    chosen_target = st.selectbox('Choose the Target Column', df.columns)
    if st.button('Run Modelling', on_click=None):
        setup(df, target=chosen_target)
        setup_df = pull()
        st.dataframe(setup_df)
        best_model = compare_models()
        compare_df = pull()
        st.dataframe(compare_df)
        save_model(best_model, 'best_model')

if choice == "Download":
    with open('best_model.pkl', 'rb') as f:
        st.download_button('Download Model', f, file_name="best_model.pkl")
