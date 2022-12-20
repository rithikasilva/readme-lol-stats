import requests
from dotenv import load_dotenv
import os
import imageio.v2 as io







def save_img(champ_id, target):
    


    # Get the latest patch
    response = requests.get("https://ddragon.leagueoflegends.com/api/versions.json")
    latest_version = response.json()[0]

    # Get data from the patch
    response = requests.get(f"https://ddragon.leagueoflegends.com/cdn/{latest_version}/data/en_US/champion.json")
    response = response.json()


    champ_name = ""
    champ_data = response["data"]
    for champ in champ_data:
        if champ_data[champ]["key"] == champ_id:
            champ_name = champ_data[champ]["name"]
            break

    
    #print(f"https://ddragon.leagueoflegends.com/cdn/{latest_version}/data/en_US/{champ_name}.json")
    #response = requests.get(f"https://ddragon.leagueoflegends.com/cdn/{latest_version}/data/en_US/champion/{champ_name}.json")
    response = requests.get(f"https://ddragon.leagueoflegends.com/cdn/{latest_version}/img/champion/{champ_name}.png")
    open(f"{target}.png", "wb").write(response.content)










def main():

    load_dotenv()
    key = os.getenv("api-key")

    response = requests.get("https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/R1tzcrackers", {"api_key": key})
    response = response.json()
    id = response["id"]
    account_id = response["accountId"]
    puuid = response["puuid"]



    response = requests.get(f"https://na1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{id}/top", {"api_key": key})

    top_champ = [str(response.json()[0]["championId"]), str(response.json()[0]["championPoints"])]
    second = [str(response.json()[1]["championId"]), str(response.json()[1]["championPoints"])]
    third = [str(response.json()[2]["championId"]), str(response.json()[2]["championPoints"])]
  
    save_img(top_champ[0], "champ1")
    save_img(second[0], "champ2")
    save_img(third[0], "champ3")


    with open("README.md", "w") as f:
        #f.write("test")

        f.write("![Champ1](champ1.png)")
        f.write(top_champ[1] + "\n\n")
        f.write("![Champ1](champ2.png)")
        f.write(second[1] + "\n\n")
        f.write("![Champ1](champ3.png)")
        f.write(third[1] + "\n\n")


    file_names = ["champ1.png", "champ2.png", "champ3.png"]
    images = []
    for filename in file_names:
        images.append(io.imread(filename))
    io.mimsave('test.gif', images, duration = 1)




if __name__ == "__main__":
    main()