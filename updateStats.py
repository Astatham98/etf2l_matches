import pandas as pd
import requests
from matches import *
from sort import *


def get_ids_to_update(to_update='player_stats_1000.csv'):
# Read the CSV file
    df = pd.read_csv(to_update)

    id_column = 'ID'

    # Find the largest ID
    largest_id = df[id_column].max()

    # Save the largest ID to a text file
    with open('largest_id.txt', 'w') as f:
        f.write(str(largest_id))

    # Keep all other IDs in a list
    other_ids = df[id_column].tolist()

    to_update_ids = []
    for id in other_ids:
        matches_played = df[df['ID'] == id].get('Matches played')
        old_matches_played = get_matches_v1(id)
        if old_matches_played != matches_played.all():
            to_update_ids.append(id)


    newdf = df[df['ID'].isin(to_update_ids)]
    newdf = newdf[['ID', 'Matches played']]

    # If you want to reset the index of the new DataFrame
    newdf = newdf.reset_index(drop=True)
    newdf.to_csv('top_1k_to_update.csv', header=None, index=False)


if __name__ == '__main__':
    get_ids_to_update()
    new_df('top_1k_to_update.csv', 'top_1k_to_update_all.csv', 1000)

