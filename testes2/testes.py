import requests

requisicao = requests.get("https://raw.githubusercontent.com/gbrit0/fg/refs/heads/main/modelo.json")


print(requisicao.json())