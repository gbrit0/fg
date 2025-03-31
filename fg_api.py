import requests

GITHUB_API_URL = "https://api.github.com/repos/gbrit0/fg/releases"

#Obtém as versões disponíveis via releases do GitHub.
def get_available_versions():
    try:
        response = requests.get(GITHUB_API_URL)
        response.raise_for_status()
        releases = response.json()
        return [release["tag_name"] for release in releases]
    except requests.RequestException:
        print("Erro ao buscar versões do FHIR Guard no GitHub!")
        return []