from dotenv import load_dotenv
import os
import json
from collections import Counter
import shutil
import data_dragon_functions as dd
import riot_api_functions as rf
import image_generation as ig
import time
import logging


'''
Given a string, replaces the API Key with stars to preventing leaking.

Paramters:
- message -- string possibly containing api_key
- api_key -- API Key to wipe

Returns:
- result -- string that replaces api_key with stars
'''
def wipe_api_key(message, api_key):
    return message.replace(api_key, "********")


'''
Creates an ASCII percentage bar given a percentage.

Parameters:
- percentage -- requested percentage to make a percentage bar of.

Returns:
- out -- A string percentage bar which is 25 characters long.
'''
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



'''
Copies all the contents of a source file and puts if in between special indicators in the target file.
The indicators used are:

"<!---LOL-STATS-START-HERE--->\n" for the start and "<!---LOL-STATS-END-HERE--->\n" for the end


Parameters:
- target_file -- file that contains the location to have content copied to.
- source_file -- file that contains information to be copied.

Returns: None
'''
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


'''
Creates data widget and copies it to the target file.

Parameters:
- target_file -- file to copy data to.
- temp_file -- name of temporary file to create to store data.
- config -- parsed json of "config.json".
- global_data -- data that applies to all current (and future) widgets such as total matches looked at.
- main_widget_info -- all information that pertains to the main widget (left most) in dictionary form.
- mastery_widget_info -- all information that pertains to the mastery widget (right most) in dictionary form.

Returns: None
'''
def create_played_and_recent_widget(target_file, temp_file, config, global_data, main_widget_info, mastery_widget_info):

    list_of_messages = []


     # Write the actual display content to a temporary file
    with open(temp_file, "w", encoding="utf-8") as f:
        f.write(f"<h3 align='center'> Data from Last {global_data['Total Matches']} Matches for {config['Summoner Name']}</h3>")
        f.write(f"<table align='center'><tr></tr>\n")
        f.write(f"<tr align='left'><th><pre>Top {len(main_widget_info['Most Played'])} Recently Played Champions\n-------------------------\n")
        
        
        for champ in main_widget_info['Most Played']:
            shutil.copyfile(f'square_champs/{champ}.png', f"readme-lol-items/{champ}.png")
            '''f.write(f"<img src='readme-lol-items/{champ}.png' alt='drawing' width='20'/>" 
            + f" {champ}".ljust(dd.get_longest_name() + 4, " ") 
            + f"<img src='readme-lol-items/{champ}_loading.gif' alt='drawing' width='170'/>"
            + f"{round(main_widget_info['Percentages'][champ], 2): .2f}%\n".rjust(9, " "))'''
            image_location = f'readme-lol-items/{champ}.png'
            ig.create_animated_loading_bar(image_location, champ, main_widget_info['Percentages'][champ], f"readme-lol-items/loading_{champ}.gif")
            f.write(f"<img src='readme-lol-items/loading_{champ}.gif' alt='drawing' width='400'/>\n")
        
        
        f.write(f"-------------------------\n")
        




        # Main Window Extra Info
        if config["Extra Info"].get("Seconds of CC"):
            cc = main_widget_info["Extra"]["Seconds of CC"]
            list_of_messages.append(f"Seconds CCing Enemies: {cc}")
        
        if config["Extra Info"].get("Display Rank"):
            if main_widget_info["Extra"]["Rank"] != "Unranked":
                rank = main_widget_info["Extra"]["Rank"].title()
                shutil.copyfile(f'rank_images/Rank={rank}.png', f'readme-lol-items/Solo-Duo-Rank.png')
                list_of_messages.append(f"Current Rank: {rank}")

        if config["Extra Info"].get("Main Lane"):
            position = main_widget_info["Extra"]["Most Played Position"]
            common_names = {"TOP": "Top", "JUNGLE": "Jungle", "MIDDLE": "Middle", "BOTTOM": "Bottom", "UTILITY": "Support", "ARAM": "Aram"}
            file_names = {"TOP": "Top", "JUNGLE": "Jungle", "MIDDLE": "Mid", "BOTTOM": "Bot", "UTILITY": "Support"}
            rank = main_widget_info["Extra"]["Rank"][0] + main_widget_info["Extra"]["Rank"][1:].lower()
            if position == "ARAM":
                list_of_messages.append(f"Most Played Position: {common_names[position]}")
            else:
                list_of_messages.append(f"Most Played Position: {common_names[position]}")

        if config["Extra Info"].get("Ability Count"):
            count = main_widget_info["Extra"]["Ability Count"]
            list_of_messages.append(f"Total Abilities Used: {count}")

        if config["Extra Info"].get("Solokills"):
            solokills = main_widget_info["Extra"]["Solokills"]
            list_of_messages.append(f"Total Solokills: {solokills}")
        
        if config["Extra Info"].get("Takedowns"):
            take_downs = main_widget_info["Extra"]["Takedowns"]
            list_of_messages.append(f"Total Takedowns: {take_downs}")
        
        if config["Extra Info"].get("K/D/A"):
            list_of_messages.append(f"KDA: {main_widget_info['Extra']['Kills']}/{main_widget_info['Extra']['Deaths']}/{main_widget_info['Extra']['Assists']}")
        if config["Extra Info"].get("Pentakills"):
            list_of_messages.append(f"Pentakills: {main_widget_info['Extra']['Pentakills']}")

        if config["Extra Info"].get("Quadrakills"):
            list_of_messages.append(f"Quadrakills: {main_widget_info['Extra']['Quadrakills']}")

        if config["Extra Info"].get("Triplekills"):
            list_of_messages.append(f"Triplekills: {main_widget_info['Extra']['Triplekills']}")

        if config["Extra Info"].get("Doublekills"):
            list_of_messages.append(f"Doublekills: {main_widget_info['Extra']['Doublekills']}")



        ig.create_extra_info(list_of_messages, "readme-lol-items/extra_info.gif")
        f.write(f"<img align='center' src='readme-lol-items/extra_info.gif' alt='drawing' width='350'/>")
        f.write("</pre></th>")
        # End main section


        # Mastery Section Info
        if config["Extra Info"].get("Mastery"):

            
            f.write(f"<th><pre>Top 3 Champion Masteries\n------------------------\n")

            images = [x for x in mastery_widget_info['Top Three Data']]
            ig.create_mastery_gif(f'loading_images/{images[0][1]}.png', 
            f'loading_images/{images[1][1]}.png', f'loading_images/{images[2][1]}.png', 
            f'{images[0][0]}: {images[0][2]}', f'{images[1][0]}: {images[1][2]}', f'{images[2][0]}: {images[2][2]}', 'readme-lol-items/mastery.gif')
            f.write(f"<img align='center' src='readme-lol-items/mastery.gif' alt='drawing' width='320'/> ")

            # '''
            # NO GIF CODE
            # '''
            # for champ in mastery_widget_info['Top Three Data']:
            #     shutil.copyfile(f'loading_images/{champ[1]}.png', f'readme-lol-items/{champ[1]}.png')
            #     f.write(f"<img align='center' src='readme-lol-items/{champ[1]}.png' alt='drawing' width='50'/> ")
            #     f.write(f"{champ[0]}: {champ[2]} \n")
            

            f.write(f"</pre></th>")

            
        f.write(f"</tr></table>\n")

        

        # # Minimal Widget of Last 10 Champions
        # temp_list_of_champs = main_widget_info["Extra"].get("Last Played Champs")[:10]
        # f.write(f"<table align='center'><tr></tr><tr><th><pre>Last {len(temp_list_of_champs)} Champions\n")
        # f.write(f'{last_played_champ_squares(temp_list_of_champs)}\n')
        # f.write("</pre></th></tr></table>")


        if config.get("Toggle Credit"):
            f.write("<h6 align='center'>\n\n")
            f.write("[README Profile LoL Stats](https://github.com/marketplace/actions/readme-profile-lol-stats) by [rithikasiilva](https://github.com/rithikasilva)\n")
            f.write("</h6>\n")


    # Copy the generated widget to the correct file and delete temporary file
    copy_file_contents_to_destination(target_file, temp_file)
    os.remove(temp_file)


    
