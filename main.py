from dotenv import load_dotenv
import os
import json
from collections import Counter
import shutil
import data_dragon_functions as dd
import riot_api_functions as rf
import time
import logging




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


def copy_file_contents_to_destination(target_file, source_file):
    # Open the the actual destination
    final_file_lines = open(target_file, encoding='utf-8').readlines()
    readme_lol_stats_file = open(source_file, encoding='utf-8').readlines()
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




def last_played_champ_squares(list_of_champs):
    dd.get_champ_images(list_of_champs, "square_champs")
    result = ""
    for champ in list_of_champs:
        shutil.copyfile(f'square_champs/{champ}.png', f"readme-lol-items/{champ}.png")
        result = f"{result}<img src='readme-lol-items/{champ}.png' alt='drawing' width='20'/>  "
    return result



def create_played_and_recent_widget(target_file, temp_file, config, global_data, main_widget_info, mastery_widget_info):
     # Write the actual display content to a temporary file
    with open(temp_file, "w", encoding="utf-8") as f:
        f.write(f"<h3 align='center'> Data from Last {global_data['Total Matches']} Matches </h3>")
        f.write(f"<table align='center'><tr></tr>\n")
        f.write(f"<tr align='left'><th><pre>Top {len(main_widget_info['Most Played'])} Recently Played Champions\n-------------------------\n")
        for champ in main_widget_info['Most Played']:
            shutil.copyfile(f'square_champs/{champ}.png', f"readme-lol-items/{champ}.png")
            f.write(f"<img src='readme-lol-items/{champ}.png' alt='drawing' width='20'/>" + f" {champ}".ljust(dd.get_longest_name() + 4, " ") + create_loading_bar(main_widget_info['Percentages'][champ]) + f"{round(main_widget_info['Percentages'][champ], 2): .2f}%\n".rjust(9, " "))
        f.write(f"-------------------------\n")
        

        # Main Window Extra Info
        if config["Extra Info"].get("Seconds of CC"):
            cc = main_widget_info["Extra"]["Seconds of CC"]
            f.write(f"Seconds CCing Enemies: {cc}\n")
        
        if config["Extra Info"].get("Display Rank"):
            rank = main_widget_info["Extra"]["Rank"][0] + main_widget_info["Extra"]["Rank"][1:].lower()
            shutil.copyfile(f'rank_images/Emblem_{rank}.png', f'readme-lol-items/Emblem_{rank}.png')
            f.write(f"Current Rank: {rank} <img src='rank_images/Emblem_{rank}.png' alt='drawing' width='20'/>\n")

        if config["Extra Info"].get("Main Lane"):
            position = main_widget_info["Extra"]["Most Played Position"]
            common_names = {"TOP": "Top", "JUNGLE": "Jungle", "MIDDLE": "Middle", "BOTTOM": "Bottom", "UTILITY": "Support", "ARAM": "Aram"}
            file_names = {"TOP": "Top", "JUNGLE": "Jungle", "MIDDLE": "Mid", "BOTTOM": "Bot", "UTILITY": "Support"}
            rank = main_widget_info["Extra"]["Rank"][0] + main_widget_info["Extra"]["Rank"][1:].lower()
            if position == "ARAM":
                f.write(f"Most Played Position: {common_names[position]}\n")
            else:
                shutil.copyfile(f'position_images/Position_{rank}-{file_names[position]}.png', f'readme-lol-items/Position_{rank}-{file_names[position]}.png')
                f.write(f"Most Played Position: {common_names[position]} <img src='position_images/Position_{rank}-{file_names[position]}.png' alt='drawing' width='20'/>\n")

        if config["Extra Info"].get("Ability Count"):
            count = main_widget_info["Extra"]["Ability Count"]
            f.write(f"Total Abilities Used: {count}\n")

        if config["Extra Info"].get("Solokills"):
            solokills = main_widget_info["Extra"]["Solokills"]
            f.write(f"Total Solokills: {solokills}\n")
        
        if config["Extra Info"].get("Takedowns"):
            take_downs = main_widget_info["Extra"]["Takedowns"]
            f.write(f"Total Takedowns: {take_downs}\n")
        
        if config["Extra Info"].get("K/D/A"):
            f.write(f"KDA: {main_widget_info['Extra']['Kills']}/{main_widget_info['Extra']['Deaths']}/{main_widget_info['Extra']['Assists']}\n")

        if config["Extra Info"].get("Pentakills"):
            f.write(f"Pentakills: {main_widget_info['Extra']['Pentakills']}\n")

        if config["Extra Info"].get("Quadrakills"):
            f.write(f"Quadrakills: {main_widget_info['Extra']['Quadrakills']}\n")

        if config["Extra Info"].get("Triplekills"):
            f.write(f"Triplekills: {main_widget_info['Extra']['Triplekills']}\n")

        if config["Extra Info"].get("Doublekills"):
            f.write(f"Doublekills: {main_widget_info['Extra']['Doublekills']}\n")



        f.write("</pre></th>")

        # Master Section Info
        if config["Extra Info"].get("Mastery"):
            f.write(f"<th><pre>Top 3 Champion Masteries\n------------------------\n")
            for champ in mastery_widget_info['Top Three Data']:
                shutil.copyfile(f'loading_images/{champ[1]}.png', f'readme-lol-items/{champ[1]}.png')
                f.write(f"<img align='center' src='readme-lol-items/{champ[1]}.png' alt='drawing' width='50'/> ")
                f.write(f"{champ[0]}: {champ[2]} \n")
            f.write(f"</pre></th>")


            
        f.write(f"</tr></table>\n")

        

        # Minimal Widget of Last 10 Champions
        '''temp_list_of_champs = main_widget_info["Extra"].get("Last Played Champs")[:10]
        f.write(f"<table align='center'><tr></tr><tr><th><pre>Last {len(temp_list_of_champs)} Champions\n")
        f.write(f'{last_played_champ_squares(temp_list_of_champs)}\n')
        f.write("</pre></th></tr></table>")'''


        if config.get("Toggle Credit"):
            f.write("<h6 align='center'>\n\n")
            f.write("[README LoL Stats](https://github.com/marketplace/actions/readme-lol-stats) by [rithikasiilva](https://github.com/rithikasilva)\n")
            f.write("</h6>\n")


    # Copy the generated widget to the correct file and delete temporary file
    copy_file_contents_to_destination(target_file, temp_file)
    os.remove(temp_file)


    
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

    global_kills = 0
    global_deaths = 0
    global_assists = 0

    pentakills = 0
    quadrakills = 0
    triplekills = 0
    doublekills = 0


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

                global_kills += participant["kills"]
                global_deaths += participant["deaths"]
                global_assists += participant["assists"]

                pentakills += participant["pentaKills"]
                quadrakills += participant["quadraKills"]
                triplekills += participant["tripleKills"]
                doublekills += participant["doubleKills"]


        time.sleep(1)


    extra_data["Takedowns"] = take_downs
    extra_data["Solokills"] = solo_kills
    extra_data["Ability Count"] = ability_usage
    extra_data["Most Played Position"] = max(set(played_positions), key=played_positions.count)
    if extra_data["Most Played Position"] == "Invalid": extra_data["Most Played Position"] = "ARAM"
    extra_data["Seconds of CC"] = time_ccing

    extra_data["Kills"] = global_kills
    extra_data["Deaths"] = global_deaths
    extra_data["Assists"] = global_assists

    extra_data["Pentakills"] = pentakills
    extra_data["Quadrakills"] = quadrakills
    extra_data["Triplekills"] = triplekills
    extra_data["Doublekills"] = doublekills

    extra_data["Last Played Champs"] = last_champs_played

    # Generates the information for the 5 most played champions
    total_length = len(last_champs_played)
    played_percentage = Counter(last_champs_played)
    for key_counts in played_percentage:
        played_percentage[key_counts] = (played_percentage[key_counts] / total_length) * 100
    recent_most_played = sorted(played_percentage, key=played_percentage.get, reverse=True)[:5]


    return {"Most Played": recent_most_played, "Percentages": played_percentage, "Extra": extra_data}





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
    return {"Top Three Data": mastery_info}








