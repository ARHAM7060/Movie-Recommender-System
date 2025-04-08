import os
import pickle
import streamlit as st
import requests

# For downloading from Google Drive
try:
    import gdown
except ImportError:
    os.system('pip install gdown')
    import gdown

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=282f9c8c31adb71767c4c6ff39e14a23&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    return "https://image.tmdb.org/t/p/w500/" + poster_path if poster_path else ""

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movie_names, recommended_movie_posters

# Step: Download similarity.pkl from Google Drive if not found
SIMILARITY_PATH = "similarity.pkl"
GDRIVE_FILE_ID = "1-mORb4tPPAw9ssDrhnMSKDG_P7jF8xmM"  # Replace with your actual file ID

if not os.path.exists(SIMILARITY_PATH):
    st.warning("Downloading similarity file. Please wait...")
    gdown.download(f"https://drive.google.com/uc?id={GDRIVE_FILE_ID}", SIMILARITY_PATH, quiet=False)

# Load the pickle files
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit UI
st.header('Movie Recommender System')
movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(recommended_movie_names[i])
            st.image(recommended_movie_posters[i])
