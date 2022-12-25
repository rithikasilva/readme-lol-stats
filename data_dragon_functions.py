import requests
import json



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
    config = json.load(open("readme-lol-items/config.json"))
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


def get_version():
    patch = requests.get("https://ddragon.leagueoflegends.com/api/versions.json")
    latest_version = patch.json()[0]
    return latest_version


def get_champion_data():
    response = requests.get(f"https://ddragon.leagueoflegends.com/cdn/{get_version()}/data/en_US/champion.json")
    response = response.json()
    champ_data = response["data"]
    return champ_data



def get_longest_name():
    data = get_champion_data()
    names = []
    for id in data:
        names.append(data[id]["name"])
    longest = len(max(names, key=len))
    return longest

