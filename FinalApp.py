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
.stApp {background-color: #F5F5F5; color: #4B0082;}
h1, h2, h3 {color: #4B0082;}
.stButton>button {background-color: #F0F0F0; color: #4B0082; font-weight: bold;}
.stTextInput input, .stTextArea textarea, .stSelectbox select, .stDateInput input {color: #4B0082 !important; background-color: #F0F0F0; border: 1px solid #F0F0F0; caret-color: #4B0082;}
.stTextInput input::placeholder, .stTextArea textarea::placeholder {color: #4B0082 !important; opacity: 0.7;}
.stTextInput label, .stTextArea label, .stSelectbox label, .stDateInput label {color: #4B0082 !important;}
.stProgress>div>div>div>div {background-color: #FFD700;}
div[data-testid="stVerticalBlock"] > div > div > div[data-testid="stRadio"] {background-color: transparent !important; padding: 0 !important; border: none !important;}
div[data-testid="stRadio"] label {font-size: 20px !important; padding: 10px 25px !important; margin-right: 15px !important; display: inline-block; color: #4B0082 !important; border-radius: 8px; cursor: pointer; transition: background 0.2s; background-color: rgba(75, 0, 130, 0.12);}
div[data-testid="stRadio"] label:hover {background-color: rgba(75, 0, 130, 0.18);}
div[data-testid="stRadio"] input:checked + span {background-color: #FFD700 !important; color: #4B0082 !important; border-radius: 8px;}
.css-1d391kg label, .css-1aumxhk {color: #4B0082 !important;}
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



































