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
/* --- Fond global et texte général --- */
.stApp {
    background-color: #F5F5F5; /* blanc légèrement cassé */
    color: #4B0082;             /* Texte par défaut violet */
}

/* Titres principaux */
h1, h2, h3 {
    color: #4B0082;
}

/* --- Boutons --- */
.stButton>button {
    background-color: #F0F0F0;
    color: #4B0082;
    font-weight: bold;
}

/* --- Inputs / TextAreas / Selectboxes / DateInput --- */
.stTextInput input,
.stTextArea textarea,
.stSelectbox select,
.stDateInput input {                   /* <-- ajout de stDateInput ici */
    color: #4B0082 !important;        /* Texte saisi violet */
    background-color: #F0F0F0;
    border: 1px solid #F0F0F0;
    caret-color: #4B0082;
}

/* Placeholder texte violet */
.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #4B0082 !important;
    opacity: 0.7;
}

/* Labels (Observer name, Opponent, Category...) */
.stTextInput label,
.stTextArea label,
.stSelectbox label,
.stDateInput label {                
    color: #4B0082 !important;
}

/* --- RADIOS --- */
div[data-testid="stVerticalBlock"] > div > div > div[data-testid="stRadio"] {
    background-color: transparent !important;
    padding: 0 !important;
    border: none !important;
}

/* Labels des radios */
div[data-testid="stRadio"] label {
    font-size: 20px !important;
    padding: 10px 25px !important;
    margin-right: 15px !important;
    display: inline-block;
    color: #4B0082 !important; 
    border-radius: 8px;
    cursor: pointer;
    transition: background 0.2s;
    background-color: rgba(75, 0, 130, 0.12);
}

/* Hover léger pour radios */
div[data-testid="stRadio"] label:hover {
    background-color: rgba(75, 0, 130, 0.18);
}

/* Fond doré pour option radio sélectionnée */
div[data-testid="stRadio"] input:checked + span {
    background-color: #FFD700 !important;
    color: #4B0082 !important;
    border-radius: 8px;
}

/* Slider / radio texte labels (optionnel selon ton Streamlit) */
.css-1d391kg label, .css-1aumxhk {
    color: #4B0082 !important;
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
activity_type = st.selectbox("Activity type", ["Match", "Training"])

if activity_type == "Match":
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
    free_man = st.radio("Play the free man or commit", [0,1,2,3], index=0, horizontal=True)
    create_overload = st.radio("Create overload", [0,1,2,3], index=0, horizontal=True)
    st.subheader("Progression")
    buildUp_finish = st.radio("From Build-up to finish", [0,1,2,3], index=0, horizontal=True)
    offBall_breaking = st.radio("Off-ball runs ➡️ Breaking lines", [0,1,2,3], index=0, horizontal=True)
    

elif activity_type == "Training":
    ssg = st.radio("Small sided games (zone)", [0,1,2,3], index=0, horizontal=True)
    decision_making = st.radio("Decision making", [0,1,2,3], index=0, horizontal=True)

# --- GENERAL COMMENTS ---
st.header("4. Comments")
general_comments = st.text_area("General Comments")

# --- SUBMIT BUTTON ---
if st.button("Submit evaluation"):

    if activity_type == "Match":
        data = [observer_name, category, opponent, str(match_date)]
        data.extend([free_man, create_overload, buildUp_finish, offBall_breaking, general_comments])
        sheet_to_use = client.open_by_url(
            "https://docs.google.com/spreadsheets/d/11_32CeQAy9w0_Bqv8kZoZhw0Vrd8AQk90aL801XshMw/edit"
        ).worksheet("Match Data")

    elif activity_type == "Training":
        data = [observer_name, category, str(match_date)]
        data.extend([ssg, decision_making, general_comments])
        sheet_to_use = client.open_by_url(
            "https://docs.google.com/spreadsheets/d/11_32CeQAy9w0_Bqv8kZoZhw0Vrd8AQk90aL801XshMw/edit"
        ).worksheet("Training Data")

    sheet_to_use.insert_row(data, 2)
    st.success(f"✅ {activity_type} evaluation successfully submitted!")













