def main():
    logging.basicConfig()
    logging.basicConfig(format='%(message)s')
    log = logging.getLogger(__name__)
    try:

        load_dotenv()
        total_matches_to_look = 10


        key = os.getenv("API_KEY")
        config = json.load(open("readme-lol-items/config.json"))


        extra_data = {}
        if "Matches" in config: total_matches_to_look = max(1, min(abs(config["Matches"]), 100))


        name = config["Summoner Name"]
        id, puuid = rf.get_summoner_identifiers(name, key)
        rank_data = rf.get_summoner_rank(id, key)
        extra_data["Rank"] = rank_data["tier"]
        global_data = {"Total Matches":  total_matches_to_look}


        # Get list of matches for the given user
        matches = rf.get_summoners_matches(puuid, key, 0, total_matches_to_look)
        

        # Returns the extra_data and a reverse list of the recently played champions
        main_widget_info = get_main_section_data(puuid, key, extra_data, matches)
        # Get Mastery Info
        mastery_widget_info = get_mastery_section_data(id, key)

        
        # Gather the square and loading images
        dd.get_champ_images(main_widget_info["Most Played"], "square_champs")
   
     
        target_file = config["Target File"]
        temp_file = "readme_lol_stats.md"
        create_played_and_recent_widget(target_file, temp_file, config, global_data, main_widget_info, mastery_widget_info)
        print("Finished")
    
    except FileNotFoundError:
        log.warning('File not found. Ensure correct directory structure and files exist.')
    except rf.BadRequest as e:
        log.warning(f'BAD REQUEST ---- {e}')





if __name__ == "__main__":
    main()
