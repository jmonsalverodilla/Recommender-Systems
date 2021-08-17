import streamlit as st
import ast
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

##############################FUNCTIONS#####################################
#MOVIES
def main_movies(df_metadata_complete):
    #Figure
    df = df_metadata_complete.sort_values(by="revenue", ascending=False).head(10)
    trace1 = go.Bar(x=df["title"],y=df["revenue"])

    #Figure
    df = df_metadata_complete.sort_values(by="vote_count",ascending=False).head(10)
    trace2 = go.Bar(x=df["title"],y=df["vote_count"])

    #Figure
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Movies with highest revenues",
                                                       "Movies with highest vote_count"))

    fig.append_trace(trace1, 1, 1)
    fig.append_trace(trace2, 1, 2)

    fig.update_layout(barmode="stack").update_layout(title='<b>Movies</b>',autosize=False,width=900,height=400,showlegend=False)
    return fig

#CORRELATION BETWEEN BUDGET AND REVENUE
def correlation(df_metadata_complete):
    fig = px.scatter(df_metadata_complete, x="budget", y="revenue", trendline="ols",title="Correlation budget vs revenue")
    fig.update_layout(title="<b>Correlation budget vs revenue</b>",autosize=False,width=900,height=400)
    results = px.get_trendline_results(fig).px_fit_results.iloc[0].summary()
    return fig,results

#PRODUCTION COMPANIES
def production_companies(df_metadata_complete):
    df_metadata_complete['production_company_name'] = df_metadata_complete['production_companies'].fillna('[]').apply(ast.literal_eval).apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else []).str[0].fillna('NA')

    #Top 10 production companies
    movies_per_company = df_metadata_complete[df_metadata_complete['production_company_name']!='NA'].groupby("production_company_name").agg({'title':'count'}).reset_index().rename(columns={'title':'number_of_movies'}).sort_values(by="number_of_movies",ascending=False).head(10)
    revenue_per_company = df_metadata_complete[df_metadata_complete['production_company_name']!='NA'].groupby("production_company_name").agg({'revenue':'sum'}).reset_index().rename(columns={'revenue':'total_revenue'}).sort_values(by="total_revenue",ascending=False).head(10)

    #Figure
    fig = make_subplots(rows=1, cols=2,subplot_titles=("Number of movies (top 10 production companies)",
                                                      "Total revenue (top 10 production companies)"))

    trace1 = go.Bar(x=movies_per_company["production_company_name"],y=movies_per_company["number_of_movies"])
    trace2 = go.Bar(x=revenue_per_company["production_company_name"],y=revenue_per_company["total_revenue"])

    fig.append_trace(trace1, 1, 1)
    fig.append_trace(trace2, 1, 2)

    fig.update_layout(barmode="stack").update_layout(title = "<b>Production companies</b>",autosize=False,width=900,height=400,showlegend=False)
    return fig

#SPOKEN LANGUAGES
#Let's get the language
def spoken_languages(df_metadata_complete):
    df_metadata_complete['language'] = df_metadata_complete['spoken_languages'].fillna('[]').apply(ast.literal_eval).apply(lambda x: [i['iso_639_1'] for i in x] if isinstance(x, list) else []).str[0].fillna('NA')

    #Top 10 languages
    languages = df_metadata_complete[df_metadata_complete['language']!='NA'].groupby("language").agg({'title':'count'}).reset_index().rename(columns={'title':'number_of_movies'}).sort_values(by="number_of_movies",ascending=False)
    top_10_languages = languages[languages['language']!='en'].head(10)

    #Figure
    fig = go.Figure(data=[go.Pie(labels=top_10_languages['language'].tolist(),
                                 values=top_10_languages['number_of_movies'].tolist(),
                                 hole=.3)])
    fig.update_layout(title="<b>Distribution of spoken languages (English not included)</b>",autosize=False,width=900,height=400)
    return fig


#DIRECTORS WITH HIGHEST REVENUES
def directors_revenue(df_metadata_complete):
    directors_revenue = df_metadata_complete.groupby('director')['revenue'].sum().reset_index().rename(columns={'revenue':'total_revenue'}).sort_values(by="total_revenue",ascending=False).head(10)

    #Directors with highest number of movies
    directors_movies = df_metadata_complete.groupby('director')['title'].count().reset_index().rename(columns={'title':'number_of_movies'}).sort_values(by="number_of_movies",ascending=False).head(10)

    #Figure
    fig = make_subplots(rows=1, cols=2,subplot_titles=("Top 10 directors with highest total revenues",
                                                      "Top 10 directors with highest number of movies"))

    trace1 = go.Bar(x=directors_revenue["director"],y=directors_revenue["total_revenue"])
    trace2 = go.Bar(x=directors_movies["director"],y=directors_movies["number_of_movies"])

    fig.append_trace(trace1, 1, 1)
    fig.append_trace(trace2, 1, 2)

    fig.update_layout(title="<b>Directors</b>",autosize=False,width=900,height=400,showlegend=False)
    return fig

# SETTING PAGE CONFIG TO WIDE MODE
#st.set_page_config(layout="wide")
#lottie_book = load_lottieurl('https://assets4.lottiefiles.com/temp/lf20_aKAfIn.json')

def load_page(df_metadata_complete):

    ###Streamlit app
    _, row1, _ = st.beta_columns((0.01, 20, 0.01))

    with row1:
        st.markdown("<h1 style='text-align: center; color: black;'> 📊 Exploratory Data Analysis</h1>", unsafe_allow_html=True)
        st.write('')

        with st.beta_expander('View movies (sorted by revenue)'):
            st.write(df_metadata_complete.drop(columns=['soup']))

        fig = main_movies(df_metadata_complete)
        st.plotly_chart(fig)

        fig,results = correlation(df_metadata_complete)
        st.plotly_chart(fig)

        with st.beta_expander('View correlation results'):
            st.write(results)

        for i in range(3):
            st.write(" ")

        fig = production_companies(df_metadata_complete)
        st.plotly_chart(fig)

        fig = spoken_languages(df_metadata_complete)
        st.plotly_chart(fig)

        fig = directors_revenue(df_metadata_complete)
        st.plotly_chart(fig)


