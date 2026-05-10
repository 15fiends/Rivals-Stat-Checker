import streamlit as st
import pandas as pd

st.set_page_config(page_title="Rivals Stat Checker", layout="wide")

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;800&family=Rajdhani:wght@400;600;700&display=swap" rel="stylesheet">

<style>
    .stApp {
        background:
            radial-gradient(circle at top left, rgba(0, 183, 255, 0.18), transparent 28%),
            radial-gradient(circle at top right, rgba(255, 59, 59, 0.18), transparent 30%),
            linear-gradient(135deg, #070b14 0%, #0f1726 45%, #131c2f 100%);
        color: #f4f7fb;
        font-family: 'Rajdhani', sans-serif;
    }

    h1, h2, h3 {
        font-family: 'Orbitron', sans-serif !important;
        letter-spacing: 1px;
        color: #ffffff;
    }

    .hero-box {
        background: linear-gradient(135deg, rgba(14, 26, 45, 0.95), rgba(26, 36, 58, 0.92));
        border: 1px solid rgba(0, 224, 255, 0.25);
        border-left: 5px solid #ff4b4b;
        border-radius: 18px;
        padding: 24px;
        margin-bottom: 18px;
        box-shadow: 0 0 25px rgba(0, 0, 0, 0.28);
    }

    .hero-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 40px;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 8px;
        text-transform: uppercase;
    }

    .hero-subtitle {
        color: #c7d3e2;
        font-size: 18px;
        line-height: 1.4;
    }

    .custom-card {
        background: linear-gradient(180deg, rgba(26, 34, 52, 0.98), rgba(18, 26, 40, 0.98));
        border: 1px solid rgba(110, 133, 164, 0.22);
        border-radius: 16px;
        padding: 18px;
        margin-bottom: 16px;
        box-shadow: 0 10px 24px rgba(0, 0, 0, 0.22);
    }

    .metric-card {
        background: linear-gradient(135deg, rgba(18, 28, 45, 0.98), rgba(26, 43, 66, 0.98));
        border: 1px solid rgba(0, 224, 255, 0.18);
        border-top: 3px solid #00e0ff;
        border-radius: 16px;
        padding: 18px;
        box-shadow: 0 8px 18px rgba(0, 0, 0, 0.22);
    }

    .stat-label {
        color: #8fa8c4;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .stat-value {
        color: #ffffff;
        font-size: 28px;
        font-weight: 700;
        margin-top: 4px;
    }

    .section-title {
        color: #ffffff;
        font-family: 'Orbitron', sans-serif;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 8px;
        margin-bottom: 10px;
    }

    .role-pill {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 999px;
        font-weight: 700;
        font-size: 13px;
        letter-spacing: 0.5px;
        margin-top: 6px;
    }

    .duelist {
        background: rgba(255, 75, 75, 0.16);
        color: #ff8f8f;
        border: 1px solid rgba(255, 75, 75, 0.45);
    }

    .vanguard {
        background: rgba(0, 224, 255, 0.14);
        color: #7deaff;
        border: 1px solid rgba(0, 224, 255, 0.4);
    }

    .strategist {
        background: rgba(255, 196, 0, 0.14);
        color: #ffd85e;
        border: 1px solid rgba(255, 196, 0, 0.35);
    }

    .varied {
        background: rgba(186, 104, 200, 0.14);
        color: #e1b7ff;
        border: 1px solid rgba(186, 104, 200, 0.4);
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: rgba(22, 31, 48, 0.9);
        border-radius: 12px 12px 0 0;
        padding: 10px 18px;
        color: #d9e4ef;
        font-family: 'Orbitron', sans-serif;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #ff4b4b, #00d8ff) !important;
        color: white !important;
    }

    .stSelectbox label, .stTextInput label, .stSlider label {
        color: #d8e2ee !important;
        font-weight: 700;
        letter-spacing: 0.4px;
    }

    .small-note {
        color: #98a8bc;
        font-size: 15px;
    }

    .winner-box {
        background: linear-gradient(135deg, rgba(0, 224, 255, 0.18), rgba(255, 75, 75, 0.12));
        border: 1px solid rgba(0, 224, 255, 0.35);
        border-radius: 14px;
        padding: 14px;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)

