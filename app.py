import streamlit as st
import pickle
import pandas as pd
import requests
import os
import gdown

# def fetch_poster(movie_id):
#     response = requests.get('https://api.themoviedb.org/3/movie/{movie.id}?api_key=67b694a77890f7c184df2be74ccb118b&language=en-US')
#     data = response.json()
#     return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]

FILE_ID = "1RX2zKonVYKaWmT9FsJaPs9ngKmBOpAt2"
FILE_PATH = "similarity.pkl"

if not os.path.exists(FILE_PATH):
    gdown.download(
        f"https://drive.google.com/uc?id={FILE_ID}",
        FILE_PATH,
        quiet=False
    )

similarity = pickle.load(open(FILE_PATH, "rb"))

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=67b694a77890f7c184df2be74ccb118b&language=en-US"

    print("Fetching:", movie_id)

    print(movies["movie_id"].dtype)
    print(movies["movie_id"].head())

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        print("Status:", response.status_code)

        data = response.json()

        if data.get("poster_path"):
            return "https://image.tmdb.org/t/p/w500" + data["poster_path"]
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster"

    except Exception as e:
        print("ERROR:", movie_id, e)
        return "https://via.placeholder.com/500x750?text=Error"



def recommend (movie):
    movie_index=movies[movies['title']==movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

    recommended_movies=[]
    recommended_movies_posters=[]
    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        #fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies, recommended_movies_posters

movies_dict=pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)

#similarity=pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommendation System')
selected_movie_name=st.selectbox(
    'Select the movie you liked: ',
    movies['title'].values
)

#print(requests.get("https://www.google.com").status_code)
#print(requests.get("https://api.themoviedb.org").status_code)

if st.button('Recommend'):
    names,posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5, vertical_alignment='bottom')

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])