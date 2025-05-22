from interfaces.command import Command
import requests


class AvailableCommand(Command):
    """
    Lista todas as versões disponíveis no GitHub.
    """

    def execute(self):
        try:
            url = "https://api.github.com/repos/gbrit0/fg/releases"
            response = requests.get(url)
            response.raise_for_status()
            releases = response.json()

            print("Versão       Data de lançamento")
            print("------------ -------------------")
            for release in releases:
                version = release.get("tag_name", "N/A")
                date = release.get("published_at", "N/A").split("T")[0] if release.get("published_at") else "N/A"
                print(f"{version:<12} {date}")
        except Exception as e:
            print(f"Erro ao obter versões disponíveis: {e}")
