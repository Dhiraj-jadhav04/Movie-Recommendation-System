import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=d0be9459fd257aa932c01080bc7cdb7f&language=en-US'
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path
    except Exception:
        pass
    # fallback placeholder if poster missing or request fails
    return "https://via.placeholder.com/500x750?text=No+Poster"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


# Load data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Title
st.title('Movie Recommender System')

# Movie selection
selected_movie_name = st.selectbox('Select a movie', movies['title'].values)

# Recommendations
if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    # Use modern API
    if hasattr(st, "columns"):
        cols = st.columns(5)
    elif hasattr(st, "beta_columns"):  # for very old versions
        cols = st.beta_columns(5)
    else:
        cols = [st, st, st, st, st]

    for i, col in enumerate(cols):
        with col:
            if i < len(names):
                st.text(names[i])
                # ✅ FIX: replaced use_column_width with use_container_width
                st.image(posters[i], use_container_width=True)
