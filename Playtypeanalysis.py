# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 22:07:56 2024

@author: NAWri
"""
# Importing necessary libraries
import pandas as pd

# Load data
filepath = "C:/Users/NAWri/Documents/BGA/MagicPlayType/Orlando_Magic_Playtype_data_.csv"
playsdata = pd.read_csv(filepath)
FTData = pd.read_csv("C:/Users/NAWri/Documents/BGA/MagicPlayType/FTData.csv")

# Modify FTData to match column names in playsdata
FTData = FTData.rename(columns={'Player': 'PLAYER_NAME'})

# Combine FTData into playsdata
playsdata = pd.merge(playsdata, FTData, on='PLAYER_NAME', how='left')

# Filter out 'putbacks' play type
playsdata = playsdata[playsdata['PLAY_TYPE'] != 'Putbacks']

# Creating playoutputscore for efficiency measurement
playsdata['playoutputscore'] = (playsdata['PPP'] * 100) + ((playsdata['FTA_FREQ'] * 100) * playsdata['FT%']) - (playsdata['TOV_FREQ'] * 100)

# Split the data by season
playsdata_2022_23 = playsdata[playsdata['SEASON'] == '2022-23']
playsdata_2023_24 = playsdata[playsdata['SEASON'] == '2023-24']

# Define the function to get top 3 play types for a player in a given season
def get_top_play_types(player_name, season_data, top_n=3):
    # Filter data by player
    player_data = season_data[season_data['PLAYER_NAME'] == player_name]
    
    # Check if the player data is empty
    if player_data.empty:
        return pd.DataFrame()
    
    # Sort the data by 'playoutputscore' in descending order and get top N
    top_play_types = player_data.nlargest(top_n, 'playoutputscore')
    
    # Return the relevant information
    return top_play_types[['PLAYER_NAME', 'SEASON', 'PLAY_TYPE', 'playoutputscore']]

# Get unique players
players = playsdata['PLAYER_NAME'].unique()

# Initialize empty DataFrames to store results for each season
top_play_types_2022_23_df = pd.DataFrame()
top_play_types_2023_24_df = pd.DataFrame()

# Loop through each player and populate the DataFrames for each season
for player in players:
    top_play_types_2022_23 = get_top_play_types(player, playsdata_2022_23)
    if not top_play_types_2022_23.empty:
        top_play_types_2022_23_df = pd.concat([top_play_types_2022_23_df, top_play_types_2022_23], ignore_index=True)
    
    top_play_types_2023_24 = get_top_play_types(player, playsdata_2023_24)
    if not top_play_types_2023_24.empty:
        top_play_types_2023_24_df = pd.concat([top_play_types_2023_24_df, top_play_types_2023_24], ignore_index=True)

# Function to query the DataFrame for a specific player and season
def query_top_play_types(player_name, season, data):
    result = data[(data['PLAYER_NAME'] == player_name) & (data['SEASON'] == season)]
    return result

# Example usage of the query function
player_name_query = "Franz Wagner"
season_query = "2023-24"
query_result = query_top_play_types(player_name_query, season_query, top_play_types_2023_24_df)

# Display the query result
print(f"Top play types for {player_name_query} in season {season_query}:")
print(query_result)

# Function to count frequency of play types in the top 3 plays DataFrame
def count_play_type_frequency(data):
    play_type_counts = data['PLAY_TYPE'].value_counts().head(3)  # Get top 3 play types by frequency
    return play_type_counts

# Count frequency of play types in top_play_types_2022_23_df
top_play_type_frequency_2022_23 = count_play_type_frequency(top_play_types_2022_23_df)

# Display the top 3 play types for the 2022-23 season
print("Top 3 play types for the 2022-23 season based on frequency:")
print(top_play_type_frequency_2022_23)

# Count frequency of play types in top_play_types_2023_24_df
top_play_type_frequency_2023_24 = count_play_type_frequency(top_play_types_2023_24_df)

# Display the top 3 play types for the 2023-24 season
print("Top 3 play types for the 2023-24 season based on frequency:")
print(top_play_type_frequency_2023_24)

print(top_play_types_2022_23_df)
print(top_play_types_2023_24_df)

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

# Setting file up as module usable with larger database

# play_analysis.py
import pandas as pd

def load_and_merge_data(filepath_playsdata, filepath_FTData):
    # Load data
    playsdata = pd.read_csv(filepath_playsdata)
    FTData = pd.read_csv(filepath_FTData)

    # Modify FTData to match column names in playsdata
    FTData = FTData.rename(columns={'Player':'PLAYER_NAME'})

    # Combine FTData into playsdata
    playsdata = pd.merge(playsdata, FTData, on='PLAYER_NAME', how='left')

    return playsdata

def calculate_playoutputscore(data):
    # Calculate playoutputscore
    data['playoutputscore'] = (data['PPP'] * 100) + ((data['FTA_FREQ']*100) * data['FT%']) - (data['TOV_FREQ'] * 100)
    return data

def get_top_play_types(player_name, season, data, top_n=3):
    # Filter data by player and season
    player_data = data[(data['PLAYER_NAME'] == player_name) & (data['SEASON'] == season)]
    
    # Check if the player data is empty
    if player_data.empty:
        return pd.DataFrame()
    
    # Sort the data by 'playoutputscore' in descending order and get top N
    top_play_types = player_data.nlargest(top_n, 'playoutputscore')
    
    # Return the relevant information
    return top_play_types[['PLAYER_NAME', 'SEASON', 'PLAY_TYPE', 'playoutputscore']]

def analyze_team_plays(filepath_playsdata, filepath_FTData):
    # Load and merge data
    playsdata = load_and_merge_data(filepath_playsdata, filepath_FTData)

    # Calculate playoutputscore
    playsdata = calculate_playoutputscore(playsdata)

    # Get unique players and seasons
    players = playsdata['PLAYER_NAME'].unique()
    seasons = playsdata['SEASON'].unique()

    # Initialize an empty DataFrame to store results
    top_play_types_df = pd.DataFrame()

    # Loop through each player and season to populate the DataFrame
    for player in players:
        for season in seasons:
            top_play_types = get_top_play_types(player, season, playsdata)
            if not top_play_types.empty:
                top_play_types_df = pd.concat([top_play_types_df, top_play_types], ignore_index=True)

    return top_play_types_df

def query_top_play_types(player_name, season, data):
    result = data[(data['PLAYER_NAME'] == player_name) & (data['SEASON'] == season)]
    return result

def count_play_type_frequency(data):
    play_type_counts = data['PLAY_TYPE'].value_counts().head(3)  # Get top 3 play types by frequency
    return play_type_counts
