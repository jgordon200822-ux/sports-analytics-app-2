import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Sports Prediction App", layout="wide")

# ---------------- DATA ---------------- #

players = {
    "LeBron James": {
        "image": "https://cdn.nba.com/headshots/nba/latest/1040x760/2544.png",
        "instagram": "https://instagram.com/kingjames",
        "impact": 92
    },
    "Jayson Tatum": {
        "image": "https://cdn.nba.com/headshots/nba/latest/1040x760/1628369.png",
        "instagram": "https://instagram.com/jaytatum0",
        "impact": 88
    }
}

teams = {
    "Lakers": {"rating": 85, "star": "LeBron James"},
    "Celtics": {"rating": 88, "star": "Jayson Tatum"}
}

if "bets" not in st.session_state:
    st.session_state.bets = []

if "odds" not in st.session_state:
    st.session_state.odds = {"Lakers": 1.8, "Celtics": 2.0}

# ---------------- LOGIC ---------------- #

def adjust_odds():
    total = len(st.session_state.bets)
    if total == 0:
        return
    for team in st.session_state.odds:
        count = sum(1 for b in st.session_state.bets if b["team"] == team)
        pressure = count / total
        st.session_state.odds[team] = round(
            max(1.2, st.session_state.odds[team] * (1 + (pressure - 0.5) * 0.2)), 2
        )

# ---------------- UI ---------------- #

st.title("📊 Sports Prediction Platform")

mode = st.sidebar.selectbox("Mode", ["User", "Admin"])

# USER VIEW
if mode == "User":
    team = st.selectbox("Pick a team", teams.keys())
    stake = st.slider("Stake (points)", 10, 500, 100)

    star = teams[team]["star"]
    player = players[star]

    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(player["image"], width=220)
    with col2:
        st.subheader(star)
        st.markdown(f"[Instagram]({player['instagram']})")

    st.write(f"### Odds: {st.session_state.odds[team]}")

    if st.button("Submit Pick"):
        st.session_state.bets.append({
            "team": team,
            "stake": stake,
            "odds": st.session_state.odds[team],
            "time": datetime.now().strftime("%H:%M:%S")
        })
        adjust_odds()
        st.success("Pick submitted!")

# ADMIN VIEW
if mode == "Admin":
    pw = st.text_input("Admin password", type="password")
    if pw == "admin123":
        st.subheader("🛠 Admin Panel")
        st.write("Current Odds")
        st.json(st.session_state.odds)
        st.write("All Picks")
        st.table(st.session_state.bets)
        if st.button("Reset Market"):
            st.session_state.bets = []
            st.session_state.odds = {"Lakers": 1.8, "Celtics": 2.0}
            st.success("Market reset")