data = [
    {"name": "Adam Warlock", "role": "Strategist", "health": 250, "mobility": 2, "damage": 3, "difficulty": 4, "range_type": "Ranged"},
    {"name": "Angela", "role": "Vanguard", "health": 550, "mobility": 4, "damage": 4, "difficulty": 3, "range_type": "Melee"},
    {"name": "Black Panther", "role": "Duelist", "health": 275, "mobility": 5, "damage": 4, "difficulty": 4, "range_type": "Melee"},
    {"name": "Black Widow", "role": "Duelist", "health": 250, "mobility": 3, "damage": 5, "difficulty": 3, "range_type": "Ranged"},
    {"name": "Blade", "role": "Duelist", "health": 350, "mobility": 4, "damage": 5, "difficulty": 4, "range_type": "Melee"},
    {"name": "Captain America", "role": "Vanguard", "health": 575, "mobility": 3, "damage": 3, "difficulty": 3, "range_type": "Melee"},
    {"name": "Cloak & Dagger", "role": "Strategist", "health": 275, "mobility": 3, "damage": 3, "difficulty": 4, "range_type": "Hybrid"},
    {"name": "Daredevil", "role": "Duelist", "health": 325, "mobility": 5, "damage": 4, "difficulty": 4, "range_type": "Melee"},
    {"name": "Deadpool", "role": "Varied", "health": 300, "mobility": 4, "damage": 4, "difficulty": 5, "range_type": "Hybrid"},
    {"name": "Doctor Strange", "role": "Vanguard", "health": 675, "mobility": 2, "damage": 3, "difficulty": 4, "range_type": "Ranged"},
    {"name": "Elsa Bloodstone", "role": "Duelist", "health": 275, "mobility": 4, "damage": 4, "difficulty": 3, "range_type": "Ranged"},
    {"name": "Emma Frost", "role": "Vanguard", "health": 650, "mobility": 2, "damage": 4, "difficulty": 4, "range_type": "Hybrid"},
    {"name": "Gambit", "role": "Strategist", "health": 275, "mobility": 3, "damage": 3, "difficulty": 4, "range_type": "Ranged"},
    {"name": "Groot", "role": "Vanguard", "health": 850, "mobility": 1, "damage": 3, "difficulty": 2, "range_type": "Melee"},
    {"name": "Hawkeye", "role": "Duelist", "health": 275, "mobility": 3, "damage": 5, "difficulty": 3, "range_type": "Ranged"},
    {"name": "Hela", "role": "Duelist", "health": 250, "mobility": 3, "damage": 5, "difficulty": 4, "range_type": "Ranged"},
    {"name": "Hulk", "role": "Vanguard", "health": 750, "mobility": 3, "damage": 4, "difficulty": 3, "range_type": "Melee"},
    {"name": "Human Torch", "role": "Duelist", "health": 250, "mobility": 5, "damage": 5, "difficulty": 4, "range_type": "Ranged"},
    {"name": "Invisible Woman", "role": "Strategist", "health": 275, "mobility": 3, "damage": 2, "difficulty": 4, "range_type": "Ranged"},
    {"name": "Iron Fist", "role": "Duelist", "health": 300, "mobility": 5, "damage": 4, "difficulty": 4, "range_type": "Melee"},
    {"name": "Iron Man", "role": "Duelist", "health": 250, "mobility": 5, "damage": 4, "difficulty": 3, "range_type": "Ranged"},
    {"name": "Jeff The Land Shark", "role": "Strategist", "health": 250, "mobility": 4, "damage": 2, "difficulty": 2, "range_type": "Ranged"},
    {"name": "Loki", "role": "Strategist", "health": 275, "mobility": 3, "damage": 3, "difficulty": 4, "range_type": "Ranged"},
    {"name": "Luna Snow", "role": "Strategist", "health": 275, "mobility": 3, "damage": 2, "difficulty": 3, "range_type": "Ranged"},
    {"name": "Magik", "role": "Duelist", "health": 250, "mobility": 5, "damage": 4, "difficulty": 4, "range_type": "Melee"},
    {"name": "Magneto", "role": "Vanguard", "health": 650, "mobility": 2, "damage": 4, "difficulty": 3, "range_type": "Mid Range"},
    {"name": "Mantis", "role": "Strategist", "health": 250, "mobility": 3, "damage": 2, "difficulty": 2, "range_type": "Ranged"},
    {"name": "Mister Fantastic", "role": "Duelist", "health": 375, "mobility": 3, "damage": 4, "difficulty": 4, "range_type": "Hybrid"},
    {"name": "Moon Knight", "role": "Duelist", "health": 275, "mobility": 4, "damage": 4, "difficulty": 3, "range_type": "Ranged"},
    {"name": "Namor", "role": "Duelist", "health": 250, "mobility": 3, "damage": 4, "difficulty": 3, "range_type": "Ranged"},
    {"name": "Peni Parker", "role": "Vanguard", "health": 650, "mobility": 2, "damage": 3, "difficulty": 3, "range_type": "Mid Range"},
    {"name": "Phoenix", "role": "Duelist", "health": 275, "mobility": 4, "damage": 5, "difficulty": 4, "range_type": "Ranged"},
    {"name": "Psylocke", "role": "Duelist", "health": 250, "mobility": 5, "damage": 4, "difficulty": 4, "range_type": "Hybrid"},
    {"name": "The Punisher", "role": "Duelist", "health": 300, "mobility": 2, "damage": 5, "difficulty": 2, "range_type": "Ranged"},
    {"name": "The Thing", "role": "Vanguard", "health": 700, "mobility": 1, "damage": 4, "difficulty": 2, "range_type": "Melee"},
    {"name": "Rocket Raccoon", "role": "Strategist", "health": 250, "mobility": 4, "damage": 2, "difficulty": 3, "range_type": "Ranged"},
    {"name": "Rogue", "role": "Vanguard", "health": 675, "mobility": 3, "damage": 4, "difficulty": 4, "range_type": "Melee"},
    {"name": "Scarlet Witch", "role": "Duelist", "health": 250, "mobility": 3, "damage": 5, "difficulty": 4, "range_type": "Mid Range"},
    {"name": "Squirrel Girl", "role": "Duelist", "health": 275, "mobility": 3, "damage": 4, "difficulty": 2, "range_type": "Ranged"},
    {"name": "Spider-Man", "role": "Duelist", "health": 250, "mobility": 5, "damage": 4, "difficulty": 5, "range_type": "Melee"},
    {"name": "Star-Lord", "role": "Duelist", "health": 250, "mobility": 5, "damage": 4, "difficulty": 3, "range_type": "Ranged"},
    {"name": "Storm", "role": "Duelist", "health": 250, "mobility": 5, "damage": 4, "difficulty": 3, "range_type": "Ranged"},
    {"name": "Thor", "role": "Vanguard", "health": 600, "mobility": 3, "damage": 4, "difficulty": 3, "range_type": "Melee"},
    {"name": "Ultron", "role": "Strategist", "health": 250, "mobility": 4, "damage": 3, "difficulty": 4, "range_type": "Ranged"},
    {"name": "Venom", "role": "Vanguard", "health": 675, "mobility": 4, "damage": 4, "difficulty": 3, "range_type": "Melee"},
    {"name": "White Fox", "role": "Strategist", "health": 275, "mobility": 3, "damage": 2, "difficulty": 3, "range_type": "Ranged"},
    {"name": "Winter Soldier", "role": "Duelist", "health": 275, "mobility": 3, "damage": 5, "difficulty": 3, "range_type": "Mid Range"},
    {"name": "Wolverine", "role": "Duelist", "health": 350, "mobility": 4, "damage": 5, "difficulty": 4, "range_type": "Melee"}
]

