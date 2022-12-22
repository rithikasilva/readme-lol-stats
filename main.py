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


def get_loading_for_masteries(list_of_champs, folder):
    image_names = []
    for champ in list_of_champs:
        image_names.append(get_loading_image(champ, folder))
    return image_names

def get_masteries(id, api_key):
    # Gather Mastery Information
    mastery_data = requests.get(f"https://na1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{id}/top", {"api_key": api_key})
    mastery_data = mastery_data.json()
    parsed = []
    for champ in mastery_data:
        parsed.append({"championId": champ["championId"], "championPoints": champ["championPoints"]})
    return parsed



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


def get_summoner_rank(id, api_key):
    rank_data = requests.get(f"https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/{id}", {"api_key": api_key})
    rank_data = rank_data.json()
    return rank_data[0]

def create_played_and_recent_widget(config, target_file, temp_file_name, list_of_champs, dict_of_data, recent_champ_img, extra_info, num_matches, mastery_info):



     # Write the actual display content to a temporary file
    with open(temp_file_name, "w", encoding="utf-8") as f:
        f.write(f"<h2 align='center'> Data from Last {num_matches} Matches </h2>")
        f.write(f"<table align='center'><tr></tr><tr><th><pre>Top {len(list_of_champs)} Recently Played Champions\n-------------------------\n")
        for champ in list_of_champs:
            f.write(f"<img src='square_champs/{champ}.png' alt='drawing' width='20'/>" + f" {champ}".ljust(25, " ") + create_loading_bar(dict_of_data[champ]) + f"{round(dict_of_data[champ], 2): .2f}%\n".rjust(9, " "))
        f.write(f"-------------------------\n")
        

        # Based on config, populate certain data
        if "Seconds of CC" in extra_info and "Seconds of CC" in config["Extra Info"] and config["Extra Info"]["Seconds of CC"]:
            cc = extra_info["Seconds of CC"]
            f.write(f"Seconds CCing Enemies: {cc}\n")
        
        if "Rank" in extra_info and "Display Rank" in config["Extra Info"] and config["Extra Info"]["Display Rank"]:
            rank = extra_info["Rank"][0] + extra_info["Rank"][1:].lower()
            f.write(f"Current Rank: {rank} <img src='rank_images/Emblem_{rank}.png' alt='drawing' width='20'/>\n")

        if "Most Played Position" in extra_info and "Rank" in extra_info and "Main Lane" in config["Extra Info"] and config["Extra Info"]["Main Lane"]:
            position = extra_info["Most Played Position"]
            common_names = {"TOP": "Top", "JUNGLE": "Jungle", "MIDDLE": "Middle", "BOTTOM": "Bottom", "UTILITY": "Support"}
            file_names = {"TOP": "Top", "JUNGLE": "Jungle", "MIDDLE": "Mid", "BOTTOM": "Bot", "UTILITY": "Support"}
            rank = extra_info["Rank"][0] + extra_info["Rank"][1:].lower()
            if position == "ARAM":
                f.write(f"Most Played Position: {common_names[position]}\n")
            else:
                f.write(f"Most Played Position: {common_names[position]} <img src='position_images/Position_{rank}-{file_names[position]}.png' alt='drawing' width='20'/>\n")

        # Based on config, populate certain data
        if "Ability Count" in extra_info and "Ability Count" in config["Extra Info"] and config["Extra Info"]["Ability Count"]:
            count = extra_info["Ability Count"]
            f.write(f"Total Abilities Used: {count}\n")


        if "Solokills" in extra_info and "Solokills" in config["Extra Info"] and config["Extra Info"]["Solokills"]:
            solokills = extra_info["Solokills"]
            f.write(f"Total Solokills: {solokills}\n")
        
        if "Takedowns" in extra_info and "Takedowns" in config["Extra Info"] and config["Extra Info"]["Takedowns"]:
            take_downs = extra_info["Takedowns"]
            f.write(f"Total Takedowns: {take_downs}\n")
         

         
        # Most Recently Played
        f.write(f"</pre></th><th><pre>Last Played\n-----------\n<img align='center' src='loading_images/{recent_champ_img}.png' alt='drawing' width='80'/>\n</pre></th>")


        # Print Mastery
        if "Mastery" in config["Extra Info"]:
            f.write("<th><pre>")
            for champ in mastery_info:
                f.write(f"<img align='center' src='loading_images/{champ[1]}.png' alt='drawing' width='80'/> {champ[0]}: {champ[2]}\n")
        
            f.write("</pre></th>")


        f.write("</tr></table>\n")




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


    '''
    Collect all the required information, but only populate with what is configured.
    '''



    load_dotenv()
    extra_data = {}

    key = os.getenv("api-key")
    config = json.load(open("config.json"))
    name = config["Summoner Name"]

    # Get my id
    id, puuid = get_summoner_identifiers(name, key)
    rank_data = get_summoner_rank(id, key)
    extra_data["Rank"] = rank_data["tier"]


    # Get list of match ids which I was part of
    matches = get_summoners_matches(puuid, key, 0, total_matches_to_look)
    
    # Generate a list of champions that I played in the last x matches
    last_champs = []
    time_ccing = 0
    played_positions = []
    ability_usage = 0
    solo_kills = 0
    take_downs = 0
    for match in matches:
        response = get_match_data(match, key)
        for participant in response["info"]["participants"]:
            if participant["puuid"] == puuid:
                last_champs.append(participant["championName"])
                ability_usage += participant["challenges"]["abilityUses"]
                played_positions.append(participant["individualPosition"])
                time_ccing += participant["timeCCingOthers"]
                solo_kills += participant["challenges"]["soloKills"]
                take_downs += participant["challenges"]["takedowns"]


    extra_data["Takedowns"] = take_downs
    extra_data["Solokills"] = solo_kills
    extra_data["Ability Count"] = ability_usage
    extra_data["Most Played Position"] = max(set(played_positions), key=played_positions.count)
    if extra_data["Most Played Position"] == "Invalid": extra_data["Most Played Position"] = "ARAM"
    extra_data["Seconds of CC"] = time_ccing


    # Generate all the actual stats
    total_length = len(last_champs)
    counts = Counter(last_champs)
    for key_counts in counts:
        counts[key_counts] = (counts[key_counts] / total_length) * 100
    ordered = sorted(counts, key=counts.get, reverse=True)[:5]

     
    
    # Get mastery information
    champ_id_points = get_masteries(id, key)
    patch = requests.get("https://ddragon.leagueoflegends.com/api/versions.json")
    latest_version = patch.json()[0]
    response = requests.get(f"https://ddragon.leagueoflegends.com/cdn/{latest_version}/data/en_US/champion.json")
    response = response.json()
    champ_data = response["data"]
    for id in champ_id_points:
        for champ in champ_data:
            if int(champ_data[champ]["key"]) == int(id["championId"]):
                id["champName"] = champ_data[champ]["name"]
                break
    print(champ_id_points)




    list_masteries = [[x["champName"], x["championPoints"]] for x in champ_id_points][:3]
    mastery_info = [[x[0], get_loading_image(x[0], "loading_images"), x[1]] for x in list_masteries]
    print(mastery_info)
 


    # Gather the square and loading images
    get_champ_images(counts, "square_champs")
    loading_image = get_loading_image(last_champs[0], "loading_images")
    create_played_and_recent_widget(config, "README.md", "readme_lol_stats.md", ordered, counts, loading_image, extra_data, total_matches_to_look, mastery_info)
    print("Finished")



if __name__ == "__main__":
    main()