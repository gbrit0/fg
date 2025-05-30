import requests

url = "https://raw.githubusercontent.com/gbrit0/fg/refs/heads/main/arquivosParaDownload/config.log" 

requisiçao = requests.get(url)

print(requisiçao)