import streamlit as st
import pickle
import pandas as pd
import difflib
import requests

page_bg_img = '''
<style>
[data-testid="stApp"] {
background-image: url('https://i.redd.it/4ctdd8dfwy8b1.jpg');
background-size: cover;
}
[data-testid="stHeader"]{
padding: 10px;
background-color: rgba(0,0,0,0);
}
[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: rgba(255, 255, 255, 0.5);  /* White background with 50% opacity */
    padding: 10px;
    border-radius: 10px;
}
.block-container {
    max-width: 80%; /* Adjust this to your desired width */
    padding: 30px;
}
</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=a0c9c39f251c922d0fdf82738b5b9ded&language=en-US".format(movie_id[0])
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie, movies_data):
    list_of_all_titles = movies_data['title'].tolist()
    find_close_match = difflib.get_close_matches(movie, list_of_all_titles)
    close_match = find_close_match[0]
    index_of_the_movie = movies_data[movies_data.title == close_match]['index'].values[0]
    similarity_score = list(enumerate(similarity[index_of_the_movie]))
    sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)
    
    i = 0
    recommended_movies = []
    recommended_movies_posters = []
    
    for movie in sorted_similar_movies:
        index = movie[0]
        title_from_index = movies_data[movies_data.index == index]['title'].values[0]
        if i < 5:  # Fix to get only the top 5 recommendations
            movie_id = movies_data[movies_data.index == index]['id'].values
            recommended_movies_posters.append(fetch_poster(movie_id))
            recommended_movies.append(title_from_index)
            i += 1
            
    return recommended_movies, recommended_movies_posters

movies_data = pickle.load(open("movies_data.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

st.title(":blue[Movie Recommendation System]:snow_cloud:")

selected_movie = st.selectbox(
    'Choose Movie',
    movies_data['title']
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie, movies_data)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0], use_column_width=True)
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1], use_column_width=True)
    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2], use_column_width=True)
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3], use_column_width=True)
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4], use_column_width=True)


