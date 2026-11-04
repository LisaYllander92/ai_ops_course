# Vi har nu en fungerande API som lagrar data till databasen baserat på en fråga/statement.
# Vill ha en frontend där man kan ställa en fråga och den ska spara till databasen. Vill också kunna filtrera på ex genres

import streamlit as st
import requests


def layout():
    st.markdown("# Cool Movies")

    movie_string = st.text_input("Give a statement and it will give back a movie")

    movie = requests.post(
        "http://127.0.0.1:8000/movie", json={"query": movie_string}
    ).json()

    genre = st.selectbox(
        "Choose genre",
        options=["action", "comedy", "cartoon", "romance", "thriller", "adventure"],
    )
    # Skriver ut filmerna som vi fått fram
    movies = requests.get(f"http://127.0.0.1:8000/movies?genre={genre}").json()

    st.dataframe(movies)


if __name__ == "__main__":
    layout()
