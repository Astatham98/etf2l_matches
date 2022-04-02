import pandas as pd
import requests

def get_top_100_ids():
    df = pd.read_csv('player_id_matches.csv', names=['ID', 'Matches played'])
    df = df.sort_values(by=['Matches played'], ascending=False)

    top_100 = df.head(100)
    top_100_id = top_100['ID'].tolist()
    
    return top_100_id, top_100

def get_country(ids):
    countries = []
    for id in ids:
        player = requests.get('https://api.etf2l.org/player/{}.json?per_page=100&since=0'.format(id))
        countries.append(player.json()['player']['country'])
    return countries

def get_name(ids):
    names = []
    for id in ids:
        player = requests.get('https://api.etf2l.org/player/{}.json?per_page=100&since=0'.format(id))
        names.append(player.json()['player']['name'])
    return names

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

def get_all_games(ids):
    HL = []
    sixes = []
    defaults = []
    for id in ids:
        HLgames, sixesgames, default = get_games(id)
        HL.append(HLgames)
        sixes.append(sixesgames)
        defaults.append(default)
    return HL, sixes, defaults

def new_df():
    ids, df = get_top_100_ids()
    HL, sixes, defaults = get_all_games(ids)
    country = get_country(ids)
    name = get_name(ids)
    
    df["Name"] = name
    df['Highlander games'] = HL
    df["6's games"] = sixes
    df["Defaults"] = defaults
    df["Country"] = country
    print(df.head(10))
    df.to_csv('player_stats.csv', index=False)

new_df()
        
