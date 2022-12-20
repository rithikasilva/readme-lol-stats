import requests
from dotenv import load_dotenv
import os
import json
from collections import Counter



def get_champ_images(list_of_champs, folder):
    # Get the latest patch
    response = requests.get("https://ddragon.leagueoflegends.com/api/versions.json")
    latest_version = response.json()[0]

    # Get data from the patch
    response = requests.get(f"https://ddragon.leagueoflegends.com/cdn/{latest_version}/data/en_US/champion.json")
    response = response.json()



    for champ in list_of_champs:
        response = requests.get(f"https://ddragon.leagueoflegends.com/cdn/{latest_version}/img/champion/{champ}.png")
        open(f"{folder}/{champ}.png", "wb").write(response.content)



def get_loading_image(champ_name, folder):
    config = json.load(open("config.json"))
    skin_num = 0
    if champ_name in config["Skin Substitutions"]:
        response = requests.get("https://ddragon.leagueoflegends.com/api/versions.json")
        latest_version = response.json()[0]
        # Get the specific skin
        response = requests.get(f"https://ddragon.leagueoflegends.com/cdn/{latest_version}/data/en_US/champion/{champ_name}.json")
        data = response.json()
        for skin in data["data"][champ_name]["skins"]:
            if skin["name"].lower() == config["Skin Substitutions"][champ_name].lower():
                skin_num = skin["num"]
    
    # Get most played champ image
    response = requests.get(f"https://ddragon.leagueoflegends.com/cdn/img/champion/loading/{champ_name}_{skin_num}.jpg")
    open(f"{folder}/{champ_name}_{skin_num}.png", "wb").write(response.content)

    return f"{champ_name}_{skin_num}"



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



def main():

    load_dotenv()
    key = os.getenv("api-key")
    name = json.load(open("config.json"))["Summoner Name"]


    # Get my id
    response = requests.get(f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}", {"api_key": key})
    response = response.json()
    id = response["id"]
    puuid = response["puuid"]
    print(puuid)

    # Get list of match ids which I was part of
    response = requests.get(f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids", {"api_key": key, "start": 0, "count": 20})
    response = response.json()
    matches = response
    

    last_champs = []
    for match in matches:
        response = requests.get(f"https://americas.api.riotgames.com/lol/match/v5/matches/{match}", {"api_key": key})
        response = response.json()
        for participant in response["info"]["participants"]:
            if participant["puuid"] == puuid:
                last_champs.append(participant["championName"])



    #last_champs = last_champs[:5]
    total_length = len(last_champs)
    counts = Counter(last_champs)


    for key in counts:
        counts[key] = (counts[key] / total_length) * 100




    ordered = sorted(counts, key=counts.get, reverse=True)[:5]

    print(counts)        
    



    get_champ_images(counts, "square_champs")
    loading_image = get_loading_image(ordered[0], "loading_images")



    with open("readme_lol_stats.md", "w", encoding="utf-8") as f:
        f.write("<table><tr></tr><tr><th>")
        f.write("<pre>")
        f.write("Recently Played Champions\n-------------------------\n")
        for champ in ordered:
            f.write(f"<img src='square_champs/{champ}.png' alt='drawing' width='20'/>" + f" {champ}".ljust(30, " ") + create_loading_bar(counts[champ]) + f"{round(counts[champ], 2): .2f}%\n".rjust(9, " "))
        f.write("</pre>")


        f.write("</th><th>")
        f.write("<pre>Most Played\n")
        f.write("-----------\n")
        f.write(f"<img align='center' src='loading_images/{loading_image}.png' alt='drawing' width='80'/>\n")
        f.write("</pre></th></tr></table>\n")





    # Open the the actual destination
    final_file_lines = open("README.md", encoding='utf-8').readlines()
    readme_lol_stats_file = open("readme_lol_stats.md", encoding='utf-8').readlines()




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
    

    with open("README.md", "w", encoding="utf-8") as f:
        for line in final_output:
            f.write(line)






    print("Finished")



if __name__ == "__main__":
    main()