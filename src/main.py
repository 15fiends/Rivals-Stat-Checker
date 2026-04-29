import streamlit as st
import pandas as pd

st.set_page_config(page_title="Rivals Stat Checker", layout="wide")

st.title("Marvel Rivals Stat Checker")
st.write("This app lets users browse Marvel Rivals character stats.")

data = [
    {"name": "Iron Man", "role": "Duelist", "health": 250, "mobility": 5, "damage": 4},
    {"name": "Hulk", "role": "Vanguard", "health": 650, "mobility": 2, "damage": 4},
    {"name": "Loki", "role": "Strategist", "health": 275, "mobility": 3, "damage": 3},
    {"name": "Spider-Man", "role": "Duelist", "health": 250, "mobility": 5, "damage": 4},
    {"name": "Doctor Strange", "role": "Strategist", "health": 300, "mobility": 2, "damage": 3},
    {"name": "Scarlet Witch", "role": "Duelist", "health": 250, "mobility": 3, "damage": 5},
    {"name": "Magneto", "role": "Vanguard", "health": 500, "mobility": 2, "damage": 4},
    {"name": "Storm", "role": "Strategist", "health": 275, "mobility": 4, "damage": 3},
    {"name": "Black Panther", "role": "Duelist", "health": 300, "mobility": 5, "damage": 4},
    {"name": "Rocket Raccoon", "role": "Strategist", "health": 250, "mobility": 4, "damage": 2},
    {"name": "Groot", "role": "Vanguard", "health": 700, "mobility": 1, "damage": 3},
    {"name": "Punisher", "role": "Duelist", "health": 275, "mobility": 2, "damage": 5},
    {"name": "Mantis", "role": "Strategist", "health": 250, "mobility": 3, "damage": 2},
    {"name": "Venom", "role": "Vanguard", "health": 600, "mobility": 4, "damage": 4},
    {"name": "Star-Lord", "role": "Duelist", "health": 250, "mobility": 4, "damage": 4}
]

df = pd.DataFrame(data)

role_filter = st.selectbox("Filter by role", ["All"] + sorted(df["role"].unique().tolist()))
search_text = st.text_input("Search for a character")

if role_filter != "All":
    df = df[df["role"] == role_filter]

if search_text.strip() != "":
    df = df[df["name"].str.contains(search_text, case=False, na=False)]

st.dataframe(df, use_container_width=True, hide_index=True)
