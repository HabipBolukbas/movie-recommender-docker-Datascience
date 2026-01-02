import os
from dotenv import load_dotenv
load_dotenv() # This loads the variables from .env
import streamlit as st
import pickle
import pandas as pd
import requests
import base64

# 1. Page Configuration (Sets the tab title and icon)
st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

# 2. Cinematic Background Styling
def set_bg_hack():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), 
                         url("https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?q=80&w=2070");
             background-size: cover;
             background-position: center;
             background-attachment: fixed;
         }}
         
         /* Styling the movie titles to be white and readable */
         h1, h2, h3, p, .stText {{
             color: white !important;
             font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
         }}

         /* Make the selection box and buttons look premium */
         .stSelectbox div[data-baseweb="select"] {{
             background-color: rgba(255, 255, 255, 0.1);
             color: white;
         }}
         
         .stButton>button {{
             background-color: #E50914; /* Netflix Red */
             color: white;
             border-radius: 5px;
             border: none;
             font-weight: bold;
             width: 100%;
             padding: 10px;
         }}

         .stButton>button:hover {{
             background-color: #ff0f1e;
             color: white;
             border: none;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

set_bg_hack()

# 3. Function to fetch the poster from TMDB
def fetch_poster(movie_id):
    # Instead of the hardcoded string, use os.getenv
    api_key = os.getenv("TMDB_API_KEY")
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    # ... the rest of your function logic ...
    
    try:
        response = requests.get(url)
        data = response.json()
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    except:
        # Fallback if image fails or movie_id is not found
        return "https://via.placeholder.com/500x750?text=No+Poster+Found"

# 4. Load Data
# Ensure these files are in the same directory as app.py
try:
    movies_dict = pickle.load(open('movie_dict.pkl','rb'))
    movies = pd.DataFrame(movies_dict)
    similarity = pickle.load(open('similarity.pkl','rb'))
except FileNotFoundError:
    st.error("Error: Could not find .pkl files. Please check your file directory.")

# 5. UI Header
st.title('🎬 Movie Recommender System')

selected_movie = st.selectbox("Search for a movie you like:", movies['title'].values)

# 6. Recommendation Logic
if st.button('Show Recommendations'):
    movie_index = movies[movies['title'] == selected_movie].index[0]
    distances = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])
    
    # Display 5 recommendations in columns
    cols = st.columns(5)
    
    # We skip the first item (range 1 to 6) because index 0 is the movie itself
    for i in range(1, 6):
        # Fetch data for each recommendation
        recommended_movie_id = movies.iloc[distances[i][0]].movie_id
        recommended_movie_title = movies.iloc[distances[i][0]].title
        
        # Create the Wikipedia URL (replacing spaces with underscores)
        wiki_url = f"https://en.wikipedia.org/wiki/{recommended_movie_title.replace(' ', '_')}"
        
        with cols[i-1]:
            # Movie Title Card
            st.markdown(f'''
                <div style="border: 2px solid rgba(255,255,255,0.1); border-radius: 10px; padding: 5px; background: rgba(0,0,0,0.5); margin-bottom: 10px;">
                    <p style="font-size: 14px; font-weight: bold; text-align: center; color: white; height: 40px; overflow: hidden; display: flex; align-items: center; justify-content: center;">
                        {recommended_movie_title}
                    </p>
                </div>
            ''', unsafe_allow_html=True)
            
            # Movie Poster with Clickable Link
            poster_url = fetch_poster(recommended_movie_id)
            
            # This HTML allows the image to act as a link
            st.markdown(f'''
                <a href="{wiki_url}" target="_blank">
                    <img src="{poster_url}" style="width:100%; border-radius: 10px; transition: 0.3s; cursor: pointer;" onmouseover="this.style.opacity='0.8'" onmouseout="this.style.opacity='1'">
                </a>
            ''', unsafe_allow_html=True)