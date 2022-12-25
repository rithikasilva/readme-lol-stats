import requests
from dotenv import load_dotenv
import os
import json
from collections import Counter
import shutil
import data_dragon_functions as dd
import riot_api_functions as rf
import time




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


def create_played_and_recent_widget(config, target_file, temp_file_name, list_of_champs, dict_of_data, recent_champ_img, extra_info, num_matches, mastery_info):



     # Write the actual display content to a temporary file
    with open(temp_file_name, "w", encoding="utf-8") as f:
        f.write(f"<h2 align='center'> Data from Last {num_matches} Matches </h2>")
        f.write(f"<table align='center'><tr></tr><tr><th><pre>Top {len(list_of_champs)} Recently Played Champions\n-------------------------\n")
        for champ in list_of_champs:
            shutil.copyfile(f'square_champs/{champ}.png', f"readme-lol-items/{champ}.png")
            f.write(f"<img src='readme-lol-items/{champ}.png' alt='drawing' width='20'/>" + f" {champ}".ljust(25, " ") + create_loading_bar(dict_of_data[champ]) + f"{round(dict_of_data[champ], 2): .2f}%\n".rjust(9, " "))
        f.write(f"-------------------------\n")
        

        # Based on config, populate certain data
        if "Seconds of CC" in extra_info and "Seconds of CC" in config["Extra Info"] and config["Extra Info"]["Seconds of CC"]:
            cc = extra_info["Seconds of CC"]
            f.write(f"Seconds CCing Enemies: {cc}\n")
        
        if "Rank" in extra_info and "Display Rank" in config["Extra Info"] and config["Extra Info"]["Display Rank"]:
            rank = extra_info["Rank"][0] + extra_info["Rank"][1:].lower()
            shutil.copyfile(f'rank_images/Emblem_{rank}.png', f'readme-lol-items/Emblem_{rank}.png')
            f.write(f"Current Rank: {rank} <img src='rank_images/Emblem_{rank}.png' alt='drawing' width='20'/>\n")

        if "Most Played Position" in extra_info and "Rank" in extra_info and "Main Lane" in config["Extra Info"] and config["Extra Info"]["Main Lane"]:
            position = extra_info["Most Played Position"]
            common_names = {"TOP": "Top", "JUNGLE": "Jungle", "MIDDLE": "Middle", "BOTTOM": "Bottom", "UTILITY": "Support"}
            file_names = {"TOP": "Top", "JUNGLE": "Jungle", "MIDDLE": "Mid", "BOTTOM": "Bot", "UTILITY": "Support"}
            rank = extra_info["Rank"][0] + extra_info["Rank"][1:].lower()
            if position == "ARAM":
                f.write(f"Most Played Position: {common_names[position]}\n")
            else:
                shutil.copyfile(f'position_images/Position_{rank}-{file_names[position]}.png', f'readme-lol-items/Position_{rank}-{file_names[position]}.png')
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
        shutil.copyfile(f'loading_images/{recent_champ_img}.png', f'readme-lol-items/{recent_champ_img}.png')
        f.write(f"</pre></th><th><pre>Last Played\n-----------\n<img align='center' src='readme-lol-items/{recent_champ_img}.png' alt='drawing' width='80'/>\n</pre></th></tr>\n")
        


        # We need to do this because otherwise we the table will alternate styling
        f.write("<tr></tr>\n")

        # Print Mastery
        if "Mastery" in config["Extra Info"] and config["Extra Info"]["Mastery"]:
            f.write("<tr><th><pre>Top 3 Champion Masteries\n------------------------</pre><table align='center'>\n")

            f.write("<tr></tr>\n")
            f.write("<tr>\n")
            for champ in mastery_info:
                shutil.copyfile(f'loading_images/{champ[1]}.png', f'readme-lol-items/{champ[1]}.png')
                f.write(f"<th><pre><img align='center' src='readme-lol-items/{champ[1]}.png' alt='drawing' width='80'/></pre></th>\n")
            f.write("</tr>\n")


            f.write("<tr></tr>\n")
            f.write("<tr>\n")
            for champ in mastery_info:
                f.write(f"<th><pre>{champ[0]}: {champ[2]}</pre></th>")
            f.write("</tr>\n")
            f.write("</table>\n")

        f.write("</th></tr></table>\n\n")
        #f.write("[By rithikasilva](https://github.com/rithikasilva)\n")



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


