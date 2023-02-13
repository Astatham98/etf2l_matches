import requests
import json
import csv

import time


def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def get_matches(id, page='100', count=0):
    player_data = requests.get('https://api-v2.etf2l.org/player/{}/results/?page={}&limit=100&since=0'.format(id, page))
    if player_data.status_code == 200:
        player_json_data = player_data.json()
        return int(player_json_data['total'])
    return False
 
def search(count=100, csv_name='player_id_matches.csv'):
    with open(csv_name, 'a') as player_ids:
        player_ids = csv.writer(player_ids, skipinitialspace=True, delimiter=',', quoting=csv.QUOTE_ALL)
        for i in range(count):
            if i % 1000 == 0:
                print(f"{i} id's have been checked.")
            matches = get_matches(id=str(i))
            if matches != False:
                player_ids.writerow([i, matches])

#search(count=1000)
search(count=145345, csv_name='player_id_match_feb.csv')