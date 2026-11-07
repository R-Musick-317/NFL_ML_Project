import nflreadpy as nfl
import pandas as pd

# Define the years to pull
years = [2023, 2024, 2025] 

# ==========================================
# PART 1: YARDS ALLOWED (From Player Data)
# ==========================================
# Load player data which contains passing and rushing yards
player_df = nfl.load_player_stats(years).to_pandas()

# Group offensive yardage production by the 'opponent_team', and count weeks played
yards_allowed = player_df.groupby(['opponent_team', 'season']).agg(
    passing_yards=('passing_yards', 'sum'),
    rushing_yards=('rushing_yards', 'sum'),
    games_played=('week', 'nunique')
).reset_index()

# Rename opponent_team to team
yards_allowed.rename(columns={'opponent_team': 'team'}, inplace=True)

# Calculate total yards allowed and per game averages
yards_allowed['total_yards_allowed'] = yards_allowed['passing_yards'] + yards_allowed['rushing_yards']

yards_allowed['pass_yards_allowed_pg'] = (yards_allowed['passing_yards'] / yards_allowed['games_played']).round(1)
yards_allowed['rush_yards_allowed_pg'] = (yards_allowed['rushing_yards'] / yards_allowed['games_played']).round(1)
yards_allowed['total_yards_allowed_pg'] = (yards_allowed['total_yards_allowed'] / yards_allowed['games_played']).round(1)

# ==========================================
# PART 2: FORMATTING & MAPPING
# ==========================================
# Stathead Translation Dictionary
stathead_map = {
    'GB': 'GNB', 'KC': 'KAN', 'SF': 'SFO', 'NE': 'NWE', 
    'NO': 'NOR', 'TB': 'TAM', 'LV': 'LVR', 'LA': 'LAR'
}

# Apply the translation map
yards_allowed['mapped_team'] = yards_allowed['team'].replace(stathead_map)

# Generate the Primary Key
yards_allowed['Primary_Key'] = yards_allowed['mapped_team'] + "-" + yards_allowed['season'].astype(str)

# Reorder and filter columns
yards_allowed = yards_allowed[[
    'Primary_Key', 'mapped_team', 'season', 'games_played', 'total_yards_allowed', 
    'passing_yards', 'rushing_yards', 'total_yards_allowed_pg', 
    'pass_yards_allowed_pg', 'rush_yards_allowed_pg'
]]

# Rename for Power BI visualization
yards_allowed.rename(columns={
    'mapped_team': 'Team',
    'season': 'Season',
    'games_played': 'Games Played',
    'total_yards_allowed': 'Total Yards Allowed',
    'passing_yards': 'Passing Yards Allowed',
    'rushing_yards': 'Rushing Yards Allowed',
    'total_yards_allowed_pg': 'Total Yards Allowed/G',
    'pass_yards_allowed_pg': 'Passing Yards Allowed/G',
    'rush_yards_allowed_pg': 'Rushing Yards Allowed/G'
}, inplace=True)

# Power BI will detect and import this final DataFrame automatically
nfl_powerbi_df = yards_allowed