'''
Generates data for the main section.

Parameters:
- region_name -- regional value name for summoner
- puuid -- puuid of requested summoner to look at.
- api_key -- Riot API key with general access.
- extra_data -- dictionary to populate all text based information found at the bottom of the main widget with.
- list_of_matches -- list of match id's to gather data from

Returns:
- dictionary in the format: {"Most Played": recent_most_played, "Percentages": played_percentage, "Extra": extra_data} where
recent_most_played is a list of champion names in order of most played recently, played_percentage is a dictionary with champion names and
what percentage of matches they were played recently, and extra_data (from the parameters).
'''
def get_main_section_data(region_name, puuid, api_key, extra_data, list_of_matches):
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
        response = rf.get_match_data(region_name, match, api_key)
        for participant in response["info"]["participants"]:
            if participant["puuid"] == puuid:
                last_champs_played.append(participant["championName"])

                
                played_positions.append(participant["individualPosition"])
                time_ccing += participant["timeCCingOthers"]

                if "challenges" in participant:
                    ability_usage += participant["challenges"]["abilityUses"]
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
Generate data for the mastery section.

Parameters:
- region_code -- platform code for region summoner belongs to
- id -- id of the summoner to get mastery information for.
- api_key -- Riot API key with general access.

Returns:
- a dictionary which contains a list of lists. The lowests lists contain each champions name, their loading image title, and their mastery score.
'''
def get_mastery_section_data(region_code, puuid, api_key):
    # Get mastery information
    champ_id_points = rf.get_masteries(region_code, puuid, api_key)
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
        

        test = os.listdir("readme-lol-items")
        for item in test:
            if item.endswith(".png") or item.endswith(".gif"):
                os.remove(os.path.join("readme-lol-items", item))



        items_dir = os.listdir("readme-lol-items")
        for item in items_dir:
            if item.endswith(".png") or item.endswith(".gif"):
                os.remove(os.path.join("readme-lol-items", item))


        load_dotenv()
        total_matches_to_look = 10


        key = os.getenv("API_KEY")
        config = json.load(open("readme-lol-items/config.json"))

        extra_data = {}
        if "Matches" in config: total_matches_to_look = max(1, min(abs(config["Matches"]), 100))


        name = config["Summoner Name"]
        region_code = config["Platform Routing Region Code"]
        region_name = config["Regional Routing Name"]
        id, puuid = rf.get_summoner_identifiers(region_code, name, key)
        rank_data = rf.get_summoner_rank(region_code, id, key)
        extra_data["Rank"] = rank_data["tier"]
        global_data = {"Total Matches":  total_matches_to_look}


        # Get list of matches for the given user
        matches = rf.get_summoners_matches(region_name, puuid, key, 0, total_matches_to_look)
        

        # Returns the extra_data and a reverse list of the recently played champions
        main_widget_info = get_main_section_data(region_name, puuid, key, extra_data, matches)
        # Get Mastery Info
        mastery_widget_info = get_mastery_section_data(region_code, puuid, key)

        
        # Gather the square and loading images
        dd.get_champ_images(main_widget_info["Most Played"], "square_champs")
   
     
        target_file = config["Target File"]
        temp_file = "readme_lol_stats.md"
        create_played_and_recent_widget(target_file, temp_file, config, global_data, main_widget_info, mastery_widget_info)
        print("Finished")
    
    except FileNotFoundError as e:
        log.warning('File not found. Ensure correct directory structure and files exist.')
        log.warning(e)
    except rf.RiotApiBadRequest as e:
        log.warning(f'{wipe_api_key(str(e), key)}')
    except Exception as e:
        log.warning(f'{wipe_api_key(str(e), key)}')


if __name__ == "__main__":
    main()
