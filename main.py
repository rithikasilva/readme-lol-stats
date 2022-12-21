import requests
from dotenv import load_dotenv
import os
import json
from collections import Counter

# Since we are using a personal key, we have a rate limit of 100 requests/2 minutes
sleep_time = 0

# Gets square impage
def get_champ_images(list_of_champs, folder):
    # Get the latest patch
    version = requests.get("https://ddragon.leagueoflegends.com/api/versions.json")
    latest_version = version.json()[0]
    # Get images of each champion
    for champ in list_of_champs:
        champ_image = requests.get(f"https://ddragon.leagueoflegends.com/cdn/{latest_version}/img/champion/{champ}.png")
        open(f"{folder}/{champ}.png", "wb").write(champ_image.content)


# Gets the loading screen image of a champion and saves to folder
def get_loading_image(champ_name, folder):
    config = json.load(open("config.json"))
    skin_num = 0
    if champ_name in config["Skin Substitutions"]:
        version = requests.get("https://ddragon.leagueoflegends.com/api/versions.json")
        latest_version = version.json()[0]
        # Get the specific skin
        champion_data = requests.get(f"https://ddragon.leagueoflegends.com/cdn/{latest_version}/data/en_US/champion/{champ_name}.json")
        data = champion_data.json()
        for skin in data["data"][champ_name]["skins"]:
            if skin["name"].lower() == config["Skin Substitutions"][champ_name].lower():
                skin_num = skin["num"]
    # Get most played champ image
    loading_image = requests.get(f"https://ddragon.leagueoflegends.com/cdn/img/champion/loading/{champ_name}_{skin_num}.jpg")
    open(f"{folder}/{champ_name}_{skin_num}.png", "wb").write(loading_image.content)
    return f"{champ_name}_{skin_num}"



# Given a percentage, generates a string to display a loading bar percentage
def create_loading_bar(percentage):
    bars = int((percentage / 100) * 25)
    out = "|"
    for x in range(25):
        if x <= bars:
            out = out + "█"
        else:
            out = out + "-"
    out = out + "|"
    return out


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


def create_played_and_recent_widget(target_file, temp_file_name, list_of_champs, dict_of_data, recent_champ_img, time_ccing, num_matches):
     # Write the actual display content to a temporary file
    with open(temp_file_name, "w", encoding="utf-8") as f:
        f.write(f"<h2 align='center'> Data from Last {num_matches} Matches </h2>")
        f.write(f"<table align='center'><tr></tr><tr><th><pre>Top {len(list_of_champs)} Played Champions\n-------------------------\n")
        for champ in list_of_champs:
            f.write(f"<img src='square_champs/{champ}.png' alt='drawing' width='20'/>" + f" {champ}".ljust(25, " ") + create_loading_bar(dict_of_data[champ]) + f"{round(dict_of_data[champ], 2): .2f}%\n".rjust(9, " "))
        f.write(f"\n")
        f.write(f"<h4> Seconds CCing Enemies: {time_ccing} </h4>\n")
        f.write(f"</pre></th><th><pre>Last Played\n-----------\n<img align='center' src='loading_images/{recent_champ_img}.png' alt='drawing' width='80'/>\n</pre></th></tr></table>\n")
 

    # Open the the actual destination
    final_file_lines = open(target_file, encoding='utf-8').readlines()
    readme_lol_stats_file = open(temp_file_name, encoding='utf-8').readlines()

    # Parse target file to see where to put widget
    final_output = []
    start_pos = 0
    end_pos = 0
    for pos, line in enumerate(final_file_lines):
        if line == "<!---LOL-STATS-START-HERE--->\n":
            start_pos = pos
        elif line == "<!---LOL-STATS-END-HERE--->\n":
            end_pos = pos

    # Format everything
    start = final_file_lines[:start_pos+1]
    end = final_file_lines[end_pos:]
    start.extend(readme_lol_stats_file)
    start.extend(end)
    final_output = start
    
    # Write to target file
    with open(target_file, "w", encoding="utf-8") as f:
        for line in final_output:
            f.write(line)

    os.remove(temp_file_name)


def main():


    total_matches_to_look = 20

    load_dotenv()
    key = os.getenv("api-key")
    name = json.load(open("config.json"))["Summoner Name"]

    # Get my id
    id, puuid = get_summoner_identifiers(name, key)

    # Get list of match ids which I was part of
    matches = get_summoners_matches(puuid, key, 0, total_matches_to_look)
    
    # Generate a list of champions that I played in the last x matches
    last_champs = []
    time_ccing = 0
    for match in matches:
        response = get_match_data(match, key)
        for participant in response["info"]["participants"]:
            if participant["puuid"] == puuid:
                last_champs.append(participant["championName"])
                time_ccing += participant["timeCCingOthers"]


    # Generate all the actual stats
    total_length = len(last_champs)
    counts = Counter(last_champs)
    for key in counts:
        counts[key] = (counts[key] / total_length) * 100
    ordered = sorted(counts, key=counts.get, reverse=True)[:5]

     
    
    # Gather the square and loading images
    get_champ_images(counts, "square_champs")
    loading_image = get_loading_image(last_champs[0], "loading_images")
    create_played_and_recent_widget("README.md", "readme_lol_stats.md", ordered, counts, loading_image, time_ccing, total_matches_to_look)
    print("Finished")



if __name__ == "__main__":
    main()