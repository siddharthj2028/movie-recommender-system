import pandas as pd
import streamlit as st
import pickle
import requests
import gzip


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return full_path
def fetch_movie_link(movie_id):
    return f"https://www.themoviedb.org/movie/{movie_id}"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

    recommended_movies = []
    recommended_movies_posters = []
    recommended_movies_links = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
        recommended_movies_links.append(fetch_movie_link(movie_id))
    return recommended_movies, recommended_movies_posters, recommended_movies_links

with open('similarity.pkl', 'rb') as f_in, gzip.open('similarity.pkl.gz', 'wb') as f_out:
    f_out.write(f_in.read())
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

# selectbox
selected_movie_name = st.selectbox(
    "Select a movie to get recommendations:",
    movies['title'].values)

# button
if st.button("Recommend"):
    recommended_movies, recommended_movies_posters, recommended_movies_links = recommend(selected_movie_name)

    # Display 5 movies in a row, up to 10 movies
    for i in range(0, 10, 5):
        cols = st.columns(5)
        for j in range(5):
            if i + j < len(recommended_movies):
                with cols[j]:
                    st.markdown(
                        f"<h4 style='text-align: center; font-size: 14px;'>{recommended_movies[i + j]}</h4>",
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        f"<a href='{recommended_movies_links[i + j]}' target='_blank'>"
                        f"<img src='{recommended_movies_posters[i + j]}' style='display: block; margin-left: auto; margin-right: auto; width: 100%;' />"
                        f"</a>",
                        unsafe_allow_html=True
                    )
