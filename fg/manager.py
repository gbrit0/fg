
import os
import requests
import tarfile
import zipfile
import shutil

import pathControll

def get_file_extension(url: str) -> str:
    # Remove parâmetros da URL (tudo após '?')
    clean_url = url.split('?')[0]
    # Remove fragmentos (tudo após '#')
    clean_url = clean_url.split('#')[0]
    # Pega a última parte do caminho (nome do arquivo)
    filename = os.path.basename(clean_url)
    # Separa a extensão (pode ser .zip, .tar.gz, etc.)
    _, extension = os.path.splitext(filename)
    return extension.lower()  # Retorna em minúsculas para consistência

def download_com_progresso(url: str, destino: str):
    response = requests.get(url, stream=True)
    total = int(response.headers.get('content-length', 0))
    baixado = 0
    bloco = 1024 * 32  # 32 KB

    with open(destino, 'wb') as arquivo:
        for dado in response.iter_content(chunk_size=bloco):
            arquivo.write(dado)
            baixado += len(dado)
            porcentagem = (baixado / total) * 100 if total else 0
            print(f"\r📥 Baixando: {porcentagem:6.2f}%", end='')

    print(" ✅")  # Finaliza a linha ao concluir

def extrair_com_progresso_tar(path_compactado: str, destino: str):
    with tarfile.open(path_compactado, 'r:gz') as tar:
        membros = tar.getmembers()
        total = len(membros)
        for i, membro in enumerate(membros, 1):
            tar.extract(membro, path=destino)
            porcentagem = (i / total) * 100
            print(f"\r📦 Extraindo .tar.gz: {porcentagem:6.2f}%", end='')
    print(" ✅")

def extrair_com_progresso_zip(path_compactado: str, destino: str):
    with zipfile.ZipFile(path_compactado, 'r') as zipf:
        membros = zipf.infolist()
        total = len(membros)
        for i, membro in enumerate(membros, 1):
            zipf.extract(membro, path=destino)
            porcentagem = (i / total) * 100
            print(f"\r📦 Extraindo .zip: {porcentagem:6.2f}%", end='')
    print(" ✅")

def install(version: str):
    print(f"🟡 Iniciando instalação da versão {version}...")

    homePath = pathControll.home_path()
    pathOfDownload = os.path.join(homePath, version)
    jdkPath = os.path.join(pathOfDownload, "jdk")

    if os.path.exists(pathOfDownload):
        print(f"🔄 Removendo diretório existente: {pathOfDownload}")
        shutil.rmtree(pathOfDownload)

    print(f"📁 Criando diretório: {pathOfDownload}")
    os.makedirs(pathOfDownload, exist_ok=True)

    jdkUrl = pathControll.getJdkUrl(version)
    ext = get_file_extension(jdkUrl)

    if ext == '.gz':
        print(f"⬇️ Baixando JDK (.tar.gz) de: {jdkUrl}")
        jdkCompactadoPath = os.path.join(jdkPath, "jdk.tar.gz")
        os.makedirs(jdkPath, exist_ok=True)
        download_com_progresso(jdkUrl, jdkCompactadoPath)


        print(f"📦 Extraindo arquivo: {jdkCompactadoPath}")
        extrair_com_progresso_tar(jdkCompactadoPath, jdkPath)


    elif ext == '.zip':
        print(f"⬇️ Baixando JDK (.zip) de: {jdkUrl}")
        jdkCompactadoPath = os.path.join(jdkPath, "jdk.zip")
        os.makedirs(jdkPath, exist_ok=True)
        download_com_progresso(jdkUrl, jdkCompactadoPath)


        print(f"📦 Extraindo arquivo: {jdkCompactadoPath}")
        extrair_com_progresso_zip(jdkCompactadoPath, jdkPath)


    print("🧹 Removendo arquivo compactado...")
    os.remove(jdkCompactadoPath)

    jdk_contents = os.listdir(jdkPath)
    if len(jdk_contents) == 1:
        subdir = os.path.join(jdkPath, jdk_contents[0])
        if os.path.isdir(subdir):
            print(f"📂 Reorganizando estrutura: movendo arquivos de {subdir} para {jdkPath}")
            for item in os.listdir(subdir):
                os.rename(
                    os.path.join(subdir, item),
                    os.path.join(jdkPath, item)
                )
            os.rmdir(subdir)

    print("⬇️ Baixando dependências...")
    dependencies = pathControll.getDependencies(version)
    for dependencie in dependencies:
        dependenciePath = os.path.join(pathOfDownload, dependencie['localName'])
        dependencieUrl = dependencie['url']
        print(f"   🔹 {dependencie['localName']} de {dependencieUrl}")
        download_com_progresso(dependencieUrl, dependenciePath)


    print("✅ Instalação concluída com sucesso.")



def uninstall(
        version: str
):
    homePath = pathControll.home_path()

    versionPath = os.path.join(homePath,version)

    if os.path.exists(versionPath): #se a pasta de download existir ela apaga tudo
        shutil.rmtree(versionPath)
    

if __name__ == "__main__":
    install(
        "6.5.19"
    )