full_df = pd.DataFrame(data)
filtered_df = full_df.copy()

st.markdown("""
<div class="hero-box">
    <div class="hero-title">Marvel Rivals Stat Checker</div>
    <div class="hero-subtitle">
        Explore the roster, compare combat stats, and break down character strengths with a game-inspired dashboard.
    </div>
</div>
""", unsafe_allow_html=True)

st.caption("Roles and health are based on current Marvel Rivals hero data. Mobility, damage, difficulty, and range labels are app comparison ratings for browsing.")

st.sidebar.header("Filters")
role_filter = st.sidebar.selectbox("Role", ["All"] + sorted(full_df["role"].unique().tolist()))
search_text = st.sidebar.text_input("Search roster by name")
min_health = st.sidebar.slider("Minimum health", 200, 850, 200)
min_damage = st.sidebar.slider("Minimum damage", 1, 5, 1)
min_mobility = st.sidebar.slider("Minimum mobility rating", 1, 5, 1)
max_difficulty = st.sidebar.slider("Maximum difficulty rating", 1, 5, 5)

if role_filter != "All":
    filtered_df = filtered_df[filtered_df["role"] == role_filter]

if search_text.strip():
    filtered_df = filtered_df[
        filtered_df["name"].str.contains(search_text, case=False, na=False, regex=False)
    ]

filtered_df = filtered_df[filtered_df["health"] >= min_health]
filtered_df = filtered_df[filtered_df["damage"] >= min_damage]
filtered_df = filtered_df[filtered_df["mobility"] >= min_mobility]
filtered_df = filtered_df[filtered_df["difficulty"] <= max_difficulty]

tab1, tab2, tab3 = st.tabs(["Overview", "Details", "Comparison"])

