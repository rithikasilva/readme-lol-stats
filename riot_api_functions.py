import requests


class BadRequest(Exception):
    pass

def riot_api_get(region, endpoint, headers):
    response = requests.get(f"https://{region}.api.riotgames.com/{endpoint}", headers)
    data = response.json()
    if "status" in data and data["status"]["status_code"] != 200:
        raise BadRequest(f"{data['status']['status_code']}: {data['status']['message']}")
    else:
        return data


def get_summoner_identifiers(name, api_key):
    summoner_values = riot_api_get("na1", f"lol/summoner/v4/summoners/by-name/{name}", {"api_key": api_key})
    return summoner_values["id"], summoner_values["puuid"]



def get_summoners_matches(puuid, api_key, start, count):
    matches = riot_api_get("americas", f"lol/match/v5/matches/by-puuid/{puuid}/ids", {"api_key": api_key, "start": start, "count": count})
    return matches


def get_match_data(match, api_key):
    match_data = riot_api_get("americas", f"lol/match/v5/matches/{match}", {"api_key": api_key})
    return match_data


def get_summoner_rank(id, api_key):
    rank_data = riot_api_get("na1", f"lol/league/v4/entries/by-summoner/{id}", {"api_key": api_key})
    return rank_data[0]


def get_masteries(id, api_key):
    mastery_data = riot_api_get("na1", f"lol/champion-mastery/v4/champion-masteries/by-summoner/{id}/top", {"api_key": api_key})
    parsed = []
    for champ in mastery_data:
        parsed.append({"championId": champ["championId"], "championPoints": champ["championPoints"]})
    return parsed