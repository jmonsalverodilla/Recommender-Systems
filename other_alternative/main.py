#Import libraries
import streamlit as st
from PIL import Image
import pandas as pd
import json

#Import custom modules
import eda
import collaborative_filtering
import content_based

@st.cache(show_spinner=False)
def load_data():
    ############PATHS########################
    path_metadata_complete = './dat/movies_metadata_complete.csv'
    path_dict_similarity_content_based = './dat/dict_similarity_content_based.json'
    path_dict_similarity_collaborative_filtering = './dat/dict_similarity_collaborative_filtering.json'

    #Loading metadata for EDA
    df_metadata_complete = pd.read_csv(path_metadata_complete, dtype=str, sep=",")

    #Loading content based similarity dict
    with open(path_dict_similarity_content_based, 'r') as fp:
        dict_similarity_content_based = json.load(fp)

    #Loading collaborative filtering similarity dict
    with open(path_dict_similarity_collaborative_filtering, 'r') as fp:
        dict_similarity_collaborative_filtering = json.load(fp)


    return df_metadata_complete, dict_similarity_content_based, dict_similarity_collaborative_filtering

def create_layout(df_metadata_complete, dict_similarity_content_based, dict_similarity_collaborative_filtering) -> None:
    # Side bar portion of code
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
            width: 370px;}
        </style>
        """,
        unsafe_allow_html=True,
    )
    author_pic = Image.open('./images/javi.jpg')
    st.sidebar.image(author_pic, "Author", use_column_width=True)
    st.sidebar.write("This app is powered by Machine Learning!")
    st.sidebar.markdown("[Link to my Github Profile](https://github.com/jmonsalverodilla)")
    st.sidebar.title("Menu")
    app_mode = st.sidebar.selectbox("Please select a page", ["Homepage",
                                                             "EDA",
                                                             "Content based movie recommender",
                                                             "Collaborative filtering movie recommender"])
    if app_mode == 'Homepage':
        load_homepage()
    elif app_mode == "EDA":
        eda.load_page(df_metadata_complete)
    elif app_mode == "Content based movie recommender":
        content_based.load_page(dict_similarity_content_based)
    elif app_mode == "Collaborative filtering movie recommender":
        collaborative_filtering.load_page(dict_similarity_collaborative_filtering)

def load_homepage() -> None:
    st.markdown("# ???? Recommendation Systems")
    st.write("")
    st.write("This project shows the results of two of the most popular methods that recommendations engines use. "
             "The dataset used can be found on the following link [The movies Dataset](https://www.kaggle.com/rounakbanik/the-movies-dataset) ")
    st.markdown("<div align='center'><br>"
                "<img src='https://img.shields.io/badge/CODED%20WITH-PYTHON%20-red?style=for-the-badge'"
                "alt='API stability' height='25'/>"
                "<img src='https://img.shields.io/badge/DEPLOYED%20ON-Heroku-blue?style=for-the-badge'"
                "alt='API stability' height='25'/>"
                "<img src='https://img.shields.io/badge/DASHBOARD%20WITH-Streamlit-green?style=for-the-badge'"
                "alt='API stability' height='25'/></div>", unsafe_allow_html=True)
    for i in range(3):
        st.write(" ")

    st.image('https://www.vshsolutions.com/wp-content/uploads/2020/02/recommender-system-for-movie-recommendation.jpg', use_column_width=True)

    for i in range(3):
        st.write(" ")
    st.header("??????? The Application")
    st.write("This application is a Streamlit dashboard hosted on Heroku which explores the MovieLens Dataset and uses two different recommendation techniques, "
             "content based and collaborative filtering, in order to make recommendations.")
    st.write("There are currently four pages available in the application:")
    st.subheader("?????? Homepage ??????")
    st.markdown("* Presentation of the app and introduction to the project.")
    st.subheader("?????? EDA  ??????")
    st.markdown("* It allows to understand the data better and play a bit with it.")
    st.subheader("?????? Content based movie recommender ??????")
    st.markdown("* It uses metadata information about the movies (genre, director, cast and keywords) in order to make recommendations.")
    st.subheader("?????? Collaborative filtering movie recommender ??????")
    st.markdown("* It uses ratings given by the users in order to establish similarities between the movies and this allows to make recommendations.")


def main():
    df_metadata_complete, dict_similarity_content_based, dict_similarity_collaborative_filtering = load_data()
    create_layout(df_metadata_complete, dict_similarity_content_based, dict_similarity_collaborative_filtering)

if __name__ == "__main__":
    main()