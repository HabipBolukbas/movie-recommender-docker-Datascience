🎬 Movie Recommender System
A content-based movie recommendation engine built with Python and Streamlit, featuring a Dockerized environment for easy deployment. 

🌟 Key Features
Content-Based Filtering: Recommends movies using Cosine Similarity on a pre-processed TMDB dataset.

Cinematic User Interface: A custom-styled Streamlit UI featuring a dark "Netflix-inspired" theme and responsive movie cards.

Dynamic Poster Fetching: Integrates with the TMDB API to display real-time movie posters for every recommendation.

Secure API Handling: Uses python-dotenv to keep API keys private and out of the source code.

Containerized Environment: Fully portable and reproducible setup using Docker and Docker Compose.

🛠️ Technical Stack
Language: Python 3.11+

Frontend: Streamlit

Data Science: Pandas, Scikit-learn, Pickle

API: TMDB (The Movie Database)

DevOps: Docker, Docker Compose, Git LFS



🚀 How to Run (The Easy Way)
This project is fully "Dockerized," so you don't need to install Python or libraries manually.

Clone the repository to your local machine.

Add your API Key:

Create a file named .env in the main folder.

Add this line inside: TMDB_API_KEY=your_key_here.

Launch the app: Open your terminal in the project folder and run:

Bash

docker-compose up --build
View the app: Go to http://localhost:8501 in your browser.

📂 What's Inside?
app.py: The main code for the website and recommendation logic.

similarity.pkl: The AI model that calculates which movies are similar.

Dockerfile & docker-compose.yml: The "recipe" that tells Docker how to run the app.

.env: (You create this) Keeps your API key safe and private.

