import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="Movie Recommendation System", page_icon="🎬")

st.title("🎬 Movie Recommendation System")
st.write("Select a movie to get similar movie recommendations.")

# Load Dataset
movies = pd.read_csv("movies.csv")

# Combine features
movies["tags"] = (
    movies["Genre"] + " " +
    movies["Director"] + " " +
    movies["Actors"]
)

# Convert text into vectors
vectorizer = TfidfVectorizer(stop_words="english")
vectors = vectorizer.fit_transform(movies["tags"])

# Calculate similarity
similarity = cosine_similarity(vectors)

# Recommendation Function
def recommend(movie_name):
    index = movies[movies["Title"] == movie_name].index[0]
    distances = similarity[index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommendations = []

    for i in movie_list:
        recommendations.append(movies.iloc[i[0]].Title)

    return recommendations

# Dropdown
selected_movie = st.selectbox(
    "Choose a Movie",
    movies["Title"].values
)

if st.button("Recommend"):
    st.subheader("Recommended Movies")

    recommendations = recommend(selected_movie)

    for movie in recommendations:
        st.success(movie)