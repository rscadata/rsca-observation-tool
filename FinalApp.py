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
/* --- Fond global et texte général --- */
.stApp {
    background-color: #F5F5F5;  /* blanc légèrement cassé */
    color: #4B0082;              /* Texte par défaut violet */
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

/* --- Inputs / TextAreas / Selectboxes --- */
.stTextInput input,
.stTextArea textarea,
.stSelectbox select {
    color: #4B0082 !important;     /* Texte saisi violet */
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
.stSelectbox label {
    color: #4B0082 !important;
}

/* --- Progress bars dorées --- */
.stProgress>div>div>div>div {
    background-color: #FFD700;
}

/* --- RADIOS --- */

/* Supprimer le fond et padding des containers parents */
div[data-testid="stVerticalBlock"] > div > div > div[data-testid="stRadio"] {
    background-color: transparent !important;
    padding: 0 !important;
    border: none !important;
}

/* Labels des radios */
div[data-testid="stRadio"] label {
    font-size: 20px !important;                   /* Taille du texte */
    padding: 10px 25px !important;                /* Espace autour du texte */
    margin-right: 15px !important;                /* Espacement horizontal */
    display: inline-block;
    color: #4B0082 !important;                    /* Texte violet */
    border-radius: 8px;
    cursor: pointer;
    transition: background 0.2s;
    background-color: rgba(75, 0, 130, 0.12);     /* Violet légèrement plus foncé */
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
opponent = st.text_input("Opponent")
match_date = st.date_input("Date", value=date.today())

# --- END-OF-MATCH EVALUATION ---
st.header("2. End-of-match evaluation")
st.write("0 = Not applied at all")
st.write("1 = Rarely applied / very weak")
st.write("2 = Applied inconsistently / moderate level")
st.write("3 = Applied consistently / strong impact")

# tactical_fluidity = st.slider("Tactical Fluidity", 0, 3, 0)
# tactical_fluidity = st.radio("Tactical Fluidity", options=[0, 1, 2, 3], index=0, horizontal=True)
# progressive_possession = st.slider("Progressive Possession", 0, 3, 0)
# off_ball_runs = st.slider("Off-Ball Runs", 0, 3, 0)
# counterpress = st.slider("Counterpress", 0, 3, 0)
# fast_transitions = st.slider("Fast Transitions", 0, 3, 0)
# intensity = st.slider("Intensity", 0, 3, 0)
# high_pressing = st.slider("High Pressing", 0, 3, 0)
# offensive_marking = st.slider("Offensive Marking", 0, 3, 0)

tactical_fluidity = st.radio(
    "Tactical Fluidity",
    options=[0, 1, 2, 3],
    index=0,
    horizontal=True
)

progressive_possession = st.radio(
    "Progressive Possession",
    options=[0, 1, 2, 3],
    index=0,
    horizontal=True
)

off_ball_runs = st.radio(
    "Off-Ball Runs",
    options=[0, 1, 2, 3],
    index=0,
    horizontal=True
)

counterpress = st.radio(
    "Counterpress",
    options=[0, 1, 2, 3],
    index=0,
    horizontal=True
)

fast_transitions = st.radio(
    "Fast Transitions",
    options=[0, 1, 2, 3],
    index=0,
    horizontal=True
)

intensity = st.radio(
    "Intensity",
    options=[0, 1, 2, 3],
    index=0,
    horizontal=True
)

high_pressing = st.radio(
    "High Pressing",
    options=[0, 1, 2, 3],
    index=0,
    horizontal=True
)

offensive_marking = st.radio(
    "Offensive Marking",
    options=[0, 1, 2, 3],
    index=0,
    horizontal=True
)


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
#coach_attitude = st.slider("Coach Attitude", 0, 3, 0)
#coach_impact = st.slider("Coach Impact On The Match", 0, 3, 0)

coach_attitude = st.radio(
    "Coach Attitude",
    options=[0, 1, 2, 3],
    index=0,
    horizontal=True
)

coach_impact = st.radio(
    "Coach Impact On The Match",
    options=[0, 1, 2, 3],
    index=0,
    horizontal=True
)

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
        observer_name, category, opponent, str(match_date),
        tactical_fluidity, progressive_possession, off_ball_runs, counterpress,
        fast_transitions, intensity, high_pressing, offensive_marking,
        round(average_players_20,1),
        coach_attitude, coach_impact, round(average_coach_20,1), general_comments,
    ]
    sheet.insert_row(data, 2)
    st.success("✅ Evaluation successfully submitted!")



























