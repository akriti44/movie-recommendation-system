import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_details(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
    data = response.json() #response converted to json and stored in data
    details = {
        "release_date": data['release_date'],
        "summary": data['overview'],
        "TMDB rating": data['vote_average'],
    }
    if data['poster_path']:
        details["poster_path"] = "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    else:
        details["poster_path"] = None


    return details


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]

    recommended_movies = []
    for i in movies_list:
        movie_id =  movies.iloc[i[0]].movie_id
        details = fetch_details(movie_id)
        details['title'] = movies.iloc[i[0]].title
        recommended_movies.append(details)
    return recommended_movies

movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict) #dataframe

similarity = pickle.load(open('similarity.pkl','rb'))

st.markdown("<h1 style='text-align:center; background-color: darkred; padding: 10px;'><img src='https://icon-library.com/images/movie-icon/movie-icon-7.jpg' width='50' height='50' width='50' height='50' width='50' height='50'> CineVerse <img src='https://icon-library.com/images/movie-icon/movie-icon-7.jpg' width='50' height='50'></h1>", unsafe_allow_html=True)

selected_movie_name = st.selectbox( #option box
'Select a movie:',
movies['title'].values)

if st.button('Recommend'):
    recommended_movies = recommend(selected_movie_name)

if 'recommended_movies' in locals():
    for movie in recommended_movies:
        st.header(movie['title'])
        st.image(movie['poster_path'], width=200)
        st.write("**Release date:** ", movie['release_date'], format='markdown')
        if movie['summary'] is not None:
            st.write("**Summary:** ", movie['summary'], format='markdown')
        st.write("**TMDB Rating:** ", movie['TMDB rating'], format='markdown')

