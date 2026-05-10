import os
import base64
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Rivals Stat Checker", layout="wide")

APP_PATH = os.path.dirname(os.path.abspath(__file__))


def get_image_path(filename):
    return os.path.join(APP_PATH, "data", "images", filename)


def get_image_filename(character_name):
    return (
        character_name.lower()
        .replace("-", "")
        .replace(" ", "_")
        .replace("&", "and")
        .replace("__", "_")
        + ".png"
    )


def get_image_data_uri(image_path):
    if not os.path.exists(image_path):
        return None
    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
    return f"data:image/png;base64,{encoded}"


st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;800&family=Rajdhani:wght@400;600;700&display=swap" rel="stylesheet">

<style>
    .stApp {
        background:
            radial-gradient(circle at top left, rgba(0, 212, 255, 0.16), transparent 30%),
            radial-gradient(circle at top right, rgba(255, 70, 70, 0.16), transparent 30%),
            linear-gradient(135deg, #060b14 0%, #0c1524 45%, #152235 100%);
        color: #f4f7fb;
        font-family: 'Rajdhani', sans-serif;
    }

    h1, h2, h3 {
        font-family: 'Orbitron', sans-serif !important;
        letter-spacing: 1px;
        color: #ffffff;
    }

    .hero-box {
        background: linear-gradient(135deg, rgba(12, 22, 38, 0.96), rgba(23, 37, 60, 0.94));
        border: 1px solid rgba(0, 212, 255, 0.28);
        border-left: 5px solid #ff4a4a;
        border-radius: 22px;
        padding: 26px;
        margin-bottom: 18px;
        box-shadow: 0 0 30px rgba(0, 0, 0, 0.28);
    }

    .checker-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 36px;
        font-weight: 800;
        color: #ffffff;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 10px;
    }

    .hero-subtitle {
        color: #d0dceb;
        font-size: 18px;
        line-height: 1.4;
        margin-top: 12px;
    }

    .custom-card {
        background: linear-gradient(180deg, rgba(24, 35, 54, 0.98), rgba(16, 25, 39, 0.98));
        border: 1px solid rgba(120, 145, 180, 0.20);
        border-radius: 16px;
        padding: 18px;
        margin-bottom: 16px;
        box-shadow: 0 10px 24px rgba(0, 0, 0, 0.22);
    }

    .metric-card {
        background: linear-gradient(135deg, rgba(19, 30, 48, 0.98), rgba(29, 47, 73, 0.98));
        border: 1px solid rgba(0, 212, 255, 0.18);
        border-top: 3px solid #00d4ff;
        border-radius: 16px;
        padding: 18px;
        box-shadow: 0 8px 18px rgba(0, 0, 0, 0.22);
    }

    .stat-label {
        color: #9cb3cd;
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
        background: rgba(255, 74, 74, 0.16);
        color: #ff9a9a;
        border: 1px solid rgba(255, 74, 74, 0.45);
    }

    .vanguard {
        background: rgba(0, 212, 255, 0.14);
        color: #87ebff;
        border: 1px solid rgba(0, 212, 255, 0.42);
    }

    .strategist {
        background: rgba(255, 191, 71, 0.14);
        color: #ffd57b;
        border: 1px solid rgba(255, 191, 71, 0.35);
    }

    .varied {
        background: rgba(182, 107, 255, 0.14);
        color: #dfb6ff;
        border: 1px solid rgba(182, 107, 255, 0.4);
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: rgba(20, 30, 46, 0.92);
        border-radius: 12px 12px 0 0;
        padding: 10px 18px;
        color: #d9e4ef;
        font-family: 'Orbitron', sans-serif;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #ff4a4a, #00d4ff) !important;
        color: white !important;
    }

    .stSelectbox label, .stTextInput label, .stSlider label {
        color: #d8e2ee !important;
        font-weight: 700;
        letter-spacing: 0.4px;
    }

    .small-note {
        color: #a0afc2;
        font-size: 15px;
    }

    .winner-box {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.18), rgba(255, 74, 74, 0.12));
        border: 1px solid rgba(0, 212, 255, 0.35);
        border-radius: 14px;
        padding: 14px;
        margin-bottom: 12px;
    }

    .profile-wrap {
        display: flex;
        align-items: center;
        gap: 16px;
        margin-bottom: 12px;
    }

    .profile-image {
        width: 110px;
        height: 110px;
        border-radius: 50%;
        object-fit: cover;
        border: 3px solid #00d4ff;
        box-shadow: 0 0 18px rgba(0, 212, 255, 0.35);
        background-color: #111827;
    }

    .profile-name {
        font-family: 'Orbitron', sans-serif;
        font-size: 28px;
        font-weight: 700;
        color: white;
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

logo_path = get_image_path("marvel_rivals_logo.png")

st.markdown("<div class='hero-box'>", unsafe_allow_html=True)

if os.path.exists(logo_path):
    logo_col1, logo_col2 = st.columns([1.2, 1])
    with logo_col1:
        st.image(logo_path, use_container_width=True)
    with logo_col2:
        st.markdown("<div class='checker-title'>Stat Checker</div>", unsafe_allow_html=True)
        st.markdown(
            "<div class='hero-subtitle'>Explore the roster, compare combat stats, and break down character strengths with a game-inspired dashboard.</div>",
            unsafe_allow_html=True
        )
else:
    st.markdown("<div class='checker-title'>Marvel Rivals Stat Checker</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='hero-subtitle'>Explore the roster, compare combat stats, and break down character strengths with a game-inspired dashboard.</div>",
        unsafe_allow_html=True
    )

st.markdown("</div>", unsafe_allow_html=True)

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
        selected_character = st.selectbox("Search or choose a character", detail_options)
        character_info = filtered_df[filtered_df["name"] == selected_character].iloc[0]
        role_class = character_info["role"].lower().replace(" ", "-")

        image_filename = get_image_filename(character_info["name"])
        image_path = get_image_path(image_filename)
        image_data_uri = get_image_data_uri(image_path)

        if image_data_uri:
            st.markdown(
                f"""
                <div class="profile-wrap">
                    <img src="{image_data_uri}" class="profile-image">
                    <div class="profile-name">{character_info['name']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.subheader(character_info["name"])

        c1, c2 = st.columns([1, 1])

        with c1:
            st.markdown(f"""
            <div class="custom-card">
                <div class="stat-label">Role</div>
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

    image_1 = get_image_data_uri(get_image_path(get_image_filename(compare_1)))
    image_2 = get_image_data_uri(get_image_path(get_image_filename(compare_2)))

    img_col1, img_col2 = st.columns(2)

    with img_col1:
        if image_1:
            st.markdown(
                f"""
                <div class="profile-wrap">
                    <img src="{image_1}" class="profile-image">
                    <div class="profile-name">{compare_1}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.subheader(compare_1)

    with img_col2:
        if image_2:
            st.markdown(
                f"""
                <div class="profile-wrap">
                    <img src="{image_2}" class="profile-image">
                    <div class="profile-name">{compare_2}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.subheader(compare_2)

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

        winner_rows.append({"Stat": stat_name.title(), "Winner": winner})

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
