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


def render_character_icon_row(character_names: list[str], size: int = 80) -> None:
    if not character_names:
        st.info("No characters assigned yet.")
        return

    cols_per_row = 6
    for start in range(0, len(character_names), cols_per_row):
        row_names = character_names[start:start + cols_per_row]
        cols = st.columns(cols_per_row)

        for col_index, col in enumerate(cols):
            if col_index < len(row_names):
                name = row_names[col_index]
                image_path = get_image_path(name)

                with col:
                    if os.path.exists(image_path):
                        st.image(image_path, width=size)
                    else:
                        st.write("No image")
                    st.caption(name)


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

    .tier-s {
        background: rgba(45, 180, 80, 0.18);
        padding: 12px;
        border-radius: 14px;
        margin-top: 12px;
    }

    .tier-a {
        background: rgba(123, 201, 67, 0.18);
        padding: 12px;
        border-radius: 14px;
        margin-top: 12px;
    }

    .tier-b {
        background: rgba(255, 196, 0, 0.16);
        padding: 12px;
        border-radius: 14px;
        margin-top: 12px;
    }

    .tier-c {
        background: rgba(255, 136, 0, 0.16);
        padding: 12px;
        border-radius: 14px;
        margin-top: 12px;
    }

    .tier-d {
        background: rgba(255, 74, 74, 0.16);
        padding: 12px;
        border-radius: 14px;
        margin-top: 12px;
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

character_lore = {
    "Adam Warlock": {
        "real_name": "Adam Warlock",
        "overview": "The genetically-engineered Adam Warlock wields mighty Quantum Magic, allowing him to connect and heal souls with a gentle touch. When the time comes for his allies to unite, Warlock emerges as the unwavering epicenter of cosmic justice!"
    },
    "Angela": {
        "real_name": "Aldrif Odinsdottir",
        "overview": "As the Hand of Heven, the warrior called Angela embodies unwavering courage and determination. Able to manipulate Ichors into various weapons and unfurl her wings to soar across the battlefield, she is ready to deliver divine judgment upon her foes!"
    },
    "Black Panther": {
        "real_name": "T'Challa",
        "overview": "T'Challa, King of Wakanda, wields the perfect blend of the cutting-edge Vibranium technology and ancestral power drawn from the Panther God, Bast. The Black Panther bides his time until elegantly infiltrating enemy lines and commencing his hunt."
    },
    "Black Widow": {
        "real_name": "Natasha Romanova",
        "overview": "Natasha Romanova is the world's most elite spy in any era. Her mastery of the sniper rifle eliminates targets from afar, while her shock batons neutralize close-range threats. Black Widow is locked, loaded, and ready to deliver a fatal bite!"
    },
    "Blade": {
        "real_name": "Eric Brooks",
        "overview": "Half-human and half-vampire, Eric Brooks walks between worlds, craving the very life force of his enemies. As night falls, Blade's hunt begins as he wields the Sword of Dracula to become the nightmare of any foe who dares to bare their fangs."
    },
    "Captain America": {
        "real_name": "Steven “Steve” Rogers",
        "overview": "Enhanced by the Super-Soldier Serum, Steven 'Steve' Rogers uses his Vibranium shield and extensive combat training to confront any threat to justice. When Captain America rallies his troops, a wave of courage sweeps across the battlefield!"
    },
    "Cloak & Dagger": {
        "real_name": "Tyrone Johnson and Tandy Bowen",
        "overview": "Tyrone Johnson and Tandy Bowen are nearly inseparable, like two sides of the same coin. Intertwined by forces of shadow and light, Cloak & Dagger fight as a united front, dealing havoc and healing allies across the arena."
    },
    "Daredevil": {
        "real_name": "Matt Murdock",
        "overview": "A tragic accident transformed Matt Murdock, blinding him, but awakening his incredible Radar Sense. When darkness falls, Daredevil wields his billy clubs in place of a gavel, doling out justice and purging the world of evil!"
    },
    "Deadpool": {
        "real_name": "Wade Wilson",
        "overview": "Wade Wilson is the full package, with devastating damage output, an impenetrable shield, and swift healing. There's no limit to what Deadpool can achieve, as long as he keeps his moves flashy! And, of course, every epic attack comes with an endless barrage of witty banter!"
    },
    "Doctor Strange": {
        "real_name": "Stephen Strange",
        "overview": "As the Sorcerer Supreme, Doctor Stephen Strange gracefully wields ancient spells to turn the tide of even the most impossible battle. However, magic always comes at a cost, and each use of his arcane abilities gradually awakens the darkness within him."
    },
    "Elsa Bloodstone": {
        "real_name": "Elsa Bloodstone",
        "overview": "Born into a line of legendary monster hunters, Elsa Bloodstone boasts incredible physical prowess and an innate talent for subduing the creepiest of creatures. The instinct to hunt is in her blood, and every foe she faces inevitably becomes prey ensnared in her traps!"
    },
    "Emma Frost": {
        "real_name": "Emma Frost",
        "overview": "For Emma Frost, war is the purest form of art. With her formidable telepathic abilities, she intricately weaves a deadly mental web that ensnares her foes, while her indestructible diamond form lets her lead her teammates fearlessly into the fray. Forever elegant and composed, Emma reigns as the one true queen of the battlefield!"
    },
    "Gambit": {
        "real_name": "Remy LeBeau",
        "overview": "Charming and free-spirited, Remy LeBeau manipulates kinetic energy with unmatched skill. With a flick of his wrist, his charged playing cards become explosive projectiles for foes or heal his allies through kinetic shifting. When the charismatic Gambit lights up the battlefield, he always plays to win!"
    },
    "Groot": {
        "real_name": "Groot",
        "overview": "A flora colossus from Planet X, the alien known as Groot exhibits enhanced vitality and the ability to manipulate all forms of vegetation. As sturdy as a towering tree, Groot forges his own way, serving as the team's silent but reliable pathfinder."
    },
    "Hawkeye": {
        "real_name": "Clint Barton",
        "overview": "Despite his lack of superpowers, Hawkeye's unparalleled skills as a marksman have earned him a spot alongside earth's mightiest heroes. With a cool head and steady hand, Clint Barton never misses a target… so enemies best stay out of his sights!"
    },
    "Hela": {
        "real_name": "Hela",
        "overview": "As the Goddess of Death, Hela wields supreme control over the fallen souls residing in Hel. With a haunting whisper and a murder of crows, the queen of the underworld gracefully reaps the souls of her enemies without an ounce of mercy."
    },
    "Hulk": {
        "real_name": "Bruce Banner",
        "overview": "Brilliant scientist Dr. Bruce Banner has finally found a way to coexist with his monstrous alter ego, the Hulk. By accumulating gamma energy over multiple transformations, he can become a wise and strong Hero Hulk or a fierce and destructive Monster Hulk – a true force of fury on the battlefield!"
    },
    "Human Torch": {
        "real_name": "Johnny Storm",
        "overview": "The Fantastic Four's resident heartthrob, Johnny Storm, adds an intense flare to every battle he fights. Shrouded in roaring flames, the Human Torch always manages to look cool while turning up the heat!"
    },
    "Invisible Woman": {
        "real_name": "Susan Storm",
        "overview": "The Invisible Woman is able to slip in and out of sight without a trace. No matter how intense the battle may be, Susan Richards always keeps her cool, conjuring up impenetrable force fields to protect herself and her team."
    },
    "Iron Fist": {
        "real_name": "Lin Lie",
        "overview": "Lin Lie is a master of Chinese martial arts who once wielded the shattered Sword of Fu Xi. After fusing its pieces with the mighty Chi of Shou-Lao, he is poised to strike his foes with the grace and force of a soaring dragon as the latest immortal Iron Fist."
    },
    "Iron Man": {
        "real_name": "Anthony \"Tony\" Stark",
        "overview": "Armed with superior intellect and a nanotech battlesuit of his own design, Tony Stark stands alongside gods as the Invincible Iron Man. His state of the art armor turns any battlefield into his personal playground, allowing him to steal the spotlight he so desperately desires."
    },
    "Jeff The Land Shark": {
        "real_name": "Jeff",
        "overview": "Most landsharks are vicious creatures of the deep... but not Jeff! This adorable and mischievous little landshark brings splashes of joy and healing to every battle. But if the tide turns, Jeff can morph into a voracious beast, swallowing an army of foes in one giant gulp!"
    },
    "Loki": {
        "real_name": "Loki Laufeyson",
        "overview": "What greater thrill is there for a God of Mischief than to outsmart his foes? The cunning trickster Loki uses his illusions and shapeshifting abilities to weave in and out of combat, toying with enemies at every turn."
    },
    "Luna Snow": {
        "real_name": "Seol Hee",
        "overview": "Equal parts pop star and Super Hero, Luna Snow puts on a dazzling show with both her light and dark ice powers. The arena is her stage, where Seol Hee and her team orchestrate spectacular displays that earn her an ever-increasing number of fans and wins."
    },
    "Magik": {
        "real_name": "Illyana Rasputin",
        "overview": "Trained in the dark arts and wielding her mighty Soulsword, Magik leaps through portals to navigate the arena with ease. Once Illyana transforms into the demonic Darkchild, all who dare stand against her will fall before her merciless blade."
    },
    "Magneto": {
        "real_name": "Max Eisenhardt",
        "overview": "The Master of Magnetism bends even the strongest metal to his whims, shielding his allies and striking at his foes. Whether he calls himself Max Eisenhardt, Erik Lehnsherr, or simply Magneto, the hardships this warrior has endured have made him as unbreakable as the steel he brandishes."
    },
    "Mantis": {
        "real_name": "Mantis",
        "overview": "Mantis uses her impressive mental abilities and her penchant for plant control to anchor any team she fights alongside. Her powers tap into a limitless flow of life energy, gently nourishing everything she touches."
    },
    "Mister Fantastic": {
        "real_name": "Reed Richards",
        "overview": "Reed Richards believes that true strength comes from remaining flexible, both mentally and physically. Mister Fantastic's elastic body, which can twist and stretch into any form with ease, is almost as impressive as his brilliant mind."
    },
    "Moon Knight": {
        "real_name": "Marc Spector",
        "overview": "As the avatar of the Egyptian God of Vengeance, Marc Spector's body has been enhanced by Khonshu himself. Bathed in a luminous aura that pierces the darkness, Moon Knight glides through the night, ready to sear his enemies with his master's sacred Ankhs."
    },
    "Namor": {
        "real_name": "Namor McKenzie",
        "overview": "The unrivaled King of the Seas, Namor surfs into battle on a mighty wave with an army of fierce aquatic creatures in his wake. When ancient horns of war blare, devastation soon follows as deadly waters engulf the arena."
    },
    "Peni Parker": {
        "real_name": "Peni Parker",
        "overview": "Peni Parker may be young, but she bravely stands on the frontlines to protect the Web of Life and Destiny. Together, this teen prodigy and her state-of-the-art mech, the sensational SP//dr, make for the most thrilling duo on the battlefield!"
    },
    "Phoenix": {
        "real_name": "Jean Grey",
        "overview": "Original X-Man Jean Grey boasted immense psychic power even before becoming host the unbridled Phoenix Force, embodiment of life and psionic energy across the universe. Now aligned with this ancient cosmic power, Jean and the Phoenix traverse space together, burning bright as both a spark of creation and inferno of destruction!"
    },
    "Psylocke": {
        "real_name": "Sai",
        "overview": "The psychic warrior known as Sai has the Mutant ability to conjure a variety of weapons with the power of her mind. Gracefully gliding across the battlefield, this trained ninja can shatter the enemy's defenses with a single thought."
    },
    "Rocket Raccoon": {
        "real_name": "Rocket Raccoon",
        "overview": "Rocket may not look like a tech genius or an expert tactician, but anyone who's ever made his hit list has quickly regretted underestimating him. This savvy space soldier is equally eager to boost his teammates and to collect bounties on his foes."
    },
    "Rogue": {
        "real_name": "Anna Marie",
        "overview": "Anna Marie possesses the Mutant ability to absorb the powers of others with a touch. Her ever-adaptable arsenal of superhuman abilities helps turn the tide of any fight. After touching Raw Chronovium, Rogue's strength soared to new heights, allowing her to overwhelm enemies with unstoppable force!"
    },
    "Scarlet Witch": {
        "real_name": "Wanda Maximoff",
        "overview": "Wanda Maximoff is adept at harnessing formidable chaos magic, casting hexes with the power to twist and reshape reality itself. Energy, space, and matter are mere playthings in the hands of Scarlet Witch!"
    },
    "Spider-Man": {
        "real_name": "Peter Parker",
        "overview": "Swinging around the arena on his signature weblines, your friendly neighborhood Spider-Man, AKA Peter Parker, catches his rivals by surprise with sneaky, sticky bursts of webbing and unexpected attacks from above. Look out… here comes the Spider-Man!"
    },
    "Squirrel Girl": {
        "real_name": "Doreen Green",
        "overview": "Possessing only the powers of a common squirrel, somehow Doreen Green manages to defeat seemingly invincible enemies in the most unexpected ways. Any foe who counts her out is bound to fall at the hands of the Unbeatable Squirrel Girl!"
    },
    "Star-Lord": {
        "real_name": "Peter Quill",
        "overview": "Peter Quill lives to dazzle his foes on the battlefield with his signature swagger. As his element guns paint arcs of devastation, his acrobatic moves sail through the sky with unrivaled style. With performances this spectacular, it's no wonder that Star-Lord is so legendary!"
    },
    "Storm": {
        "real_name": "Ororo Munroe",
        "overview": "An Omega-level Mutant ability to manipulate weather patterns makes Ororo Munroe a force to be reckoned with. Rain or shine, thunder or lightning, nature itself bends to the command of the Goddess of the Storm!"
    },
    "The Punisher": {
        "real_name": "Frank Castle",
        "overview": "Expertly wielding a full arsenal of futuristic weapons, Frank Castle is a formidable one-man army. With a steadfast resolve to deliver justice to his enemies, The Punisher won't cease in his mission until every last round is fired!"
    },
    "The Thing": {
        "real_name": "Ben Grimm",
        "overview": "Benjamin J. Grimm is unquestionably the rock star of any team he's on. Always at the forefront of the fight, the Thing shields his allies with his unbreakable form, selflessly fending off any harm that comes their way."
    },
    "Thor": {
        "real_name": "Thor Odinson",
        "overview": "The son of Odin taps into his divine power to call forth thunder and lightning, raining down relentless fury upon his enemies. With his mighty hammer Mjolnir in hand, Thor effortlessly asserts his dominance on the field of combat."
    },
    "Ultron": {
        "real_name": "Ultron",
        "overview": "The Pinnacle of artificial lifeforms, Ultron is programmed to learn and adapt in ways beyond human capability. He can summon an army of automated drones that obey his every command, raising his chances of victory exponentially."
    },
    "Venom": {
        "real_name": "Edward \"Eddie\" Brock",
        "overview": "Using his symbiote-enhanced body as the perfect living weapon, Eddie Brock and his alien ally stand ever-ready to unleash vicious attacks upon anyone he deems an enemy. Those ensnared by Venom's tentacles have no choice but to surrender to this insatiable predator."
    },
    "White Fox": {
        "real_name": "Ami Han",
        "overview": "Ami Han, the last of the legendary Kumiho, can summon her ancestral Nine-Tailed Power to fortify herself and heal her allies on the battlefield. As the calm and capable Director of Tiger Division, she is any team's unwavering backbone, no matter the foe."
    },
    "Winter Soldier": {
        "real_name": "James Buchanan \"Bucky\" Barnes",
        "overview": "Terrifying experiments turned him into a brainwashed assassin, but now James Buchanan 'Bucky' Barnes is in control of his own fate once again. With his enhanced mechanical arm, the Winter Soldier is primed to deliver earth-shattering blows to any foe in his path!"
    },
    "Wolverine": {
        "real_name": "Logan",
        "overview": "Thanks to his regenerative healing factor and berserker rage, the centuries-old Logan can fight through the worst pain to go claw-to-claw with any foe. The Wolverine stands ready to shred through all obstacles in his way with his Adamantium claws."
    },
}

full_df = pd.DataFrame(data)
full_df["real_name"] = full_df["name"].map(lambda name: character_lore.get(name, {}).get("real_name", "Unknown"))
full_df["overview"] = full_df["name"].map(lambda name: character_lore.get(name, {}).get("overview", "No overview added yet."))
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
    st.write("Saved tier lists and team comps now appear in their dropdowns immediately after saving.")

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

        st.markdown(f"**Real Name:** {character_info['real_name']}")
        st.write(character_info["overview"])

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
    st.write("Assign characters into S through D ranks, then save or load different tier list categories.")

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

    st.markdown("<div class='tier-s'><h3>S Rank</h3></div>", unsafe_allow_html=True)
    render_character_icon_row(current_tierlist["S"], size=72)

    st.markdown("<div class='tier-a'><h3>A Rank</h3></div>", unsafe_allow_html=True)
    render_character_icon_row(current_tierlist["A"], size=72)

    st.markdown("<div class='tier-b'><h3>B Rank</h3></div>", unsafe_allow_html=True)
    render_character_icon_row(current_tierlist["B"], size=72)

    st.markdown("<div class='tier-c'><h3>C Rank</h3></div>", unsafe_allow_html=True)
    render_character_icon_row(current_tierlist["C"], size=72)

    st.markdown("<div class='tier-d'><h3>D Rank</h3></div>", unsafe_allow_html=True)
    render_character_icon_row(current_tierlist["D"], size=72)

with tabs[4]:
    st.markdown("## Team Comps")
    st.write("Choose 6 characters, then save or load named team compositions.")

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
    render_character_icon_row([name for name in current_team if name], size=78)
