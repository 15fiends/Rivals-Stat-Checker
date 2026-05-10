import base64
import json
import os

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Rivals Stat Checker", layout="wide")

APP_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(APP_PATH, "data")
IMAGES_PATH = os.path.join(DATA_PATH, "images")
TIERLISTS_PATH = os.path.join(DATA_PATH, "tierlists.json")
TEAM_COMPS_PATH = os.path.join(DATA_PATH, "team_comps.json")


def ensure_data_files() -> None:
    os.makedirs(DATA_PATH, exist_ok=True)
    os.makedirs(IMAGES_PATH, exist_ok=True)

    if not os.path.exists(TIERLISTS_PATH):
        with open(TIERLISTS_PATH, "w", encoding="utf-8") as file:
            json.dump({}, file, indent=2)

    if not os.path.exists(TEAM_COMPS_PATH):
        with open(TEAM_COMPS_PATH, "w", encoding="utf-8") as file:
            json.dump({}, file, indent=2)


def load_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json(path: str, data: dict) -> None:
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


def get_image_filename(character_name: str) -> str:
    return (
        character_name.lower()
        .replace("-", "")
        .replace(" ", "_")
        .replace("&", "and")
        .replace("__", "_")
        + ".png"
    )


def get_image_path(character_name: str) -> str:
    return os.path.join(IMAGES_PATH, get_image_filename(character_name))


@st.cache_data(show_spinner=False)
def get_image_data_uri(image_path: str) -> str | None:
    if not os.path.exists(image_path):
        return None
    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode("utf-8")
    return f"data:image/png;base64,{encoded}"


def empty_tierlist() -> dict[str, list[str]]:
    return {"S": [], "A": [], "B": [], "C": [], "D": []}


def sanitize_tierlist(tierlist: dict) -> dict[str, list[str]]:
    clean = empty_tierlist()
    for tier in clean:
        clean[tier] = list(tierlist.get(tier, []))
    return clean


def remove_character_from_tierlist(tierlist: dict[str, list[str]], character_name: str) -> None:
    for tier in tierlist:
        if character_name in tierlist[tier]:
            tierlist[tier].remove(character_name)


def assign_character_to_tier(tierlist: dict[str, list[str]], character_name: str, tier_name: str) -> None:
    remove_character_from_tierlist(tierlist, character_name)
    tierlist[tier_name].append(character_name)


def empty_team_comp() -> list[str]:
    return ["", "", "", "", "", ""]


def sanitize_team_comp(team_comp: list[str]) -> list[str]:
    clean = empty_team_comp()
    for index in range(min(6, len(team_comp))):
        clean[index] = team_comp[index]
    return clean


def role_class(role_name: str) -> str:
    return role_name.lower().replace(" ", "-")


