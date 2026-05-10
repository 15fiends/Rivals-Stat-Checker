import streamlit as st
import pandas as pd

st.set_page_config(page_title="Rivals Stat Checker", layout="wide")

st.title("Marvel Rivals Stat Checker")
st.write("Browse Marvel Rivals character stats, compare heroes, and explore team roles.")

data = [
    {"name": "Iron Man", "role": "Duelist", "health": 250, "mobility": 5, "damage": 4, "difficulty": 3, "range_type": "Ranged"},
    {"name": "Hulk", "role": "Vanguard", "health": 650, "mobility": 2, "damage": 4, "difficulty": 2, "range_type": "Melee"},
    {"name": "Loki", "role": "Strategist", "health": 275, "mobility": 3, "damage": 3, "difficulty": 4, "range_type": "Ranged"},
    {"name": "Spider-Man", "role": "Duelist", "health": 250, "mobility": 5, "damage": 4, "difficulty": 5, "range_type": "Melee"},
    {"name": "Doctor Strange", "role": "Strategist", "health": 300, "mobility": 2, "damage": 3, "difficulty": 4, "range_type": "Ranged"},
    {"name": "Scarlet Witch", "role": "Duelist", "health": 250, "mobility": 3, "damage": 5, "difficulty": 4, "range_type": "Mid Range"},
    {"name": "Magneto", "role": "Vanguard", "health": 500, "mobility": 2, "damage": 4, "difficulty": 3, "range_type": "Mid Range"},
    {"name": "Storm", "role": "Strategist", "health": 275, "mobility": 4, "damage": 3, "difficulty": 3, "range_type": "Ranged"},
    {"name": "Black Panther", "role": "Duelist", "health": 300, "mobility": 5, "damage": 4, "difficulty": 4, "range_type": "Melee"},
    {"name": "Rocket Raccoon", "role": "Strategist", "health": 250, "mobility": 4, "damage": 2, "difficulty": 3, "range_type": "Ranged"},
    {"name": "Groot", "role": "Vanguard", "health": 700, "mobility": 1, "damage": 3, "difficulty": 2, "range_type": "Melee"},
    {"name": "Punisher", "role": "Duelist", "health": 275, "mobility": 2, "damage": 5, "difficulty": 2, "range_type": "Ranged"},
    {"name": "Mantis", "role": "Strategist", "health": 250, "mobility": 3, "damage": 2, "difficulty": 2, "range_type": "Ranged"},
    {"name": "Venom", "role": "Vanguard", "health": 600, "mobility": 4, "damage": 4, "difficulty": 3, "range_type": "Melee"},
    {"name": "Star-Lord", "role": "Duelist", "health": 250, "mobility": 4, "damage": 4, "difficulty": 3, "range_type": "Ranged"}
]

df = pd.DataFrame(data)

st.sidebar.header("Filters")

role_filter = st.sidebar.selectbox("Filter by role", ["All"] + sorted(df["role"].unique().tolist()))
search_text = st.sidebar.text_input("Search for a character")
min_health = st.sidebar.slider("Minimum health", 200, 700, 200)
min_damage = st.sidebar.slider("Minimum damage", 1, 5, 1)

if role_filter != "All":
    df = df[df["role"] == role_filter]

if search_text.strip() != "":
    df = df[df["name"].str.contains(search_text, case=False, na=False)]

df = df[df["health"] >= min_health]
df = df[df["damage"] >= min_damage]

st.subheader("Roster Overview")

col1, col2, col3 = st.columns(3)
col1.metric("Characters Shown", len(df))
col2.metric("Average Health", round(df["health"].mean(), 1) if not df.empty else 0)
col3.metric("Average Damage", round(df["damage"].mean(), 1) if not df.empty else 0)

st.dataframe(df, use_container_width=True, hide_index=True)

if not df.empty:
    st.subheader("Character Detail Viewer")
    selected_character = st.selectbox("Choose a character to view details", df["name"].tolist())
    character_info = df[df["name"] == selected_character].iloc[0]

    detail_col1, detail_col2 = st.columns(2)
    detail_col1.write(f"**Name:** {character_info['name']}")
    detail_col1.write(f"**Role:** {character_info['role']}")
    detail_col1.write(f"**Health:** {character_info['health']}")
    detail_col2.write(f"**Mobility:** {character_info['mobility']}")
    detail_col2.write(f"**Damage:** {character_info['damage']}")
    detail_col2.write(f"**Difficulty:** {character_info['difficulty']}")
    st.write(f"**Range Type:** {character_info['range_type']}")

    st.subheader("Quick Stat Chart")
    chart_df = pd.DataFrame({
        "Stat": ["Health", "Mobility", "Damage", "Difficulty"],
        "Value": [
            character_info["health"],
            character_info["mobility"],
            character_info["damage"],
            character_info["difficulty"]
        ]
    })
    st.bar_chart(chart_df.set_index("Stat"))

    st.subheader("Character Comparison")
    compare_options = df["name"].tolist()
    compare_character_1 = st.selectbox("First character", compare_options, key="compare1")
    compare_character_2 = st.selectbox("Second character", compare_options, key="compare2")

    compare_df = df[df["name"].isin([compare_character_1, compare_character_2])]
    st.dataframe(compare_df, use_container_width=True, hide_index=True)

else:
    st.warning("No characters match your current filters.")
