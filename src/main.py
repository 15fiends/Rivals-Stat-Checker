import streamlit as st
import pandas as pd

st.set_page_config(page_title="Rivals Stat Checker", layout="wide")

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(to bottom, #0b1020, #111827);
        color: #f3f4f6;
    }

    h1, h2, h3 {
        color: #ffffff;
    }

    .custom-card {
        background-color: #1f2937;
        padding: 18px;
        border-radius: 14px;
        border: 1px solid #374151;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25);
        margin-bottom: 15px;
    }

    .stat-label {
        color: #9ca3af;
        font-size: 14px;
    }

    .stat-value {
        color: #ffffff;
        font-size: 24px;
        font-weight: bold;
    }

    .section-title {
        color: #f9fafb;
        margin-top: 10px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.title("Marvel Rivals Stat Checker")
st.write("Browse Marvel Rivals character stats in a cleaner, more interactive dashboard.")

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
role_filter = st.sidebar.selectbox("Role", ["All"] + sorted(df["role"].unique().tolist()))
search_text = st.sidebar.text_input("Search character")
min_health = st.sidebar.slider("Minimum health", 200, 700, 200)
min_damage = st.sidebar.slider("Minimum damage", 1, 5, 1)

if role_filter != "All":
    df = df[df["role"] == role_filter]

if search_text.strip() != "":
    df = df[df["name"].str.contains(search_text, case=False, na=False)]

df = df[df["health"] >= min_health]
df = df[df["damage"] >= min_damage]

st.markdown("<h2 class='section-title'>Roster Overview</h2>", unsafe_allow_html=True)

metric1, metric2, metric3 = st.columns(3)

with metric1:
    st.markdown(f"""
    <div class="custom-card">
        <div class="stat-label">Characters Shown</div>
        <div class="stat-value">{len(df)}</div>
    </div>
    """, unsafe_allow_html=True)

with metric2:
    average_health = round(df["health"].mean(), 1) if not df.empty else 0
    st.markdown(f"""
    <div class="custom-card">
        <div class="stat-label">Average Health</div>
        <div class="stat-value">{average_health}</div>
    </div>
    """, unsafe_allow_html=True)

with metric3:
    average_damage = round(df["damage"].mean(), 1) if not df.empty else 0
    st.markdown(f"""
    <div class="custom-card">
        <div class="stat-label">Average Damage</div>
        <div class="stat-value">{average_damage}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
st.dataframe(df, use_container_width=True, hide_index=True)
st.markdown("</div>", unsafe_allow_html=True)

if not df.empty:
    st.markdown("<h2 class='section-title'>Character Detail Viewer</h2>", unsafe_allow_html=True)
    selected_character = st.selectbox("Choose a character", df["name"].tolist())
    character_info = df[df["name"] == selected_character].iloc[0]

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div class="custom-card">
            <div class="stat-label">Name</div>
            <div class="stat-value">{character_info['name']}</div>
            <br>
            <div class="stat-label">Role</div>
            <div class="stat-value">{character_info['role']}</div>
            <br>
            <div class="stat-label">Range Type</div>
            <div class="stat-value">{character_info['range_type']}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="custom-card">
            <div class="stat-label">Health</div>
            <div class="stat-value">{character_info['health']}</div>
            <br>
            <div class="stat-label">Mobility</div>
            <div class="stat-value">{character_info['mobility']}</div>
            <br>
            <div class="stat-label">Damage</div>
            <div class="stat-value">{character_info['damage']}</div>
            <br>
            <div class="stat-label">Difficulty</div>
            <div class="stat-value">{character_info['difficulty']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<h2 class='section-title'>Selected Character Stat Chart</h2>", unsafe_allow_html=True)
    single_chart_df = pd.DataFrame(
        {
            "Stat": ["Health", "Mobility", "Damage", "Difficulty"],
            "Value": [
                character_info["health"],
                character_info["mobility"],
                character_info["damage"],
                character_info["difficulty"]
            ]
        }
    )
    st.bar_chart(single_chart_df.set_index("Stat"))

    st.markdown("<h2 class='section-title'>Character Comparison</h2>", unsafe_allow_html=True)
    compare_col1, compare_col2 = st.columns(2)

    with compare_col1:
        compare_1 = st.selectbox("First character", df["name"].tolist(), key="compare_1")

    with compare_col2:
        compare_2 = st.selectbox("Second character", df["name"].tolist(), key="compare_2")

    comparison_rows = []
    for stat_name in ["health", "mobility", "damage", "difficulty"]:
        first_value = df[df["name"] == compare_1][stat_name].iloc[0]
        second_value = df[df["name"] == compare_2][stat_name].iloc[0]
        comparison_rows.append(
            {
                "Stat": stat_name.title(),
                compare_1: first_value,
                compare_2: second_value
            }
        )

    comparison_chart_df = pd.DataFrame(comparison_rows).set_index("Stat")

    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.bar_chart(comparison_chart_df)
    st.markdown("</div>", unsafe_allow_html=True)

    compare_table = df[df["name"].isin([compare_1, compare_2])]
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.dataframe(compare_table, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

else:
    st.warning("No characters match your current filters.")
