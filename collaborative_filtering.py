import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import requests
import plotly.express as px
from streamlit_lottie import st_lottie
import time


################################Functions##########
@st.cache(show_spinner=False)
def get_similarity_matrix(df_ratings_complete):
    # Dataframe where every row is an user, the columns are all the possible movies and the values are the ratings (NaN if the user has not watched the movie)
    pivot_ratings = df_ratings_complete.pivot(index='userId', columns='title', values='rating').fillna(0)

    # Cosine similarity matrix
    similarity = cosine_similarity(pivot_ratings.T)  ##The distance is a positive measure, and we are calculating the similarity as 1-distance
    df_similarity = pd.DataFrame(similarity, index=pivot_ratings.columns, columns=pivot_ratings.columns).reset_index()
    return df_similarity

@st.cache(show_spinner=False)
def get_most_similar_items(*,items,max_number_of_predictions,df_similarity):
    df_transactions_cosine = df_similarity[df_similarity['title'].isin(items)].drop(columns=items)
    df_most_similar_items = df_transactions_cosine.drop(columns=['title']).sum(axis = 0).reset_index().rename(columns={0:'similarity'}).sort_values(by="similarity",ascending=False).head(max_number_of_predictions)
    return df_most_similar_items

@st.cache(show_spinner=False)
def plot_similarities(df_most_similar_items):
    fig = px.histogram(df_most_similar_items,
                       x="title",
                       y="similarity",
                       color='title',
                       title="Recommended movies",
                       color_discrete_sequence=px.colors.qualitative.Dark24,
                       height=500)
    fig.update_yaxes(title="Similarity")
    return fig

@st.cache(show_spinner=False)
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


###################################APP######################################

# SETTING PAGE CONFIG TO WIDE MODE
#st.set_page_config(layout="wide")
#lottie_book = load_lottieurl('https://assets4.lottiefiles.com/temp/lf20_aKAfIn.json')

def load_page(df_ratings_complete):

    df_similarity = get_similarity_matrix(df_ratings_complete)

    ###Streamlit app
    row1_spacer1, row1_1, row1_spacer2 = st.beta_columns((0.01, 3.2, 0.01))

    with row1_1:
        st.markdown("<h1 style='text-align: center; color: black;'> 🎬 Collaborative Filtering Movie Recommender</h1>", unsafe_allow_html=True)

        st.image('./images/item_based_collaborative_filtering.jpg', use_column_width=True)
        #st_lottie(lottie_book, speed=1, height=200, key="initial")

        #if st.checkbox('view data'):
        #    st.subheader('Raw data')
        #    st.write(df_ratings_complete)
        #    st.write("\n")

        # User search
        st.markdown("## Select your favourite movie/movies in order to get recommendations")
        selected_titles = st.multiselect(label="Selected movie/movies",
                                        options=df_ratings_complete['title'].unique(),
                                        default = ["The Dark Knight Rises"])


        # Number of recommendations
        number_of_recommendations = st.number_input("Number of recommended movies", value=10, step=1)

        #################################ITEM-TO-ITEM COLLABORATIVE FILTERING USING COSINE SIMILARITIES##########################
        if st.button("Get recommendations"):
            if len(selected_titles) != 0:
                df_most_similar_items = get_most_similar_items(items=selected_titles,
                                                               max_number_of_predictions=number_of_recommendations,
                                                               df_similarity=df_similarity)
                fig = plot_similarities(df_most_similar_items=df_most_similar_items)
                st.plotly_chart(fig)
            else:
                st.write("You need to select at least a movie you liked in order to get recommendations")
        print(type(st.session_state))
        for var in st.session_state:
            print(var)
