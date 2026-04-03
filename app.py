import requests

API_KEY = "1053464a-7270-42bb-"

def get_live_matches():
    url = f"https://api.cricapi.com/v1/currentMatches?apikey={API_KEY}&offset=0"
    response = requests.get(url)
    data = response.json()
    return dataimport streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Cricket AI Predictor", layout="wide")

players_data = pd.DataFrame({
    "player": ["Kohli","Rohit","Dhoni","Sky","Bumrah","Jadeja","Russell","Gill"],
    "team": ["RCB","MI","CSK","MI","MI","CSK","KKR","GT"],
    "avg": [52, 48, 39, 42, 10, 30, 28, 50],
    "sr": [140, 135, 130, 160, 90, 125, 170, 145],
    "wickets": [0, 0, 0, 0, 150, 120, 95, 0],
    "economy": [0, 0, 0, 0, 6.5, 7.2, 8.5, 0],
    "recent": [60, 55, 50, 65, 70, 68, 72, 66]
})

def compute_scores(df):
    df['batting_score'] = df['avg']*0.4 + df['sr']*0.3 + df['recent']*0.3
    df['bowling_score'] = df['wickets']*0.4 - df['economy']*0.3 + df['recent']*0.3
    return df

players_data = compute_scores(players_data)

def team_strength(team):
    team_df = players_data[players_data['team'] == team]
    return team_df['batting_score'].sum(), team_df['bowling_score'].sum()

def simulate(t1, t2, n=500):
    t1_wins, t2_wins = 0, 0
    s1, s2 = [], []

    for _ in range(n):
        score1 = np.random.normal(t1[0]*0.8 + t2[1]*0.2, 15)
        score2 = np.random.normal(t2[0]*0.8 + t1[1]*0.2, 15)

        s1.append(score1)
        s2.append(score2)

        if score1 > score2:
            t1_wins += 1
        else:
            t2_wins += 1

    return {
        "t1_win": t1_wins/n,
        "t2_win": t2_wins/n,
        "s1": int(np.mean(s1)),
        "s2": int(np.mean(s2))
    }

def live_pred(score, overs, target, wickets):
    if overs == 0:
        return 50
    req = (target - score) / (20 - overs + 0.1)
    pressure = wickets*2 + req*3
    return max(0, min(100, 100 - pressure*5))

st.title("🏏 Cricket AI Predictor")

teams = ["CSK","MI","RCB","KKR","GT"]

col1, col2 = st.columns(2)

with col1:
    team1 = st.selectbox("Team 1", teams)

with col2:
    team2 = st.selectbox("Team 2", teams)

if st.button("Predict Match"):
    t1 = team_strength(team1)
    t2 = team_strength(team2)

    result = simulate(t1, t2)

    st.subheader("🏆 Win Probability")
    st.write(f"{team1}: {result['t1_win']*100:.2f}%")
    st.write(f"{team2}: {result['t2_win']*100:.2f}%")

    st.subheader("📊 Score Prediction")
    st.write(f"{team1}: {result['s1']}")
    st.write(f"{team2}: {result['s2']}")

    st.subheader("🎲 Toss")
    st.write("50% - 50%")

st.markdown("---")
st.subheader("📡 Live Match Predictor")

score = st.number_input("Score", 0)
overs = st.number_input("Overs", 0.0)
target = st.number_input("Target", 0)
wickets = st.number_input("Wickets", 0)

if st.button("Update Live"):
    prob = live_pred(score, overs, target, wickets)
    st.write(f"Win Probability: {prob:.2f}%")
st.markdown("---")
st.subheader("📡 Live IPL Matches")

if st.button("Fetch Live Matches"):
    data = get_live_matches()
    
    if "data" in data:
        for match in data["data"]:
            st.write("### 🏏", match["name"])
            st.write("Status:", match["status"])
            st.write("Teams:", match["teams"])
            st.write("Score:", match.get("score", "N/A"))
            st.markdown("---")
    else:
        st.write("No live matches available")
