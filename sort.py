import pandas as pd
import requests
import time
import datetime

def get_top_100_ids(amount=100):
    df = pd.read_csv('player_id_matches.csv', names=['ID', 'Matches played'])
    df = df.sort_values(by=['Matches played'], ascending=False)

    if amount > 0:
        top_100 = df.head(amount)
    top_100_id = top_100['ID'].tolist()
    
    return top_100_id, top_100

def get_country_and_name(ids):
    countries = []
    names = []
    days_since_joining = []
    for id in ids:
        if id % 100 == 0:
            print("1000 id's names and countries gathered")
        player = requests.get('https://api.etf2l.org/player/{}.json?per_page=100&since=0'.format(id))
        countries.append(player.json()['player']['country'])
        names.append(player.json()['player']['name'])
        days_since_joining.append(get_date_joined(player))
    return countries, names, days_since_joining

def get_date_joined(player):
    date_joined = player.json()['player']['registered']
    difference = int(time.time()) - int(date_joined)
    days = datetime.timedelta(seconds=difference)
    return str(days.days)

def get_games(id, page='1', HLcount=0, sixescount=0, defaults=0):
    player_data = requests.get('https://api.etf2l.org/player/{}/results/{}.json?per_page=100&since=0'.format(id, page))
    if player_data.status_code == 200:
        results = player_data.json()['results']
        if player_data.json()['page'].get('next_page_url', None) == None:
            for result in results:
                category = result['competition']['category']
                if "6v6" in category: sixescount += 1
                elif "Highlander" in category: HLcount += 1
                if result['defaultwin'] == 1: defaults += 1
            return HLcount, sixescount, defaults
        else:
            for result in results:
                category = result['competition']['category']
                if "6v6" in category: sixescount += 1
                elif "Highlander" in category: HLcount += 1
            return get_games(id, page=str(player_data.json()['page']['page'] + 1), HLcount=HLcount, sixescount=sixescount, defaults=defaults)

def get_points(id, page='1', points=0):
    player_data = requests.get('https://api.etf2l.org/player/{}/results/{}.json?per_page=100&since=0'.format(id, page))
    if player_data.status_code == 200:
        results = player_data.json()['results']
        if player_data.json()['page'].get('next_page_url', None) == None:
            for result in results:
                clan1 = result['clan1']['was_in_team']
                if clan1: points += result['r1']
                else: points += result['r2']
            return points
        else: 
            for result in results:
                clan1 = result['clan1']['was_in_team']
                if clan1: points += result['r1']
                else: points += result['r2']
            return get_points(id, page=str(player_data.json()['page']['page'] + 1), points=points)

def get_all_games(ids):
    HL = []
    sixes = []
    defaults = []
    for id in ids:
        if id % 1000 == 0:
            print("1000 id's checked for games")
        HLgames, sixesgames, default = get_games(id)
        HL.append(HLgames)
        sixes.append(sixesgames)
        defaults.append(default)
    return HL, sixes, defaults

def edit_csv():
    #Editable to add any data needed
    df = pd.read_csv('player_stats_full.csv')
    ids = df['ID'].tolist() 

    points = []
    for i, id in enumerate(ids):
        if i % 100 == 0:
            print(f"{i} id's covered")
        points.append(get_points(id))

    df['Points'] = points
    df.to_csv('player_stats_full.csv', index=False)

def new_df(filename='', amount=100):
    ids, df = get_top_100_ids(amount=amount)
    HL, sixes, defaults = get_all_games(ids)
    country, name, joined = get_country_and_name(ids)
    
    df["Name"] = name
    df['Highlander games'] = HL
    df["6's games"] = sixes
    df["Defaults"] = defaults
    df["Country"] = country
    df["Joined"] = joined
    print(df.head(10))
    df.to_csv(filename, index=False)

new_df(filename='player_stats_full.csv', amount=34167)
#edit_csv()
