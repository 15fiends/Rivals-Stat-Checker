# Rivals Stat Checker

Rivals Stat Checker is a Streamlit app for exploring Marvel Rivals characters, comparing hero stats, reading character lore, building tier lists, and saving team compositions.

## Features

- Filter the roster by role, name, health, damage, mobility, and difficulty
- View character details, lore, and a stat radar chart
- Compare two characters with a radar chart
- Create, save, load, and delete tier lists
- Create, save, load, and delete team compositions
- Display local character art from the project data folders

## How To Run

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the graded app:

```bash
streamlit run dist/main.py
```

3. Optional development run:

```bash
streamlit run src/main.py
```

## How To Use

- Use the sidebar filters to narrow the character roster.
- Open the `Details` tab to read lore, see role info, and review the character radar chart.
- Open the `Comparison` tab to compare two heroes side by side.
- Open `Tier Lists` to build and save your own rankings.
- Open `Team Comps` to save six-character squads.

## File Structure

- `README.md`: project overview, instructions, and file descriptions
- `demo.mp4`: short demo video of the app
- `requirements.txt`: Python dependencies used by the project
- `src/`: development version of the project
- `src/main.py`: development entry point for the Streamlit app
- `src/data/`: development data files and character images
- `dist/`: stable production version that should be graded
- `dist/main.py`: stable entry point for the graded app
- `dist/data/`: stable copied data used by the graded app

## Repository Notes

- `src/` is the playground version where changes are developed first.
- `dist/` contains the stable version that mirrors the app the instructor should run.
- The app uses local JSON files for saved tier lists and team comps.

## Requirements Checklist

- Language: Python 3
- Libraries: Streamlit, Pandas, Plotly
- Graded run command: `streamlit run dist/main.py`

