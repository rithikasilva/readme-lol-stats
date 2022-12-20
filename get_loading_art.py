import requests



champ = "Yasuo_9"
response = requests.get(f"https://ddragon.leagueoflegends.com/cdn/img/champion/loading/{champ}.jpg")
open(f"vertical.png", "wb").write(response.content)


