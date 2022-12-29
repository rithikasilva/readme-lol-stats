import requests


class BadRequest(Exception):
    pass


'''
A function to get data from specfieid endpoints in the Riot API.

Parameters:
- region -- region to collect data from.
- endpoint -- URI endpoint which contains data to be requested.
- headers -- get request headers

Returns:
- data - collected data as parsed json.
'''
def riot_api_get(region, endpoint, headers):
    response = requests.get(f"https://{region}.api.riotgames.com/{endpoint}", headers)
    data = response.json()
    if "status" in data and data["status"]["status_code"] != 200:
        raise BadRequest(f"{data['status']['status_code']}: {data['status']['message']}")
    else:
        return data


'''
Given a summoners name, gathers their internal id and puuid.

Parameters:
- name -- summoner name of the player to request data about.
- api_key -- Riot API key with general access.

Returns:
- id -- id of the requested summoner
- puuid -- puuid of the requested summoner
'''
def get_summoner_identifiers(name, api_key):
    summoner_values = riot_api_get("na1", f"lol/summoner/v4/summoners/by-name/{name}", {"api_key": api_key})
    return summoner_values["id"], summoner_values["puuid"]


'''
Given a summoners puuid, get a list of match_ids that the user participated in.

Paramters:
- puuid -- summoners puuid
- api_key -- Riot API key with general access.
- start -- start index
- count -- number of previous matches to gathered (0 - 100)

Returns:
- matches -- list of match ids
'''
def get_summoners_matches(puuid, api_key, start, count):
    matches = riot_api_get("americas", f"lol/match/v5/matches/by-puuid/{puuid}/ids", {"api_key": api_key, "start": start, "count": count})
    return matches



'''
Gathered match data given the id of a certain match.

Parameters:
- match_id -- valid id of a match a summoner participated in.
- api_key -- Riot API key with general access.

Returns:
- match_data -- parsed json of data collected in match.
'''
def get_match_data(match_id, api_key):
    match_data = riot_api_get("americas", f"lol/match/v5/matches/{match_id}", {"api_key": api_key})
    return match_data


'''
Gets the rank information of a given summoner using their id.

Parameters:
- id -- id of a given summoner.
- api_key -- Riot API key with general access.

Returns:
- rank_data[0] -- dictionary of rank releated information.
'''
def get_summoner_rank(id, api_key):
    rank_data = riot_api_get("na1", f"lol/league/v4/entries/by-summoner/{id}", {"api_key": api_key})
    return rank_data[0]



'''
Gets mastery points of all champions played by a summoner.

Parameters:
- id -- id of a given summoner.
- api_key -- Riot API key with general access.

Returns:
- parsed -- list of dictionaries containing the id of a champion and the requested summoners mastery of them.
'''
def get_masteries(id, api_key):
    mastery_data = riot_api_get("na1", f"lol/champion-mastery/v4/champion-masteries/by-summoner/{id}/top", {"api_key": api_key})
    parsed = []
    for champ in mastery_data:
        parsed.append({"championId": champ["championId"], "championPoints": champ["championPoints"]})
    return parsed