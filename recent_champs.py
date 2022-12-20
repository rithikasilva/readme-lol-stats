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
    try:
        load_dotenv()
        key = os.getenv("api-key")


        # Get my id
        response = requests.get("https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/R1tzcrackers", {"api_key": key})
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



        ordered = sorted(counts, key=counts.get, reverse=True)


        print(counts)        
        



        get_champ_images(counts, "champs")
        


        with open("README.md", "w", encoding="utf-8") as f:
            f.write("<pre>\n")
            f.write("Recently Played Champions\n-------------------------\n")
            amount = 0
            for champ in ordered:
                if amount >= 5:
                    break
                f.write(f"<img src='champs/{champ}.png' alt='drawing' width='20'/>" + f" {champ}".ljust(30, " ") + create_loading_bar(counts[champ]) + f"{round(counts[champ], 2): .2f}%\n".rjust(9, " "))
                amount += 1
            f.write("</pre>")

        print("Finished")
    except Exception as e:
        print(e)
        #print(response)


if __name__ == "__main__":
    main()