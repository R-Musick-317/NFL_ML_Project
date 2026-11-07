import nflreadpy as nfl
import pandas as pd

# 1. Fetch the NFL data using the updated library
years = [2023, 2024, 2025] 
df = nfl.load_player_stats(years).to_pandas()

# 2. Group by Team and Season (Updated column to 'team')
team_stats = df.groupby(['team', 'season'])[['passing_yards', 'rushing_yards', 'passing_tds', 'rushing_tds']].sum().reset_index()

# 3. Stathead Translation Dictionary
stathead_map = {
    'GB': 'GNB', 
    'KC': 'KAN', 
    'SF': 'SFO', 
    'NE': 'NWE', 
    'NO': 'NOR', 
    'TB': 'TAM', 
    'LV': 'LVR', 
    'LA': 'LAR'
}

# Apply the translation map (Updated column to 'team')
team_stats['mapped_team'] = team_stats['team'].replace(stathead_map)

# 4. Generate the Primary Key 
team_stats['Primary_Key'] = team_stats['mapped_team'] + "-" + team_stats['season'].astype(str)

# 5. Calculate Totals
team_stats['total_yards'] = team_stats['passing_yards'] + team_stats['rushing_yards']
team_stats['total_tds'] = team_stats['passing_tds'] + team_stats['rushing_tds']

# 6. Reorder and filter columns
team_stats = team_stats[['Primary_Key', 'mapped_team', 'season', 'passing_yards', 'rushing_yards', 'passing_tds', 'rushing_tds', 'total_yards', 'total_tds']]

# 7. Rename for Power BI visualization
team_stats.rename(columns={
    'mapped_team': 'Team',
    'season': 'Season',
    'passing_yards': 'Pass Yds',
    'rushing_yards': 'Rush Yds',
    'passing_tds': 'Pass TDs',
    'rushing_tds': 'Rush TDs',
    'total_yards': 'Total Yds',
    'total_tds': 'Total TDs'
}, inplace=True)

# Power BI will detect and import this final DataFrame automatically
nfl_powerbi_df = team_stats