import streamlit as st  # Bibliotek för att bygga webbappar i Python
import httpx            # HTTP-klient för att anropa backend-API:et

def init_session_states():
    # Streamlit kör om hela skriptet vid varje interaktion,
    # så session_state används för att spara data mellan körningarna

    if "messages" not in st.session_state:
        # Skapar en tom lista för chattmeddelanden (visas i gränssnittet)
        st.session_state.messages = []

    if "message_history" not in st.session_state:
        # Skapar en tom lista för historiken som skickas till backend
        # (så att boten kommer ihåg samtalet)
        st.session_state.message_history = []


def display_chat_messages():
    # Går igenom alla sparade meddelanden och ritar ut dem
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):  # "user" eller "assistant" ger rätt ikon/stil
            st.markdown(message["content"])     # Visar meddelandetexten


def handle_user_input():
    # Visar ett inmatningsfält och sparar texten i "prompt" om användaren skickat något
    if prompt := st.chat_input("Talk to the JokeBot"):
        # Sparar användarens meddelande i listan
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Skickar frågan och tidigare historik till backend (körs lokalt på port 8000)
        response = httpx.post(
            "http://127.0.0.1:8000/chat",
            json={
                "question": prompt, "message_history": st.session_state.message_history
            },
            timeout=60,
        ).json()  # Omvandlar svaret från JSON till en Python-dict

        # Uppdaterar historiken med den nya versionen från backend
        st.session_state.message_history = response.get("message_history")

        # Hämtar botens svar
        bot_response = response.get("response")
        st.write(bot_response)  # Skriver ut svaret direkt (se notering nedan)

        # Lägger till botens namn framför svaret
        response = f"Ro Båt: {bot_response}"

        # Visar användarens fråga och botens svar som chattbubblor
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            st.markdown(response)

        # Sparar botens svar så det visas vid nästa omritning
        st.session_state.messages.append({"role": "assistant", "content": response})

def layout():
    # Bygger sidans utseende
    st.markdown("# Chat with Ro Båt") 
    st.write("Ro Båt is a fynny robot that will answer with programming joke")  # Beskrivning

    display_chat_messages()  # Visar tidigare meddelanden
    handle_user_input()      # Hanterar ny inmatning


if __name__ == "__main__":
    # Startpunkt: förbereder session_state och ritar sedan upp sidan
    init_session_states()
    layout()