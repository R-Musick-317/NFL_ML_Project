import nflreadpy as nfl
import pandas as pd

# Define the years to pull
years = [2023, 2024, 2025] 

# ==========================================
# PART 1: YARDS ALLOWED (From Player Data)
# ==========================================
# Load player data which contains passing and rushing yards
player_df = nfl.load_player_stats(years).to_pandas()

# Group offensive yardage production by the 'opponent_team' to get defensive yards allowed
yards_allowed = player_df.groupby(['opponent_team', 'season'])[['passing_yards', 'rushing_yards']].sum().reset_index()

# Calculate total yards allowed
yards_allowed['total_yards_allowed'] = yards_allowed['passing_yards'] + yards_allowed['rushing_yards']

# Rename columns to match standard naming conventions
yards_allowed.rename(columns={
    'opponent_team': 'team',
    'passing_yards': 'pass_yards_allowed',
    'rushing_yards': 'rush_yards_allowed'
}, inplace=True)


# ==========================================
# PART 2: FORMATTING & MAPPING
# ==========================================
# Stathead Translation Dictionary[cite: 2]
stathead_map = {
    'GB': 'GNB', 'KC': 'KAN', 'SF': 'SFO', 'NE': 'NWE', 
    'NO': 'NOR', 'TB': 'TAM', 'LV': 'LVR', 'LA': 'LAR'
}

# Apply the translation map[cite: 2]
yards_allowed['mapped_team'] = yards_allowed['team'].replace(stathead_map)

# Generate the Primary Key[cite: 2]
yards_allowed['Primary_Key'] = yards_allowed['mapped_team'] + "-" + yards_allowed['season'].astype(str)

# Reorder and filter columns[cite: 2]
yards_allowed = yards_allowed[[
    'Primary_Key', 'mapped_team', 'season', 'total_yards_allowed', 
    'pass_yards_allowed', 'rush_yards_allowed'
]]

# Rename for Power BI visualization[cite: 2]
yards_allowed.rename(columns={
    'mapped_team': 'Team',
    'season': 'Season',
    'total_yards_allowed': 'Total Yards Allowed',
    'pass_yards_allowed': 'Passing Yards Allowed',
    'rush_yards_allowed': 'Rushing Yards Allowed'
}, inplace=True)

# Power BI will detect and import this final DataFrame automatically[cite: 2]
nfl_powerbi_df = yards_allowed