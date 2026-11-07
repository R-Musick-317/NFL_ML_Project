import nflreadpy as nfl
import pandas as pd

# Define the years to pull
years = [2023, 2024, 2025] 

# ==========================================
# PART 1: POINTS (From Schedule Data)
# ==========================================
sched_df = nfl.load_schedules(years).to_pandas()

# Filter out games that haven't been played yet
sched_df = sched_df.dropna(subset=['home_score', 'away_score'])

# Process Home Games (Extract points and count unique games played)
home_pts = sched_df.groupby(['home_team', 'season']).agg(
    pts_scored=('home_score', 'sum'),
    pts_allowed=('away_score', 'sum'),
    games_played=('week', 'nunique')
).reset_index()
home_pts.rename(columns={'home_team': 'team'}, inplace=True)

# Process Away Games (Extract points and count unique games played)
away_pts = sched_df.groupby(['away_team', 'season']).agg(
    pts_scored=('away_score', 'sum'),
    pts_allowed=('home_score', 'sum'),
    games_played=('week', 'nunique')
).reset_index()
away_pts.rename(columns={'away_team': 'team'}, inplace=True)

# Combine and sum total points and games played per team, per season
points_df = pd.concat([home_pts, away_pts])
points_df = points_df.groupby(['team', 'season']).agg(
    pts_scored=('pts_scored', 'sum'),
    pts_allowed=('pts_allowed', 'sum'),
    games_played=('games_played', 'sum')
).reset_index()

# ==========================================
# PART 2: TURNOVERS (From Player Data)
# ==========================================
player_df = nfl.load_player_stats(years).to_pandas()

# Calculate total fumbles lost by combining all fumble types
player_df['fumbles_lost'] = (
    player_df['sack_fumbles_lost'] + 
    player_df['rushing_fumbles_lost'] + 
    player_df['receiving_fumbles_lost']
)

# Rename passing_interceptions to match the desired grouping format
player_df.rename(columns={'passing_interceptions': 'interceptions'}, inplace=True)

# Turnovers Lost (Offensive mistakes grouped by the active 'team')
to_lost = player_df.groupby(['team', 'season'])[['interceptions', 'fumbles_lost']].sum().reset_index()
to_lost['turnovers_lost'] = to_lost['interceptions'] + to_lost['fumbles_lost']
to_lost = to_lost[['team', 'season', 'turnovers_lost']]

# Turnovers Generated (Opponent mistakes grouped by 'opponent_team')
to_gen = player_df.groupby(['opponent_team', 'season'])[['interceptions', 'fumbles_lost']].sum().reset_index()
to_gen['turnovers_generated'] = to_gen['interceptions'] + to_gen['fumbles_lost']
to_gen.rename(columns={'opponent_team': 'team'}, inplace=True)
to_gen = to_gen[['team', 'season', 'turnovers_generated']]

# ==========================================
# PART 3: MERGING & FORMATTING
# ==========================================
# Merge Points and Turnovers together
team_stats = pd.merge(points_df, to_lost, on=['team', 'season'], how='inner')
team_stats = pd.merge(team_stats, to_gen, on=['team', 'season'], how='inner')

# Stathead Translation Dictionary
stathead_map = {
    'GB': 'GNB', 'KC': 'KAN', 'SF': 'SFO', 'NE': 'NWE', 
    'NO': 'NOR', 'TB': 'TAM', 'LV': 'LVR', 'LA': 'LAR'
}

# Apply the translation map
team_stats['mapped_team'] = team_stats['team'].replace(stathead_map)

# Generate the Primary Key 
team_stats['Primary_Key'] = team_stats['mapped_team'] + "-" + team_stats['season'].astype(str)

# Calculate Totals and Per Game Averages
team_stats['turnover_diff'] = team_stats['turnovers_generated'] - team_stats['turnovers_lost']

team_stats['pts_scored_pg'] = (team_stats['pts_scored'] / team_stats['games_played']).round(1)
team_stats['pts_allowed_pg'] = (team_stats['pts_allowed'] / team_stats['games_played']).round(1)
team_stats['turnovers_lost_pg'] = (team_stats['turnovers_lost'] / team_stats['games_played']).round(1)
team_stats['turnovers_generated_pg'] = (team_stats['turnovers_generated'] / team_stats['games_played']).round(1)
team_stats['turnover_diff_pg'] = (team_stats['turnover_diff'] / team_stats['games_played']).round(1)

# Reorder and filter columns
team_stats = team_stats[[
    'Primary_Key', 'mapped_team', 'season', 'games_played', 'pts_scored', 'pts_allowed', 
    'turnovers_lost', 'turnovers_generated', 'turnover_diff', 'pts_scored_pg', 
    'pts_allowed_pg', 'turnovers_lost_pg', 'turnovers_generated_pg', 'turnover_diff_pg'
]]

# Rename for Power BI visualization
team_stats.rename(columns={
    'mapped_team': 'Team',
    'season': 'Season',
    'games_played': 'Games Played',
    'pts_scored': 'Points Scored',
    'pts_allowed': 'Points Allowed',
    'turnovers_lost': 'Turnovers Lost',
    'turnovers_generated': 'Turnovers Generated',
    'turnover_diff': 'Turnover Margin',
    'pts_scored_pg': 'Points Scored/G',
    'pts_allowed_pg': 'Points Allowed/G',
    'turnovers_lost_pg': 'Turnovers Lost/G',
    'turnovers_generated_pg': 'Turnovers Generated/G',
    'turnover_diff_pg': 'Turnover Margin/G'
}, inplace=True)

# Power BI will detect and import this final DataFrame automatically
nfl_powerbi_df = team_stats