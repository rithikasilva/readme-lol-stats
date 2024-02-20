import requests


class RiotApiBadRequest(Exception):
    pass


'''
A function to get data from specfieid endpoints in the Riot API.

Parameters:
- region -- region to collect data from (platform code or region name)
- endpoint -- URI endpoint which contains data to be requested.
- headers -- get request headers

Returns:
- data - collected data as parsed json.
'''
def riot_api_get(region, endpoint, headers):
    response = requests.get(f"https://{region}.api.riotgames.com/{endpoint}", headers)
    data = response.json()
    if "status" in data and data["status"]["status_code"] != 200:
        message = f"Error in getting endpoint {endpoint}\nin region {region}\nwith headers {headers}\n" + \
                f"with status code {data['status']['status_code']}\nwith message{data['status']['message']}"
        raise RiotApiBadRequest("Riot API Functions Error:\n" + message)
    else:
        return data


'''
Given a summoners name, gathers their internal id and puuid.

Parameters:
- region -- region to look for summoner (platform code)
- name -- summoner name of the player to request data about.
- api_key -- Riot API key with general access.

Returns:
- id -- id of the requested summoner
- puuid -- puuid of the requested summoner
'''
def get_summoner_identifiers(region, name, api_key):
    summoner_values = riot_api_get(region, f"lol/summoner/v4/summoners/by-name/{name}", {"api_key": api_key})
    return summoner_values["id"], summoner_values["puuid"]


'''
Given a summoners puuid, get a list of match_ids that the user participated in.

Paramters:
- region -- region where the matches took place (region name)
- puuid -- summoners puuid
- api_key -- Riot API key with general access.
- start -- start index
- count -- number of previous matches to gathered (0 - 100)

Returns:
- matches -- list of match ids
'''
def get_summoners_matches(region, puuid, api_key, start, count):
    matches = riot_api_get(region, f"lol/match/v5/matches/by-puuid/{puuid}/ids", {"api_key": api_key, "start": start, "count": count})
    return matches



'''
Gathered match data given the id of a certain match.

Parameters:
- region -- region where the match took place (region name)
- match_id -- valid id of a match a summoner participated in.
- api_key -- Riot API key with general access.

Returns:
- match_data -- parsed json of data collected in match.
'''
def get_match_data(region, match_id, api_key):
    match_data = riot_api_get(region, f"lol/match/v5/matches/{match_id}", {"api_key": api_key})
    return match_data


'''
Gets the rank information of a given summoner using their id.

Parameters:
- region -- region of the summoner (platform code)
- id -- id of a given summoner.
- api_key -- Riot API key with general access.

Returns:
- rank_data[0] -- dictionary of rank releated information.
'''
def get_summoner_rank(region, id, api_key):
    rank_data = riot_api_get(region, f"lol/league/v4/entries/by-summoner/{id}", {"api_key": api_key})
    if len(rank_data) == 0:
        return {"tier": "Unranked"}
    else:
        return rank_data[0]



'''
Gets mastery points of all champions played by a summoner.

Parameters:
- region -- region of the summoner (platform code)
- id -- id of a given summoner.
- api_key -- Riot API key with general access.

Returns:
- parsed -- list of dictionaries containing the id of a champion and the requested summoners mastery of them.
'''
def get_masteries(region, puuid, api_key):
    mastery_data = riot_api_get(region, f"lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}", {"api_key": api_key})
    parsed = []
    for champ in mastery_data:
        parsed.append({"championId": champ["championId"], "championPoints": champ["championPoints"]})
    return parsed