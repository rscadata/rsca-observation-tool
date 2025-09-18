import streamlit as st
import pandas as pd
from datetime import date
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- CONNEXION À GOOGLE SHEETS ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

credentials_dict = st.secrets["google_sheets"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
client = gspread.authorize(creds)

# --- AFFICHAGE (CSS) ---
st.markdown(""" 
<style>
/* Ton CSS de base est inchangé */

/* --- AJOUT POUR SEGMENTED CONTROL AVEC FOND CLAIR --- */
div[data-baseweb="segmented-control"] {
    background-color: #F0F0F0 !important;  /* Fond global gris clair */
    border-radius: 12px !important;
    padding: 4px !important;
}

div[data-baseweb="segmented-control"] button {
    background-color: #F0F0F0 !important;  /* Chaque option non sélectionnée -> gris clair */
    color: #4B0082 !important;             /* Texte violet */
    font-weight: bold !important;
    border-radius: 10px !important;
    border: none !important;
    transition: all 0.2s ease-in-out;
}

div[data-baseweb="segmented-control"] button:hover {
    background-color: rgba(75, 0, 130, 0.12) !important; /* Léger violet au survol */
}

div[data-baseweb="segmented-control"] button[aria-checked="true"] {
    background-color: #FFD700 !important;  /* Option sélectionnée -> fond doré */
    color: #4B0082 !important;             /* Texte violet */
}
</style>
""", unsafe_allow_html=True)


# --- TITRE DE LA PAGE ---  
st.title("METHODOLOGY GAME OBSERVATION")
st.write("Welcome to the RSCA Academy Game Evaluation tool!")

# --- PRE MATCH INFORMATION ---
st.header("1. Pre-match information")
observer_name = st.text_input("Observer name")
category = st.selectbox("Category", ["U23", "U18", "U16", "U15", "U14", "U13", "U12", "U11", "U10"])
#activity_type = st.selectbox("Activity type", ["Match", "Training"])
activity_type = st.segmented_control("Choose activity type:", options=["Match", "Training"], default="Match")
opponent = st.text_input("Opponent")
match_date = st.date_input("Date", value=date.today())

# --- EVALUATION ---
st.header("2. Evaluation")
st.write("0 = Not applied at all")
st.write("1 = Rarely applied / very weak")
st.write("2 = Applied inconsistently / moderate level")
st.write("3 = Applied consistently / strong impact")


if activity_type == "Match":
    st.subheader("Build-up")
    tactical_fluidity = st.radio("Tactical Fluidity", [0,1,2,3], index=0, horizontal=True)
    progressive_possession = st.radio("Progressive Possession", [0,1,2,3], index=0, horizontal=True)
    st.subheader("Progression")
    off_ball_runs = st.radio("Off-Ball Runs", [0,1,2,3], index=0, horizontal=True)
    player_scores = [tactical_fluidity, progressive_possession, off_ball_runs]

elif activity_type == "Training":
    high_pressing = st.radio("High Pressing", [0,1,2,3], index=0, horizontal=True)
    offensive_marking = st.radio("Offensive Marking", [0,1,2,3], index=0, horizontal=True)
    player_scores = [high_pressing, offensive_marking]

# --- GENERAL COMMENTS ---
st.header("4. Comments")
general_comments = st.text_area("General Comments")

# --- SUBMIT BUTTON ---
if st.button("Submit evaluation"):
    data = [observer_name, category, opponent, str(match_date)]

    if activity_type == "Match":
        data.extend([tactical_fluidity, progressive_possession, off_ball_runs, general_comments])
        sheet_to_use = client.open_by_url(
            "https://docs.google.com/spreadsheets/d/11_32CeQAy9w0_Bqv8kZoZhw0Vrd8AQk90aL801XshMw/edit"
        ).worksheet("Match Data")

    elif activity_type == "Training":
        data.extend([high_pressing, offensive_marking, general_comments])
        sheet_to_use = client.open_by_url(
            "https://docs.google.com/spreadsheets/d/11_32CeQAy9w0_Bqv8kZoZhw0Vrd8AQk90aL801XshMw/edit"
        ).worksheet("Training Data")

    sheet_to_use.insert_row(data, 2)
    st.success(f"✅ {activity_type} evaluation successfully submitted!")





































