
import os
import platform
import json
from typing import Dict, Any, List
from datetime import datetime

#FG_HOME = os.environ.get("FG_HOME", os.path.expanduser("~")) #tenta pegar a variavel de ambiente, se não existir usa o home mesmo
FG_HOME = os.environ.get("FG_HOME", "fg") #para testes usar esse pois fica mais facil de vizualizar

installPath = os.path.join(FG_HOME,".fg")

def set_home_path(
        homePath :str
):
    global FG_HOME, installPath
    FG_HOME = homePath
    installPath = os.path.join(FG_HOME,"fg_app")


def home_path() -> str:
    """Retorna o caminho base do FHIR Guard."""
    try:
        return installPath
    except Exception as e:
        raise RuntimeError(f"Erro ao determinar o caminho base: {str(e)}")

def openJson() -> Dict[str, Any]:
    """Abre e carrega o arquivo JSON de dependências."""
    try:
        file_path = "fg/dependencias/modelo.json"
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Arquivo de dependências não encontrado: {file_path}")
        
        with open(file_path, "r", encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        raise ValueError(f"Erro ao decodificar o arquivo JSON: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Erro ao abrir o arquivo de dependências: {str(e)}")

def getVersion(version: str) -> Dict[str, Any]:
    """Obtém os dados de uma versão específica."""
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
    """Obtém a URL do JDK para a versão e SO específicos."""
    try:
        version_dict = getVersion(version)
        
        if 'jdkUrl' not in version_dict:
            raise KeyError(f"A versão {version} não contém URLs de JDK")
            
        system = platform.system()
        jdk_urls = version_dict['jdkUrl']
        
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
    """Obtém a lista de dependências para uma versão específica."""
    version_dict = getVersion(version)

    return version_dict['dependencies']

def available():
    try:
        datas = openJson()
        
        if datas is None:
            yield "[ERRO] Nenhum dado de versão disponível (retornou None)"
            return
            
        if not isinstance(datas, dict):
            yield "[ERRO] Formato inválido - os dados devem ser um dicionário"
            return
            
        if not datas:
            yield "[AVISO] Nenhuma versão disponível no arquivo de configuração"
            return

        for version, data in datas.items():
            try:
                if version is None:
                    yield "[ERRO] Versão None encontrada nos dados"
                    continue
                    
                if data is None:
                    yield f"[ERRO] Dados da versão {version} são None"
                    continue
                    
                release_date = data.get('releaseDate')
                if release_date is None:
                    yield f"[ERRO] Versão {version} não possui releaseDate"
                    continue
                    
                yield f"{version.ljust(10)} {release_date}"
                
            except Exception as e:
                yield f"[ERRO] Ao processar versão {version}: {str(e)}"
                continue
                
    except Exception as e:
        yield f"[ERRO CRÍTICO] {str(e)}"


def mostRecentVersion():
    try:
        datas = openJson()
        
        if datas is None:
            raise ValueError("O arquivo de versões retornou None")
            
        if not isinstance(datas, dict):
            raise TypeError("Os dados das versões devem ser um dicionário")
            
        if not datas:
            raise ValueError("Nenhuma versão disponível no arquivo de configuração")

        recent_version = None
        recent_data = None

        for version, data in datas.items():
            if version is None:
                continue  # Pula versões None ou levanta erro se preferir
                
            if data is None:
                raise ValueError(f"Dados da versão {version} são None")
                
            try:
                release_date = data.get('releaseDate')
                if release_date is None:
                    raise ValueError(f"releaseDate não encontrado para a versão {version}")

                current_date = datetime.strptime(release_date, "%d/%m/%Y")

                if recent_data is None:
                    recent_version = version
                    recent_data = data
                else:
                    recent_release_date = recent_data.get('releaseDate')
                    if recent_release_date is None:
                        raise ValueError(f"releaseDate não encontrado para a versão recente {recent_version}")

                    dR = datetime.strptime(recent_release_date, "%d/%m/%Y")
                    
                    if current_date > dR:
                        recent_version = version
                        recent_data = data

            except ValueError as e:
                raise ValueError(f"Data inválida para a versão {version}: {str(e)}")
            except Exception as e:
                raise RuntimeError(f"Erro ao processar a versão {version}: {str(e)}")

        if recent_data is None:
            raise RuntimeError("Nenhuma versão válida encontrada")

        return recent_version

    except Exception as e:
        raise RuntimeError(f"Falha ao determinar a versão mais recente: {str(e)}")


def mostRecentInstalledVersion():
    homePath = home_path()
    datas = openJson()
    
    installed_versions = []
    
    # Primeiro verifica quais versões estão instaladas
    for item in os.listdir(homePath):
        full_path = os.path.join(homePath, item)
        if os.path.isdir(full_path) and item in datas:
            installed_versions.append(item)
    
    if not installed_versions:
        return None  # ou raise Exception("No installed versions found")
    
    recent_version = None
    recent_date = None
    
    # Agora compara apenas as versões instaladas
    for version in installed_versions:
        version_data = datas[version]
        try:
            current_date = datetime.strptime(version_data['releaseDate'], "%d/%m/%Y")
            
            if recent_date is None or current_date > recent_date:
                recent_version = version
                recent_date = current_date
                
        except (KeyError, ValueError) as e:
            raise f"Error processing version {version}: {str(e)}"
    
    return recent_version


def list():
    try:
        homePath = home_path()
        
        if not os.path.exists(homePath):
            raise FileNotFoundError(f"O diretório {homePath} não existe")
            
        if not os.path.isdir(homePath):
            raise NotADirectoryError(f"{homePath} não é um diretório")
        
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
                
                try:
                    if recent and item == recent:
                        yield f'* {item} (most recent)'
                    else:
                        yield f"  {item}"
                except Exception as e:
                    yield f"  [Erro ao processar {item}: {str(e)}]"
        
        if not dirs_exist:
            yield "  Nenhuma versão instalada encontrada"
            
    except Exception as e:
        yield f"[Erro crítico: {str(e)}]"
        return

if __name__ == "__main__":
    for item in list():
        print(item)


