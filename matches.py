import requests
import json
import csv


def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


def get_matches(id, page='1', count=0):
    player_data = requests.get('https://api.etf2l.org/player/{}/results/{}.json?per_page=100&since=0'.format(id, page))
    if player_data.status_code == 200:
        if player_data.json()['results'] is not None:
            if player_data.json()['page'].get('next_page_url', None) == None:
                return count + len(player_data.json()['results'])
            else:
                count += len(player_data.json()['results'])
                return get_matches(id, page=str(player_data.json()['page']['page'] + 1), count=count)
    return False
    
 
def search(count=100):
    with open('player_id_matches.csv', 'a') as player_ids:
        player_ids = csv.writer(player_ids, delimiter=',', quoting=csv.QUOTE_ALL)
        for i in range(count):
            if i % 1000 == 0:
                print(f"{i} id's have been checked.")
            matches = get_matches(str(i))
            if matches != False:
                player_ids.writerow([i, matches])

search(count=143520)