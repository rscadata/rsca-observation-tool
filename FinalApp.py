import streamlit as st
import pandas as pd
import os
from datetime import date
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- CONNEXION À GOOGLE SHEETS ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Récupérer les credentials depuis les secrets Streamlit
credentials_dict = st.secrets["google_sheets"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
client = gspread.authorize(creds)

sheet = client.open_by_url(
    "https://docs.google.com/spreadsheets/d/11_32CeQAy9w0_Bqv8kZoZhw0Vrd8AQk90aL801XshMw/edit"
).sheet1

# --- PARAMÉTRAGE DE L'AFFICHAGE (CSS) ---
st.markdown("""
<style>
/* Fond global violet Anderlecht */
.stApp {
    background-color: #4B0082;
    color: white;
}
/* Titres principaux et sous-titres */
h1, h2, h3 {
    color: white;
}
/* Boutons */
.stButton>button {
    background-color: #F0F0F0;
    color: #4B0082;
    font-weight: bold;
}
/* Champs texte et text area */
.stTextInput>div>div>input,
.stTextArea>div>div>textarea {
    border: 1px solid #F0F0F0;
    background-color: #F0F0F0;
    color: black;
    caret-color: #4B0082;
}
/* Selectbox / dropdown */
.stSelectbox>div>div>div>select {
    background-color: #F0F0F0;
    color: black;
    border: 1px solid #F0F0F0;
}
/* Slider texte labels */
.css-1d391kg label, .css-1aumxhk {
    color: white;
}
/* Progress bars */
.stProgress>div>div>div>div {
    background-color: #FFD700;
}
</style>
""", unsafe_allow_html=True)

# --- TITRE DE LA PAGE ---  
st.title("Observation tool RSCA")
st.write("Welcome to the RSCA Academy Match Evaluation App!")

# --- PRE MATCH INFORMATION ---
st.header("1. Pre-match information")
observer_name = st.text_input("Observer name")
category = st.selectbox("Category", ["U8", "U9", "U10", "U11", "U12", "U13", "U14", "U15", "U16", "U18"])
opponent = st.text_input("Opponent")
match_date = st.date_input("Date", value=date.today())

competition_type = st.text_input("Competition / Training type")

# --- END-OF-MATCH EVALUATION ---
st.header("2. End-of-match evaluation")
st.write("0 = Not applied at all")
st.write("1 = Rarely applied / very weak")
st.write("2 = Applied inconsistently / moderate level")
st.write("3 = Applied consistently / strong impact")

# tactical_fluidity = st.slider("Tactical Fluidity", 0, 3, 0)
tactical_fluidity = st.segmented_control(
    "Tactical Fluidity",
    options=[0, 1, 2, 3],
    default=0
)
progressive_possession = st.slider("Progressive Possession", 0, 3, 0)
off_ball_runs = st.slider("Off-Ball Runs", 0, 3, 0)
counterpress = st.slider("Counterpress", 0, 3, 0)
fast_transitions = st.slider("Fast Transitions", 0, 3, 0)
intensity = st.slider("Intensity", 0, 3, 0)
high_pressing = st.slider("High Pressing", 0, 3, 0)
offensive_marking = st.slider("Offensive Marking", 0, 3, 0)

player_scores = [
    tactical_fluidity, progressive_possession, off_ball_runs,
    counterpress, fast_transitions, intensity, high_pressing, offensive_marking
]
average_players = sum(player_scores) / len(player_scores)
average_players_20 = (average_players / 3) * 20
st.subheader("Team evaluation average")
st.write(f"Average score: {average_players_20:.1f}/20")
st.progress(int((average_players_20/20)*100))

# --- COACH EVALUATION ---
st.header("3. Coach evaluation")
coach_attitude = st.slider("Coach Attitude", 0, 3, 0)
coach_impact = st.slider("Coach Impact On The Match", 0, 3, 0)

coach_scores = [coach_attitude, coach_impact]
average_coach = sum(coach_scores) / len(coach_scores)
average_coach_20 = (average_coach / 3) * 20
st.subheader("Coach evaluation average")
st.write(f"Average score: {average_coach_20:.1f}/20")
st.progress(int((average_coach_20/20)*100))

# --- GENERAL COMMENTS ---
st.header("4. Comments")
general_comments = st.text_area("General Comments")

# --- SUBMIT BUTTON ---
if st.button("Submit evaluation"):
    data = [
        observer_name, category, opponent, str(match_date), competition_type,
        tactical_fluidity, progressive_possession, off_ball_runs, counterpress,
        fast_transitions, intensity, high_pressing, offensive_marking,
        round(average_players_20,1),
        coach_attitude, coach_impact, round(average_coach_20,1), general_comments,
    ]
    sheet.insert_row(data, 2)
    st.success("✅ Evaluation successfully submitted!")





