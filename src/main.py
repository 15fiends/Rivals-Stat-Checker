import streamlit as st
import pandas as pd

st.set_page_config(page_title="Rivals Stat Checker", layout="wide")

st.title("Marvel Rivals Stat Checker")
st.write("This app lets users browse Marvel Rivals character stats.")

data = [
    {"name": "Iron Man", "role": "Duelist", "health": 250, "mobility": 5, "damage": 4},
    {"name": "Hulk", "role": "Vanguard", "health": 650, "mobility": 2, "damage": 4},
    {"name": "Loki", "role": "Strategist", "health": 275, "mobility": 3, "damage": 3}
]

df = pd.DataFrame(data)

role_filter = st.selectbox("Filter by role", ["All"] + sorted(df["role"].unique().tolist()))

if role_filter != "All":
    df = df[df["role"] == role_filter]

st.dataframe(df, use_container_width=True, hide_index=True)
