import streamlit as st
import pickle
import pandas as pd
import requests
page_by_img = """
<style>
[data-testid="stAppViewContainer"]{
background-image:url("https://wallpapers.com/images/hd/american-movie-posters-z0puq43u0qbtr6j2.webp");
background-size: cover;
}
[data-testid="block-container"]{
background-color: rgba(0, 0, 0, 0.5);
padding-bottom: 5rem;
padding-top: 3rem;
}
</style>
"""
st.markdown(page_by_img, unsafe_allow_html=True)
def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=c19cfd9048526e66a0e4248fb6814186a'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse = True, key = lambda x:x[1])[1:6]
    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))
st.title('Movies Recommender System')
selected_movie_name = st.selectbox(
'Which movie you would like to get recommendations for?',
movies['title'].values)
if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.header(names[0])
        st.image(posters[0])

    with col2:
        st.header(names[1])
        st.image(posters[1])

    with col3:
        st.header(names[2]) 
        st.image(posters[2])
    with col4:
        st.header(names[3])
        st.image(posters[3])
    with col5:
        st.header(names[4])
        st.image(posters[4])