import os
import platform
import json
from typing import Dict, Any, List
from datetime import datetime
import manager


def set_home_path(homePath: str):

    try:
        global FG_HOME, installPath
        FG_HOME = homePath
        installPath = os.path.join(FG_HOME, ".fg")
        os.makedirs(installPath, exist_ok=True)
    except Exception as e:
        raise Exception(f"Erro ao criar diretorio .fg: {e}")


set_home_path(os.environ.get("FG_HOME", os.path.expanduser("~")))


def home_path() -> str:
    try:
        return installPath
    except Exception as e:
        raise RuntimeError(f"Erro ao determinar o caminho base: {str(e)}")


def procurarNovasVersoes():
    try:
        dirPath = "fg/dependencias"
        os.makedirs(dirPath, exist_ok=True)
        
        file_path = os.path.join(dirPath, "modelo.json")

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

def getApps(version: str) -> List[Dict[str, str]]:
    version_dict = getVersion(version)
    return version_dict['apps']

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

def get_default_version():
    try:
        default_path = "fg/dependencias/versionDefault.txt"
        if os.path.exists(default_path):
            with open(default_path, "r") as f:
                return f.read().strip()
        return None
    except Exception:
        return None


def list() -> List[Dict[str, Any]]:
    """
    Lista as versões instaladas do FHIR Guard, indicando qual é a versão padrão.
    Se não houver uma versão padrão definida, usa a mais recente.
    """
    try:
        homePath = home_path()

        if not os.path.isdir(homePath):
            raise FileNotFoundError(f"O diretório {homePath} não existe ou não é um diretório.")

        # Obtem versão padrão, se houver
        try:
            default_version = manager.get_default_version()
        except Exception:
            default_version = None

        versoes_instaladas = sorted([
            item for item in os.listdir(homePath)
            if os.path.isdir(os.path.join(homePath, item))
        ])

        if not versoes_instaladas:
            return []  # Não há versões instaladas

        # Se não há default, pega a mais recente
        if not default_version:
            try:
                default_version = mostRecentInstalledVersion()
            except Exception:
                default_version = None  # Se não conseguir, permanece None

        versoes = []
        for item in versoes_instaladas:
            versoes.append({
                "nome": item,
                "default": item == default_version
            })

        return versoes

    except Exception as e:
        raise Exception(f"[Erro crítico: {str(e)}]")

if __name__ == "__main__":
    for item in list():
        print(item)
