#Libraries
import pandas as pd
import numpy as np
import ast

#Nltk
from nltk.stem.wordnet import WordNetLemmatizer

#################################COLLABORATIVE FILTERING FUNCTION########################################################################################################
def get_df_ratings_complete(df_ratings, df_links, df_metadata):
    # Merge three dataframes
    df_ratings_complete = df_ratings. \
        merge(df_links, how="inner"). \
        merge(df_metadata[['imdb_id', 'title']].drop_duplicates('title'), how="inner", left_on="imdbId", right_on="imdb_id")

    df_ratings_complete = df_ratings_complete[['userId', 'title', 'rating']]
    df_ratings_complete['userId'] = df_ratings_complete['userId'].astype(str)
    df_ratings_complete['rating'] = df_ratings_complete['rating'].astype(float)
    return df_ratings_complete
################################################################################################################################################################################


#############################CONTENT BASED FUNCTION###################################################################################################################################
def get_soup_column(df_metadata,df_credits,df_keywords):
    df_metadata1 = df_metadata.merge(df_credits, on='id',how="inner").drop_duplicates()
    df_metadata_complete = df_metadata1.merge(df_keywords, on='id',how="inner").drop_duplicates()

    #Literal eval
    df_metadata_complete['crew'] = df_metadata_complete['crew'].apply(ast.literal_eval)
    df_metadata_complete['cast'] = df_metadata_complete['cast'].apply(ast.literal_eval)
    df_metadata_complete['keywords'] = df_metadata_complete['keywords'].apply(ast.literal_eval)

    #######################GENRES###########################
    #Let's get the genres of each movie
    df_metadata_complete['genre_formatted'] = df_metadata_complete['genres'].fillna('[]').apply(ast.literal_eval).apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])

    ######################DIRECTOR#########################
    #Let's get the directors of each movie
    def get_director(x):
        for i in x:
            if i['job'] == 'Director':
                return i['name']
        return np.nan

    df_metadata_complete['director'] = df_metadata_complete['crew'].apply(get_director) #get diretor from crew column
    df_metadata_complete['director'] = df_metadata_complete['director'].astype('str').apply(lambda x: str.lower(x.replace(" ", ""))) #lower case and remove white spaces
    df_metadata_complete['director'] = df_metadata_complete['director'].apply(lambda x: [x,x]) #mention director twice times to weigh it more

    #####################CAST##############################
    df_metadata_complete['cast_formatted'] = df_metadata_complete['cast'].apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])
    df_metadata_complete['cast_formatted'] = df_metadata_complete['cast_formatted'].apply(lambda x: [str.lower(i.replace(" ", "")) for i in x])
    df_metadata_complete['cast_formatted'] = df_metadata_complete['cast_formatted'].apply(lambda x: x[:3] if len(x) >=3 else x) #keep first 3 actors from the list

    ####################KEYWORDS############################
    #stemmer = SnowballStemmer('english')
    lemmatizer = WordNetLemmatizer()
    df_metadata_complete['keywords_formatted'] = df_metadata_complete['keywords'].apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])
    #df_metadata2['keywords_formatted'] = df_metadata2['keywords_formatted'].apply(lambda x: [stemmer.stem(i) for i in x]) #stem of the word
    df_metadata_complete['keywords_formatted'] = df_metadata_complete['keywords_formatted'].apply(lambda x: [lemmatizer.lemmatize(i) for i in x]) #lemma of the word
    df_metadata_complete['keywords_formatted'] = df_metadata_complete['keywords_formatted'].apply(lambda x: [str.lower(i.replace(" ", "")) for i in x]) #lowercase and without white spaces

    ##################COMBINE PREVIOUS COLUMNS: GENRE, DIRECTOR, CAST, KEYWORDS#############
    df_metadata_complete['soup'] = df_metadata_complete['genre_formatted'] + df_metadata_complete['director'] + df_metadata_complete['cast_formatted'] + df_metadata_complete['keywords_formatted']
    df_metadata_complete['soup'] = df_metadata_complete['soup'].apply(lambda x: ' '.join(x))
    return df_metadata_complete
###################################################################################################################################################################################################

#############Paths############
#Input
path_metadata = './dat/movies_metadata.csv'
path_credits = './dat/credits.csv'
path_keywords = './dat/keywords.csv'
path_links = './dat/links_small.csv'
path_ratings_small = './dat/ratings_small.csv'

#Output
path_metadata_complete = './dat/movies_metadata_complete.csv'
path_ratings_complete = './dat/ratings_complete.csv'

#################  1) METADATA DATASET     ##########################
df_metadata = pd.read_csv(path_metadata)
df_metadata['id'] = df_metadata['id'].astype('str')
df_metadata['title'] = df_metadata['title'].str.title()
df_metadata['revenue'] = df_metadata['revenue'].astype('float')
df_metadata['imdb_id'] = df_metadata['imdb_id'].str.replace('tt', '')
df_metadata = df_metadata[df_metadata['revenue'] > 10_000_000].drop_duplicates('title')


#################### 2)  CREDITS DATASET   ###############################
df_credits = pd.read_csv(path_credits)
df_credits['id'] = df_credits['id'].astype('str')

##################### 3)  KEYWORDS DATASET ###############################
df_keywords = pd.read_csv(path_keywords)
df_keywords['id'] = df_keywords['id'].astype('str')

################   4) LINKS DATASET         #####################
df_links = pd.read_csv(path_links,dtype=str)

################   5) RATINGS SMALL DATASET ####################
df_ratings = pd.read_csv(path_ratings_small,dtype=str)


#########################CONTENT BASED RECOMMENDER###############
df_metadata_complete = get_soup_column(df_metadata, df_credits, df_keywords)
columns_selected = ['budget','genres','original_language','popularity','production_companies','production_countries',
                    'release_date','revenue','runtime','vote_average','vote_count',
                   'title','soup']
df_metadata_complete[columns_selected].to_csv(path_metadata_complete, sep=",",index=False)

##########################COLLABORATIVE FILTERING##############
df_ratings_complete = get_df_ratings_complete(df_ratings, df_links, df_metadata)
df_ratings_complete.to_csv(path_ratings_complete, sep=",",index=False)