with tab1:
    st.markdown("<h2 class='section-title'>Roster Overview</h2>", unsafe_allow_html=True)

    m1, m2, m3 = st.columns(3)

    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="stat-label">Characters Shown</div>
            <div class="stat-value">{len(filtered_df)}</div>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        avg_health = round(filtered_df["health"].mean(), 1) if not filtered_df.empty else 0
        st.markdown(f"""
        <div class="metric-card">
            <div class="stat-label">Average Health</div>
            <div class="stat-value">{avg_health}</div>
        </div>
        """, unsafe_allow_html=True)

    with m3:
        avg_damage = round(filtered_df["damage"].mean(), 1) if not filtered_df.empty else 0
        st.markdown(f"""
        <div class="metric-card">
            <div class="stat-label">Average Damage</div>
            <div class="stat-value">{avg_damage}</div>
        </div>
        """, unsafe_allow_html=True)

    sort_col1, sort_col2 = st.columns(2)
    with sort_col1:
        sort_stat = st.selectbox(
            "Sort roster by",
            ["name", "role", "health", "mobility", "damage", "difficulty"]
        )
    with sort_col2:
        sort_direction = st.selectbox(
            "Sort direction",
            ["Descending ↓", "Ascending ↑"]
        )

    ascending = sort_direction == "Ascending ↑"
    sorted_df = filtered_df.sort_values(by=sort_stat, ascending=ascending).reset_index(drop=True)

    st.markdown("<div class='small-note'>Use the sorting controls to quickly find the strongest characters in each stat category.</div>", unsafe_allow_html=True)

    if sorted_df.empty:
        st.warning("No characters match your current filters.")
    else:
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        st.dataframe(sorted_df, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

        role_counts = sorted_df["role"].value_counts().rename_axis("Role").reset_index(name="Count")
        st.markdown("<h2 class='section-title'>Role Distribution</h2>", unsafe_allow_html=True)
        st.bar_chart(role_counts.set_index("Role"))

with tab2:
    st.markdown("<h2 class='section-title'>Character Details</h2>", unsafe_allow_html=True)

    if filtered_df.empty:
        st.warning("No characters match your current filters.")
    else:
        detail_options = filtered_df["name"].tolist()
        selected_character = st.selectbox(
            "Search or choose a character",
            detail_options
        )
        character_info = filtered_df[filtered_df["name"] == selected_character].iloc[0]
        role_class = character_info["role"].lower().replace(" ", "-")

        c1, c2 = st.columns([1, 1])

        with c1:
            st.markdown(f"""
            <div class="custom-card">
                <div class="stat-label">Character</div>
                <div class="stat-value">{character_info['name']}</div>
                <div class="role-pill {role_class}">{character_info['role']}</div>
                <br><br>
                <div class="stat-label">Range Type</div>
                <div class="stat-value">{character_info['range_type']}</div>
            </div>
            """, unsafe_allow_html=True)

        with c2:
            st.markdown(f"""
            <div class="custom-card">
                <div class="stat-label">Health</div>
                <div class="stat-value">{character_info['health']}</div>
                <br>
                <div class="stat-label">Mobility Rating</div>
                <div class="stat-value">{character_info['mobility']}</div>
                <br>
                <div class="stat-label">Damage Rating</div>
                <div class="stat-value">{character_info['damage']}</div>
                <br>
                <div class="stat-label">Difficulty Rating</div>
                <div class="stat-value">{character_info['difficulty']}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div class='small-note'>Stat guide: Health is current roster data. Mobility, damage, and difficulty are app comparison ratings for easier browsing.</div>", unsafe_allow_html=True)

        chart_df = pd.DataFrame(
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
        st.bar_chart(chart_df.set_index("Stat"))

with tab3:
    st.markdown("<h2 class='section-title'>Side-by-Side Comparison</h2>", unsafe_allow_html=True)

    compare_col1, compare_col2 = st.columns(2)

    with compare_col1:
        compare_1 = st.selectbox("First character", full_df["name"].tolist(), key="compare_1")

    with compare_col2:
        compare_2 = st.selectbox("Second character", full_df["name"].tolist(), key="compare_2")

    first_row = full_df[full_df["name"] == compare_1].iloc[0]
    second_row = full_df[full_df["name"] == compare_2].iloc[0]

    comparison_rows = []
    winner_rows = []

    for stat_name in ["health", "mobility", "damage", "difficulty"]:
        first_value = first_row[stat_name]
        second_value = second_row[stat_name]

        comparison_rows.append(
            {
                "Stat": stat_name.title(),
                compare_1: first_value,
                compare_2: second_value
            }
        )

        if first_value > second_value:
            winner = compare_1
        elif second_value > first_value:
            winner = compare_2
        else:
            winner = "Tie"

        winner_rows.append(
            {
                "Stat": stat_name.title(),
                "Winner": winner
            }
        )

    comparison_chart_df = pd.DataFrame(comparison_rows).set_index("Stat")
    winners_df = pd.DataFrame(winner_rows)

    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.bar_chart(comparison_chart_df)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='winner-box'>", unsafe_allow_html=True)
    st.subheader("Stat Winners")
    st.dataframe(winners_df, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

    compare_table = full_df[full_df["name"].isin([compare_1, compare_2])]
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.dataframe(compare_table, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)
