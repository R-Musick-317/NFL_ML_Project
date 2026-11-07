import nflreadpy as nfl
import pandas as pd

# Define the years to pull
years = [2023, 2024, 2025] 

# ==========================================
# PART 1: POINTS (From Schedule Data)
# ==========================================
sched_df = nfl.load_schedules(years).to_pandas()

# Filter out games that haven't been played yet (where score is null)
sched_df = sched_df.dropna(subset=['home_score', 'away_score'])

# Process Home Games
home_pts = sched_df.groupby(['home_team', 'season'])[['home_score', 'away_score']].sum().reset_index()
home_pts.rename(columns={'home_team': 'team', 'home_score': 'pts_scored', 'away_score': 'pts_allowed'}, inplace=True)

# Process Away Games
away_pts = sched_df.groupby(['away_team', 'season'])[['away_score', 'home_score']].sum().reset_index()
away_pts.rename(columns={'away_team': 'team', 'away_score': 'pts_scored', 'home_score': 'pts_allowed'}, inplace=True)

# Combine and sum total points per team, per season
points_df = pd.concat([home_pts, away_pts])
points_df = points_df.groupby(['team', 'season'])[['pts_scored', 'pts_allowed']].sum().reset_index()


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

# Calculate Turnover Differential
team_stats['turnover_diff'] = team_stats['turnovers_generated'] - team_stats['turnovers_lost']

# Reorder and filter columns
team_stats = team_stats[[
    'Primary_Key', 'mapped_team', 'season', 'pts_scored', 'pts_allowed', 
    'turnovers_lost', 'turnovers_generated', 'turnover_diff'
]]

# Rename for Power BI visualization
team_stats.rename(columns={
    'mapped_team': 'Team',
    'season': 'Season',
    'pts_scored': 'Points Scored',
    'pts_allowed': 'Points Allowed',
    'turnovers_lost': 'Turnovers Lost',
    'turnovers_generated': 'Turnovers Generated',
    'turnover_diff': 'Turnover Margin'
}, inplace=True)

# Power BI will detect and import this final DataFrame automatically
nfl_powerbi_df = team_stats