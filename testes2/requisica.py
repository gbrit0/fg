import requests

url = "https://api.github.com/repos/hapifhir/org.hl7.fhir.core/releases"

resposta = requests.get(url)
print(resposta.json())

if resposta.status_code == 200:
    releases = resposta.json()
    print(releases)
    
    for release in releases:
        print("🔹 Versão:", release['tag_name'])
        print("📄 Nome:", release['name'])
        print("📝 Descrição:")
        print(release['body'] or "Sem descrição")
        
        print("📦 Assets para download:")
        for asset in release['assets']:
            print(f"  - {asset['name']} → {asset['browser_download_url']}")
        
        print("-" * 40)
else:
    print("Erro ao acessar API:", resposta.status_code)
