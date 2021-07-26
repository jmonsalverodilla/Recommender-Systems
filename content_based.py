#################Libraries##############
#Data analysis libraries
import pandas as pd
pd.options.display.max_colwidth = 1000
pd.set_option("display.max_columns",100)
pd.set_option("display.max_rows",100)

#Visualization libraries
import plotly.express as px

#Sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#Dashboarding
import streamlit as st

##########################Functions###############################
#Let's create the vectorizer and the tfidf matrix
@st.cache(show_spinner=False,allow_output_mutation=True)
def tfidf(df_input, column_similarities):
    vectorizer = TfidfVectorizer(stop_words='english',max_features=None) #It gets the features that will make up the sparse matrix
    tfidf_matrix = vectorizer.fit_transform(df_input[column_similarities])
    return tfidf_matrix

#Let's create the cosine similarity matrix
@st.cache(show_spinner=False,allow_output_mutation=True)
def similarities(df_input, tfidf_matrix, column_identifier):
    cosine_sim = cosine_similarity(tfidf_matrix)
    df_cosine_sim = pd.DataFrame(cosine_sim, columns=df_input[column_identifier], index=df_input[column_identifier])
    return df_cosine_sim

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


###################################APP###################################################
def load_page(df_metadata_complete):

    ###########Let's call the functions
    tfidf_matrix_content_based= tfidf(df_input=df_metadata_complete, column_similarities='soup')
    df_similarity = similarities(df_input=df_metadata_complete, tfidf_matrix=tfidf_matrix_content_based, column_identifier='title').reset_index()

    ###Streamlit app
    row1_spacer1, row1_1, row1_spacer2 = st.beta_columns((0.01, 3.2, 0.01))

    with row1_1:
        st.markdown("<h1 style='text-align: center; color: black;'> 🎬 Content based movie recommender </h1>", unsafe_allow_html=True)

        st.image('./images/content_based_recommender_2.png', use_column_width=True)

        # User search
        st.markdown("## Select your favourite movie/movies in order to get recommendations")
        selected_titles = st.multiselect(label="Selected movie/movies",
                                        options=df_metadata_complete['title'].unique(),
                                        default=["The Dark Knight Rises"])

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

