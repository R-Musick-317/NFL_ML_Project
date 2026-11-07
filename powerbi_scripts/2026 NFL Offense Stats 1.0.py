import nflreadpy as nfl
import pandas as pd

# Set to 2026; updates automatically on Power BI refresh as games complete
years = [2026] 
df = nfl.load_player_stats(years).to_pandas()

# 2. Group by Team and Season, calculate sums, and count unique weeks played to account for byes
team_stats = df.groupby(['team', 'season']).agg(
    passing_yards=('passing_yards', 'sum'),
    rushing_yards=('rushing_yards', 'sum'),
    passing_tds=('passing_tds', 'sum'),
    rushing_tds=('rushing_tds', 'sum'),
    games_played=('week', 'nunique')
).reset_index()

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

# 5. Calculate Totals and Per Game Averages
team_stats['total_yards'] = team_stats['passing_yards'] + team_stats['rushing_yards']
team_stats['total_tds'] = team_stats['passing_tds'] + team_stats['rushing_tds']

# Per Game Averages (rounded to 1 decimal place)
team_stats['pass_yds_pg'] = (team_stats['passing_yards'] / team_stats['games_played']).round(1)
team_stats['rush_yds_pg'] = (team_stats['rushing_yards'] / team_stats['games_played']).round(1)
team_stats['total_yds_pg'] = (team_stats['total_yards'] / team_stats['games_played']).round(1)
team_stats['total_tds_pg'] = (team_stats['total_tds'] / team_stats['games_played']).round(1)

# 6. Reorder and filter columns
team_stats = team_stats[[
    'Primary_Key', 'mapped_team', 'season', 'games_played',
    'passing_yards', 'rushing_yards', 'passing_tds', 'rushing_tds', 'total_yards', 'total_tds',
    'pass_yds_pg', 'rush_yds_pg', 'total_yds_pg', 'total_tds_pg'
]]

# 7. Rename for Power BI visualization
team_stats.rename(columns={
    'mapped_team': 'Team',
    'season': 'Season',
    'games_played': 'Games Played',
    'passing_yards': 'Pass Yds',
    'rushing_yards': 'Rush Yds',
    'passing_tds': 'Pass TDs',
    'rushing_tds': 'Rush TDs',
    'total_yards': 'Total Yds',
    'total_tds': 'Total TDs',
    'pass_yds_pg': 'Pass Yds/G',
    'rush_yds_pg': 'Rush Yds/G',
    'total_yds_pg': 'Total Yds/G',
    'total_tds_pg': 'Total TDs/G'
}, inplace=True)

# Power BI will detect and import this final DataFrame automatically
nfl_powerbi_df = team_stats