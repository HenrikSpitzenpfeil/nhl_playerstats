import csv
import os
import requests
from consts import team_abbreviations

def listToCsv(list : list, path: os.PathLike ):
    ''' Takes a list and stores it to the specified path in csv format.'''
    with open(path, "w", newline="") as file:
        writer = csv.writer(file)
        for element in list:
            writer.writerow([element])

def csvTolist(path: os.PathLike) -> list:
    with open(path, "r") as file:
        reader = csv.reader(file)
        return [int(row[0]) for row in reader]
    
def fetchPlayerIds(season_id: int) -> list:
    ''' Get all listed players for the specified season from the NHL API.
    season_id needs to be formatted like 20232024 for 2023-2024 season.'''
    all_player_ids = set()

    for team_abbr in team_abbreviations:
        url = f'https://api-web.nhle.com/v1/roster/{team_abbr}/{season_id}'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            roster = data.get('forwards', [])
            roster = roster + data.get('defensemen', [])
            for player in roster:
                player_id = player.get('id')
                if player_id:
                    all_player_ids.add(player_id)
        else:
            print(f"Failed to fetch roster for team {team_abbr}. Status Code: {response.status_code}")

    print(f"Total number of unique players: {len(all_player_ids)}")
    return list(all_player_ids)

def skater_season_stats(stat_type: str, player_id: int, season_id: int) -> str:
    '''stat_type needs to be one of 'summary', 'goalsForAgainst', 'realtime', 'penalties', 'shottype'
       season_id needs to be formatted like 20232024 for 2023-2024 season'''
    
    stat_types = ['summary', 'goalsForAgainst', 'realtime', 'penalties', 'shottype']
    if stat_type in stat_types:
      url = f'https://api.nhle.com/stats/rest/en/skater/{stat_type}?cayenneExp=playerId={player_id}%20and%20seasonId={season_id}'
      responnse = requests.get(url)
      return responnse.json()
    else:
       raise ValueError(f'stat_type needs to be one of {str(stat_types)}')
    
def get_team_stats(stat_type: str, season):
    '''Fetch the stats of a given type for all teams in the given season'''

    stat_types = ['summary', 'penalties', 'realtime', 'shottype']
    if stat_type not in stat_types:
        raise ValueError(f"Invalid stat type. Must be one of {stat_types}")
    
    url = f"https://api.nhle.com/stats/rest/en/team/{stat_type}"
    payload  = {"cayenneExp": f"gameTypeId=2 and seasonId<={season} and seasonId>={season}"}
    response = requests.get(url, params=payload)
    return response.json()['data']