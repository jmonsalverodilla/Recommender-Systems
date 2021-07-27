#################Libraries##############
#Data analysis libraries
import pandas as pd
pd.options.display.max_colwidth = 1000
pd.set_option("display.max_columns",100)
pd.set_option("display.max_rows",100)

#Visualization libraries
import plotly.express as px

#Dashboarding
import streamlit as st

##########################Functions###############################
@st.cache(show_spinner=False)
def get_most_likely_items_similarity_dict(*,items,max_number_of_predictions,dict_similarity):
    d = {}
    for movie in items:
        dict_movie = dict_similarity[movie]
        values = list(dict_movie.values())
        columns = list(dict_movie.keys())
        df_movie = pd.DataFrame(data = [values], columns=columns)
        d[movie] = df_movie
    df_similarity_filtered = pd.concat(d.values(), ignore_index=True).fillna(0)
    df_most_similar_items = df_similarity_filtered.sum(axis = 0).reset_index().rename(columns={'index':'title', 0:'similarity'}).sort_values(by="similarity",ascending=False)
    fig = px.bar(df_most_similar_items.head(max_number_of_predictions), x="title",y="similarity",title="Recommended movies",
           labels={'similarity': "Similarity"}, height=500)
    return fig
###################################APP######################################

# SETTING PAGE CONFIG TO WIDE MODE
#st.set_page_config(layout="wide")

def load_page(dict_similarity_collaborative_filtering):

    ###Streamlit app
    row1_spacer1, row1_1, row1_spacer2 = st.beta_columns((0.01, 3.2, 0.01))

    with row1_1:
        st.markdown("<h1 style='text-align: center; color: black;'> 🎬 Collaborative Filtering Movie Recommender</h1>", unsafe_allow_html=True)
        st.image('./images/item_based_collaborative_filtering.jpg', use_column_width=True)

        #if st.checkbox('view data'):
        #    st.subheader('Raw data')
        #    st.write(df_ratings_complete)
        #    st.write("\n")

        # User search
        st.markdown("## Select your favourite movie/movies in order to get recommendations")
        selected_titles = st.multiselect(label="Selected movie/movies",
                                        options=list(dict_similarity_collaborative_filtering.keys()),
                                        default = ["The Dark Knight Rises"])


        # Number of recommendations
        number_of_recommendations = st.number_input("Number of recommended movies", value=10, step=1)

        #################################ITEM-TO-ITEM COLLABORATIVE FILTERING USING COSINE SIMILARITIES##########################
        if st.button("Get recommendations"):
            if len(selected_titles) != 0:
                fig = get_most_likely_items_similarity_dict(items=selected_titles,
                                                            max_number_of_predictions=number_of_recommendations,
                                                            dict_similarity=dict_similarity_collaborative_filtering)
                st.plotly_chart(fig)
            else:
                st.write("You need to select at least a movie you liked in order to get recommendations")

        #print(type(st.session_state))
        #for var in st.session_state:
        #    print(var)
