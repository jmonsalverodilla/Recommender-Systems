import streamlit as st
from streamlit_lottie import st_lottie
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import requests
import plotly.express as px

########Functions##########
def get_most_likely_items_cosine_similarity(*,items,max_number_of_predictions,df_similarity):
    df_transactions_cosine = df_similarity[df_similarity['title'].isin(items)].drop(columns=items)
    df_most_similar_items = df_transactions_cosine.drop(columns=['title']).sum(axis = 0).reset_index().rename(columns={0:'similarity'}).sort_values(by="similarity",ascending=False)
    fig = px.bar(df_most_similar_items.head(max_number_of_predictions), x="title",y="similarity",title="Recommended movies",
           labels={'producto': "Most likely product to buy"}, height=500)
    return fig

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# SETTING PAGE CONFIG TO WIDE MODE
#st.set_page_config(layout="wide")
#lottie_book = load_lottieurl('https://assets4.lottiefiles.com/temp/lf20_aKAfIn.json')

def load_page(df_metadata_complete):

    ###Streamlit app
    row1_spacer1, row1_1, row1_spacer2 = st.beta_columns((0.01, 3.2, 0.01))

    with row1_1:
        st.markdown("# 📊 Exploratory Data Analysis")