'''
Generates data for the main widget
'''
def get_main_section_data(puuid, api_key, extra_data, list_of_matches):
    # Generate a list of champions that I played in the last x matches
    last_champs_played = []
    played_positions = []

    time_ccing = 0
    ability_usage = 0
    solo_kills = 0
    take_downs = 0

    for match in list_of_matches:
        response = rf.get_match_data(match, api_key)
        for participant in response["info"]["participants"]:
            if participant["puuid"] == puuid:
                last_champs_played.append(participant["championName"])
                ability_usage += participant["challenges"]["abilityUses"]
                played_positions.append(participant["individualPosition"])
                time_ccing += participant["timeCCingOthers"]
                solo_kills += participant["challenges"]["soloKills"]
                take_downs += participant["challenges"]["takedowns"]
        time.sleep(1)


    extra_data["Takedowns"] = take_downs
    extra_data["Solokills"] = solo_kills
    extra_data["Ability Count"] = ability_usage
    extra_data["Most Played Position"] = max(set(played_positions), key=played_positions.count)
    if extra_data["Most Played Position"] == "Invalid": extra_data["Most Played Position"] = "ARAM"
    extra_data["Seconds of CC"] = time_ccing




    # Generates the information for the 5 most played champions
    total_length = len(last_champs_played)
    five_played_percentage = Counter(last_champs_played)
    for key_counts in five_played_percentage:
        five_played_percentage[key_counts] = (five_played_percentage[key_counts] / total_length) * 100
    five_most_played = sorted(five_played_percentage, key=five_played_percentage.get, reverse=True)[:5]


    return extra_data, last_champs_played, five_most_played, five_played_percentage





'''
Generate data for the mastery widget
'''
def get_mastery_section_data(id, api_key):
    # Get mastery information
    champ_id_points = rf.get_masteries(id, api_key)
    champ_data = dd.get_champion_data()

    for id in champ_id_points:
        for champ in champ_data:
            if int(champ_data[champ]["key"]) == int(id["championId"]):
                id["champName"] = champ_data[champ]["name"]
                break

    list_masteries = [[x["champName"], x["championPoints"]] for x in champ_id_points][:3]
    mastery_info = [[x[0], dd.get_loading_image(x[0], "loading_images"), x[1]] for x in list_masteries]
    return mastery_info







def main():

    # Max is 100
    total_matches_to_look = 100


    '''
    Collect all the required information, but only populate with what is configured.
    '''


    load_dotenv()
    extra_data = {}



    key = os.getenv("API_KEY")
    config = json.load(open("readme-lol-items/config.json"))

    name = config["Summoner Name"]
    id, puuid = rf.get_summoner_identifiers(name, key)
    rank_data = rf.get_summoner_rank(id, key)
    extra_data["Rank"] = rank_data["tier"]





    matches = rf.get_summoners_matches(puuid, key, 0, total_matches_to_look)
    




    # Returns the extra_data and a reverse list of the recently played champions
    extra_data, last_champs_played, five_most_played, five_played_percentage = get_main_section_data(puuid, key, extra_data, matches)



    # Get Mastery Info
    mastery_info = get_mastery_section_data(id, key)

     

    '''
    last_champs: list of champ names from last played to nth played
    ordered: list of five champ names from most played to least
    mastery_info [["champname", "specific_loading_image", mastery_score]]
    counts: {'champname': percentage}
    '''


    # Gather the square and loading images
    dd.get_champ_images(five_played_percentage, "square_champs")
    loading_image = dd.get_loading_image(last_champs_played[0], "loading_images")



    # CREATE THE WIDGET
    create_played_and_recent_widget(config, "README.md", "readme_lol_stats.md", five_most_played, five_played_percentage, loading_image, extra_data, total_matches_to_look, mastery_info)
    print("Finished")





if __name__ == "__main__":
    main()