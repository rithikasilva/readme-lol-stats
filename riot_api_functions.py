import requests



def get_summoner_identifiers(name, api_key):
    summoner_values = requests.get(f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}", {"api_key": api_key})
    data = summoner_values.json()
    return data["id"], data["puuid"]



def get_summoners_matches(puuid, api_key, start, count):
    matches = requests.get(f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids", {"api_key": api_key, "start": start, "count": count})
    return matches.json()


def get_match_data(match, api_key):
    match_data = requests.get(f"https://americas.api.riotgames.com/lol/match/v5/matches/{match}", {"api_key": api_key})
    return match_data.json()


def get_summoner_rank(id, api_key):
    rank_data = requests.get(f"https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/{id}", {"api_key": api_key})
    rank_data = rank_data.json()
    return rank_data[0]


def get_masteries(id, api_key):
    # Gather Mastery Information
    mastery_data = requests.get(f"https://na1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{id}/top", {"api_key": api_key})
    mastery_data = mastery_data.json()
    parsed = []
    for champ in mastery_data:
        parsed.append({"championId": champ["championId"], "championPoints": champ["championPoints"]})
    return parsed