import os #To provide fuctions to interact with operating system
import pickle
import streamlit as st
import requests #To send HTTP requests and interact with web APIs easily
import tempfile #To create temporary files and directories that are automatically cleaned up, useful for storing data during runtime

# For downloading from Google Drive
try:
    import gdown
except ImportError:
    os.system('pip install gdown')
    import gdown

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=282f9c8c31adb71767c4c6ff39e14a23&language=en-US"
    data = requests.get(url).json() #Data from url to json format
    poster_path = data.get('poster_path') #json from url have poster_path key which has poster link as its value is what we get
    return "https://image.tmdb.org/t/p/w500/" + poster_path if poster_path else "" #To concatenate base link and posterpath

def recommend(movie):
    index = movies[movies['title'] == movie].index[0] #Index of selected movie
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1]) #distances with indexes and sort by similarity value by using key
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id #access the value of movie_id column value 
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movie_names, recommended_movie_posters

# === Download files from Google Drive if not found ===

# Set paths
SIMILARITY_PATH = os.path.join(tempfile.gettempdir(), "similarity.pkl")
MOVIE_LIST_PATH = os.path.join(tempfile.gettempdir(), "movie_list.pkl")

# Your Google Drive file IDs
SIMILARITY_FILE_ID = "1-mORb4tPPAw9ssDrhnMSKDG_P7jF8xmM"
MOVIE_LIST_FILE_ID = "1V4XOkRJ5v6n_5WYD6Wk1PSRdW3wVbeN4"  # <- Replace this with actual ID

# Download similarity.pkl
if not os.path.exists(SIMILARITY_PATH):
    st.warning("Downloading similarity file. Please wait...")
    gdown.download(f"https://drive.google.com/uc?id={SIMILARITY_FILE_ID}", SIMILARITY_PATH, quiet=False)

# Download movie_list.pkl
if not os.path.exists(MOVIE_LIST_PATH):
    st.warning("Downloading movie list file. Please wait...")
    gdown.download(f"https://drive.google.com/uc?id={MOVIE_LIST_FILE_ID}", MOVIE_LIST_PATH, quiet=False)

# === Load data ===
movies = pickle.load(open(MOVIE_LIST_PATH, 'rb'))
similarity = pickle.load(open(SIMILARITY_PATH, 'rb'))

# === Streamlit UI ===
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
