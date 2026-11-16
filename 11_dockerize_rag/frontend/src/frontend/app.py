import streamlit as st
import requests
from pathlib import Path
import os

BASE_URL = os.getenv("API_URL", default="http://127.0.0.1:8000") 

ASSETS_PATH = Path(__file__).absolute().parents[1] / "assets"

def layout():
    st.markdown("# Ragbit")
    st.markdown("Ask a question about diffrent dwarf rabbits")
    text_input = st.text_input(label= "Ask a question")

    if st.button("Send") and text_input != "":
        response = requests.post(f"{BASE_URL}/rag/query", json={"prompt": text_input})
       # st.write(response.status_code)
       # st.write(response.text)

        data = response.json()

        st.markdown("## Question:")
        st.markdown(text_input)

        st.markdown("## Answer:")
        st.markdown(data["answer"])

        st.markdown("## Source:")
        st.markdown(data["filepath"])

        st.image(ASSETS_PATH / f"{data['filename']}.png")


if __name__ == "__main__":
    layout()