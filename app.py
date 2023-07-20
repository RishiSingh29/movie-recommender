import streamlit as st
import pickle
import pandas as pd
import requests
import plotly.express as px
import base64

@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


img = get_img_as_base64("background.jpg")

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://www.notebookcheck.net/fileadmin/Notebooks/News/_nc3/netflixteaser.png");
background-size: 100%;
background-position: top left;
background-repeat: no-repeat;
background-attachment: local;
}}

[data-testid="stSidebar"] > div:first-child {{
background-image: url("data:image/png;base64,{img}");
background-position: center; 
background-repeat: no-repeat;
background-attachment: fixed;
}}

[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}

[data-testid="stToolbar"] {{
right: 2rem;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

def fetch_poster(id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=9d91b0f6423ae2f110bfb8ddb6a6f1c3&language=en-US".format(id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        id = movies.iloc[i[0]].id
        recommended_movie_posters.append(fetch_poster(id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters


title_style = 'color: white; font-size: 40px; text-shadow: -1px -1px 0 black, 1px -1px 0 black, -1px 1px 0 black, 1px 1px 0 black; padding: 10px;'

st.markdown(f'<h1 style="{title_style}">Movies Recommendation System</h1>', unsafe_allow_html=True)


selected_movie = st.selectbox(
    'Select a movie',
    movies['title'].values
)

if st.button('Recommend'):
   recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
   col1, col2, col3, col4, col5 = st.columns(5)
   with col1:
    st.text(recommended_movie_names[0])
    st.image(recommended_movie_posters[0])
   with col2:
    st.text(recommended_movie_names[1])
    st.image(recommended_movie_posters[1])

   with col3:
    st.text(recommended_movie_names[2])
    st.image(recommended_movie_posters[2])
   with col4:
    st.text(recommended_movie_names[3])
    st.image(recommended_movie_posters[3])
   with col5:
    st.text(recommended_movie_names[4])
    st.image(recommended_movie_posters[4])