def show_character_header(character_name: str) -> None:
    image_uri = get_image_data_uri(get_image_path(character_name))
    if image_uri:
        st.markdown(
            f"""
            <div class="profile-wrap">
                <img src="{image_uri}" class="profile-image">
                <div class="profile-name">{character_name}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.subheader(character_name)


def render_character_icon_row(character_names: list[str], size: int = 56) -> None:
    if not character_names:
        st.info("No characters assigned yet.")
        return

    html = "<div class='icon-row'>"
    for name in character_names:
        image_uri = get_image_data_uri(get_image_path(name))
        if image_uri:
            html += f"""
            <div class="icon-card">
                <img src="{image_uri}" class="mini-icon" style="width:{size}px;height:{size}px;">
                <div class="icon-name">{name}</div>
            </div>
            """
        else:
            html += f"""
            <div class="icon-card">
                <div class="mini-icon missing-icon" style="width:{size}px;height:{size}px;">?</div>
                <div class="icon-name">{name}</div>
            </div>
            """
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


ensure_data_files()

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

    .metric-card {
        background: linear-gradient(135deg, rgba(19, 30, 48, 0.98), rgba(29, 47, 73, 0.98));
        border: 1px solid rgba(0, 212, 255, 0.18);
        border-top: 3px solid #00d4ff;
        border-radius: 16px;
        padding: 18px;
        box-shadow: 0 8px 18px rgba(0, 0, 0, 0.22);
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

    .icon-row {
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        margin-top: 10px;
        margin-bottom: 10px;
    }

    .icon-card {
        width: 84px;
        text-align: center;
    }

    .mini-icon {
        border-radius: 50%;
        object-fit: cover;
        border: 3px solid #00d4ff;
        box-shadow: 0 0 12px rgba(0, 212, 255, 0.25);
        background: #111827;
        display: block;
        margin: 0 auto 6px auto;
    }

    .missing-icon {
        display: flex;
        align-items: center;
        justify-content: center;
        color: #9fb3c8;
        font-weight: bold;
    }

    .icon-name {
        font-size: 12px;
        color: #d9e4ef;
        line-height: 1.1;
    }

    .tier-section {
        margin-bottom: 18px;
        padding: 14px;
        border-radius: 16px;
    }

    .tier-s { background: rgba(45, 180, 80, 0.18); border: 1px solid rgba(45, 180, 80, 0.45); }
    .tier-a { background: rgba(123, 201, 67, 0.18); border: 1px solid rgba(123, 201, 67, 0.45); }
    .tier-b { background: rgba(255, 196, 0, 0.16); border: 1px solid rgba(255, 196, 0, 0.38); }
    .tier-c { background: rgba(255, 136, 0, 0.16); border: 1px solid rgba(255, 136, 0, 0.38); }
    .tier-d { background: rgba(255, 74, 74, 0.16); border: 1px solid rgba(255, 74, 74, 0.38); }

    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
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
    {"name": "Wolverine", "role": "Duelist", "health": 350, "mobility": 4, "damage": 5, "difficulty": 4, "range_type": "Melee"},
]

full_df = pd.DataFrame(data)
all_character_names = full_df["name"].tolist()

if "current_tierlist_name" not in st.session_state:
    st.session_state.current_tierlist_name = "My Tier List"
if "current_tierlist_data" not in st.session_state:
    st.session_state.current_tierlist_data = empty_tierlist()
if "current_team_name" not in st.session_state:
    st.session_state.current_team_name = "My Team Comp"
if "current_team_data" not in st.session_state:
    st.session_state.current_team_data = empty_team_comp()

tierlists_store = load_json(TIERLISTS_PATH)
team_comps_store = load_json(TEAM_COMPS_PATH)

logo_path = os.path.join(IMAGES_PATH, "marvel_rivals_logo.png")

st.markdown("<div class='hero-box'>", unsafe_allow_html=True)
if os.path.exists(logo_path):
    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.image(logo_path, use_container_width=True)
    with col2:
        st.markdown("<div class='checker-title'>Stat Checker</div>", unsafe_allow_html=True)
        st.markdown("<div class='hero-subtitle'>Explore the roster, compare heroes, build tier lists, and save team comps.</div>", unsafe_allow_html=True)
else:
    st.markdown("<div class='checker-title'>Marvel Rivals Stat Checker</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

filtered_df = full_df.copy()

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

tabs = st.tabs(["Overview", "Details", "Comparison", "Tier Lists", "Team Comps"])

with tabs[0]:
    st.markdown("## How To Use")
    st.write("Use the sidebar filters to narrow the roster. Then browse characters in Details, compare two heroes in Comparison, build custom rankings in Tier Lists, and save six-character squads in Team Comps.")
    st.write("Tier lists and team comps save to local JSON files and can be loaded again later.")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"<div class='metric-card'><h3>Characters Shown</h3><h2>{len(filtered_df)}</h2></div>", unsafe_allow_html=True)
    with c2:
        avg_health = round(filtered_df["health"].mean(), 1) if not filtered_df.empty else 0
        st.markdown(f"<div class='metric-card'><h3>Average Health</h3><h2>{avg_health}</h2></div>", unsafe_allow_html=True)
    with c3:
        avg_damage = round(filtered_df["damage"].mean(), 1) if not filtered_df.empty else 0
        st.markdown(f"<div class='metric-card'><h3>Average Damage</h3><h2>{avg_damage}</h2></div>", unsafe_allow_html=True)

    if filtered_df.empty:
        st.warning("No characters match your current filters.")
    else:
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)

with tabs[1]:
    st.markdown("## Character Details")

    if filtered_df.empty:
        st.warning("No characters match your current filters.")
    else:
        selected_character = st.selectbox("Choose a character", filtered_df["name"].tolist())
        show_character_header(selected_character)

        character_info = filtered_df[filtered_df["name"] == selected_character].iloc[0]

        left_col, right_col = st.columns(2)

        with left_col:
            st.markdown(
                f"<div class='role-pill {role_class(character_info['role'])}'>{character_info['role']}</div>",
                unsafe_allow_html=True
            )
            st.write(f"Range Type: {character_info['range_type']}")
            st.write(f"Health: {character_info['health']}")

        with right_col:
            chart_df = pd.DataFrame(
                {
                    "Stat": ["Health", "Mobility", "Damage", "Difficulty"],
                    "Value": [
                        character_info["health"],
                        character_info["mobility"],
                        character_info["damage"],
                        character_info["difficulty"],
                    ],
                }
            )
            st.bar_chart(chart_df.set_index("Stat"))

with tabs[2]:
    st.markdown("## Character Comparison")

    compare_options = filtered_df["name"].tolist() if not filtered_df.empty else all_character_names
    compare_col1, compare_col2 = st.columns(2)

    with compare_col1:
        compare_1 = st.selectbox("First character", compare_options, key="compare_1")
        show_character_header(compare_1)

    with compare_col2:
        compare_2 = st.selectbox("Second character", compare_options, key="compare_2")
        show_character_header(compare_2)

    first_row = full_df[full_df["name"] == compare_1].iloc[0]
    second_row = full_df[full_df["name"] == compare_2].iloc[0]

    comparison_rows = []
    for stat_name in ["health", "mobility", "damage", "difficulty"]:
        comparison_rows.append(
            {
                "Stat": stat_name.title(),
                compare_1: first_row[stat_name],
                compare_2: second_row[stat_name],
            }
        )

    st.bar_chart(pd.DataFrame(comparison_rows).set_index("Stat"))

with tabs[3]:
    st.markdown("## Tier Lists")
    st.write("Build a tier list, save it, and load it later. Saved lists now appear in the dropdown immediately after saving.")

    tier_prefix = st.text_input(
        "Tier list title",
        value=st.session_state.current_tierlist_name.replace(" Tier List", "")
    )
    st.session_state.current_tierlist_name = f"{tier_prefix.strip() or 'My'} Tier List"

    tierlists_store = load_json(TIERLISTS_PATH)
    saved_tierlist_name = st.selectbox("Saved tier lists", ["None"] + sorted(tierlists_store.keys()))

    a1, a2, a3, a4 = st.columns(4)
    with a1:
        if st.button("New Tier List"):
            st.session_state.current_tierlist_name = "My Tier List"
            st.session_state.current_tierlist_data = empty_tierlist()
            st.rerun()
    with a2:
        if st.button("Load Tier List") and saved_tierlist_name != "None":
            st.session_state.current_tierlist_name = saved_tierlist_name
            st.session_state.current_tierlist_data = sanitize_tierlist(tierlists_store[saved_tierlist_name])
            st.rerun()
    with a3:
        if st.button("Save Tier List"):
            tierlists_store[st.session_state.current_tierlist_name] = st.session_state.current_tierlist_data
            save_json(TIERLISTS_PATH, tierlists_store)
            st.success("Tier list saved.")
            st.rerun()
    with a4:
        if st.button("Delete Tier List"):
            if st.session_state.current_tierlist_name in tierlists_store:
                tierlists_store.pop(st.session_state.current_tierlist_name)
                save_json(TIERLISTS_PATH, tierlists_store)
                st.session_state.current_tierlist_data = empty_tierlist()
                st.success("Tier list deleted.")
                st.rerun()

    current_tierlist = sanitize_tierlist(st.session_state.current_tierlist_data)

    assign_character = st.selectbox("Character to place", all_character_names, key="tier_character")
    assign_tier = st.selectbox("Rank", ["S", "A", "B", "C", "D"], key="tier_rank")

    if st.button("Assign to Tier"):
        assign_character_to_tier(current_tierlist, assign_character, assign_tier)
        st.session_state.current_tierlist_data = current_tierlist
        st.rerun()

    st.markdown("<div class='tier-section tier-s'><h3>S Rank</h3></div>", unsafe_allow_html=True)
    render_character_icon_row(current_tierlist["S"], size=58)

    st.markdown("<div class='tier-section tier-a'><h3>A Rank</h3></div>", unsafe_allow_html=True)
    render_character_icon_row(current_tierlist["A"], size=58)

    st.markdown("<div class='tier-section tier-b'><h3>B Rank</h3></div>", unsafe_allow_html=True)
    render_character_icon_row(current_tierlist["B"], size=58)

    st.markdown("<div class='tier-section tier-c'><h3>C Rank</h3></div>", unsafe_allow_html=True)
    render_character_icon_row(current_tierlist["C"], size=58)

    st.markdown("<div class='tier-section tier-d'><h3>D Rank</h3></div>", unsafe_allow_html=True)
    render_character_icon_row(current_tierlist["D"], size=58)

with tabs[4]:
    st.markdown("## Team Comps")
    st.write("Build a team of 6, save it, and load it later. Saved comps now appear in the dropdown immediately after saving.")

    team_name = st.text_input("Team comp name", value=st.session_state.current_team_name)
    st.session_state.current_team_name = team_name.strip() or "My Team Comp"

    team_comps_store = load_json(TEAM_COMPS_PATH)
    saved_comp_name = st.selectbox("Saved team comps", ["None"] + sorted(team_comps_store.keys()))

    b1, b2, b3, b4 = st.columns(4)
    with b1:
        if st.button("New Team Comp"):
            st.session_state.current_team_name = "My Team Comp"
            st.session_state.current_team_data = empty_team_comp()
            st.rerun()
    with b2:
        if st.button("Load Team Comp") and saved_comp_name != "None":
            st.session_state.current_team_name = saved_comp_name
            st.session_state.current_team_data = sanitize_team_comp(team_comps_store[saved_comp_name])
            st.rerun()
    with b3:
        if st.button("Save Team Comp"):
            team_comps_store[st.session_state.current_team_name] = st.session_state.current_team_data
            save_json(TEAM_COMPS_PATH, team_comps_store)
            st.success("Team comp saved.")
            st.rerun()
    with b4:
        if st.button("Delete Team Comp"):
            if st.session_state.current_team_name in team_comps_store:
                team_comps_store.pop(st.session_state.current_team_name)
                save_json(TEAM_COMPS_PATH, team_comps_store)
                st.session_state.current_team_data = empty_team_comp()
                st.success("Team comp deleted.")
                st.rerun()

    current_team = sanitize_team_comp(st.session_state.current_team_data)

    cols_top = st.columns(3)
    cols_bottom = st.columns(3)
    all_cols = cols_top + cols_bottom

    options = [""] + all_character_names
    for i, col in enumerate(all_cols):
        with col:
            selected = st.selectbox(
                f"Slot {i + 1}",
                options,
                index=options.index(current_team[i]) if current_team[i] in options else 0,
                key=f"slot_{i}"
            )
            current_team[i] = selected

    st.session_state.current_team_data = current_team

    st.markdown("### Current Team Preview")
    render_character_icon_row([name for name in current_team if name], size=64)
