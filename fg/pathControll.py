import os
import platform
import json
from typing import Dict, Any, List
from datetime import datetime
import manager

FG_HOME = os.environ.get("FG_HOME", "fg")
installPath = os.path.join(FG_HOME, "fg_app")

def set_home_path(homePath: str):
    global FG_HOME, installPath
    FG_HOME = homePath
    installPath = os.path.join(FG_HOME, "fg_app")

def home_path() -> str:
    try:
        return installPath
    except Exception as e:
        raise RuntimeError(f"Erro ao determinar o caminho base: {str(e)}")


def procurarNovasVersoes():
    try:
        file_path = "fg/dependencias/modelo.json"
        url = "https://raw.githubusercontent.com/gbrit0/fg/refs/heads/main/arquivosParaDownload/modelo.json"

        for _ in manager.download_com_progresso(url, file_path):
            pass
    
    except Exception as e:
        raise Exception(f"Erro ao buscar novas versão: {e}")


def openJson() -> Dict[str, Any]:
    try:

        file_path = "fg/dependencias/modelo.json"

        if not os.path.exists(file_path):
            procurarNovasVersoes()

        with open(file_path, "r", encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        raise ValueError(f"Erro ao decodificar o arquivo JSON: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Erro ao abrir o arquivo de dependências: {str(e)}")

def getVersion(version: str) -> Dict[str, Any]:
    try:
        data = openJson()
        if not isinstance(data, dict):
            raise ValueError("O arquivo JSON não contém um objeto válido")
        if version not in data:
            available_versions = ", ".join(data.keys())
            raise ValueError(f"Versão {version} não encontrada. Versões disponíveis: {available_versions}")
        return data[version]
    except Exception as e:
        raise RuntimeError(f"Erro ao obter versão {version}: {str(e)}")

def getJdkUrl(version: str) -> str:
    try:
        version_dict = getVersion(version)
        jdk_urls = version_dict.get("jdk", {}).get("urls", {})
        system = platform.system()
        if system == "Windows":
            return jdk_urls.get("windows", "")
        elif system == "Linux":
            return jdk_urls.get("linux", "")
        elif system == "Darwin":
            return jdk_urls.get("mac", "")
        else:
            raise NotImplementedError(f"Sistema operacional não suportado: {system}")
    except Exception as e:
        raise RuntimeError(f"Erro ao obter URL do JDK: {str(e)}")

def getDependencies(version: str) -> List[Dict[str, str]]:
    version_dict = getVersion(version)
    dependencies = []
    for app in version_dict.get("apps", []):
        dependencies.extend(app.get("dependencias", []))
    return dependencies

def available() -> List[Dict[str, str]]:
    try:
        datas = openJson()
        if datas is None or not isinstance(datas, dict) or not datas:
            raise ValueError("[AVISO] Nenhuma versão válida encontrada")

        result = []

        for version, data in datas.items():
            try:
                release_date = data.get("data")
                jdk_versao = data.get("jdk", {}).get("versao", "desconhecido")

                if not release_date:
                    raise ValueError(f"[ERRO] Versão {version} não possui campo 'data'")

                result.append({
                    "versao": version,
                    "data": release_date,
                    "jdkVersao": jdk_versao
                })

            except Exception as e:
                raise RuntimeError(f"[ERRO] Ao processar versão {version}: {str(e)}")

        return result

    except Exception as e:
        raise RuntimeError(f"[ERRO CRÍTICO] {str(e)}")


def mostRecentVersion():
    try:
        datas = openJson()
        if not isinstance(datas, dict) or not datas:
            raise ValueError("Nenhuma versão disponível no arquivo de configuração")

        recent_version = None
        recent_date = None
        for version, data in datas.items():
            release_date = data.get("data")
            if not release_date:
                continue
            current_date = datetime.strptime(release_date, "%d/%m/%Y")
            if recent_date is None or current_date > recent_date:
                recent_date = current_date
                recent_version = version
        return recent_version
    except Exception as e:
        raise RuntimeError(f"Falha ao determinar a versão mais recente: {str(e)}")

def mostRecentInstalledVersion():
    homePath = home_path()
    datas = openJson()
    installed_versions = []

    for item in os.listdir(homePath):
        full_path = os.path.join(homePath, item)
        if os.path.isdir(full_path) and item in datas:
            installed_versions.append(item)

    if not installed_versions:
        return None

    recent_version = None
    recent_date = None
    for version in installed_versions:
        version_data = datas[version]
        try:
            current_date = datetime.strptime(version_data["data"], "%d/%m/%Y")
            if recent_date is None or current_date > recent_date:
                recent_version = version
                recent_date = current_date
        except (KeyError, ValueError) as e:
            raise RuntimeError(f"Erro ao processar versão {version}: {str(e)}")
    return recent_version

def list():
    try:
        homePath = home_path()
        if not os.path.isdir(homePath):
            raise FileNotFoundError(f"O diretório {homePath} não existe ou não é um diretório")

        try:
            recent = mostRecentInstalledVersion()
        except Exception as e:
            recent = None
            yield f"  [Aviso: Não foi possível determinar a versão mais recente: {str(e)}]"

        dirs_exist = False
        for item in sorted(os.listdir(homePath)):
            full_path = os.path.join(homePath, item)
            if os.path.isdir(full_path):
                dirs_exist = True
                if recent and item == recent:
                    yield f'* {item} (mais recente)'
                else:
                    yield f"  {item}"
        if not dirs_exist:
            yield "  Nenhuma versão instalada encontrada"
    except Exception as e:
        yield f"[Erro crítico: {str(e)}]"

if __name__ == "__main__":
    for item in list():
        print(item)
