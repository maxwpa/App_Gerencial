import streamlit as st
from datetime import datetime, time, date, timedelta
import firebase_admin
from firebase_admin import credentials, db, initialize_app

# Load Firebase credentials
cred = credentials.Certificate("tempo-329ad-firebase-adminsdk-fc9sq-11d8bd1d0e.json")

# Check if the app is already initialized
try:
    app = firebase_admin.get_app()
except ValueError:
    app = initialize_app(cred, options={'databaseURL': 'https://tempo-329ad-default-rtdb.firebaseio.com/'})

# Function to calculate time difference in minutes
def calculate_time_difference():
    current_time = datetime.now().time()
    target_time = time(12, 30, 45)
    time_difference_minutes = (datetime.combine(date.today(), target_time) - datetime.combine(date.today(), current_time)).total_seconds() / 60
    return int(time_difference_minutes)

# Reference to the '/tempo' node in the Firebase Realtime Database
db_ref = db.reference('/tempo', app=app)

# Streamlit UI
st.title("Tempo App")

# Botão para atualizar a variável tempo
if st.button("Atualizar Tempo"):
    tempo_atualizado = calculate_time_difference()

    # Prepare the data to be updated in Firebase
    data = {
        'tempo': tempo_atualizado,  # Store as integer in minutes
    }

    # Update data in Firebase
    db_ref.update(data)

    st.write('Tempo atualizado:', tempo_atualizado)
else:
    st.write('Tempo atual:', calculate_time_difference())

