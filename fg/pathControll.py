
import os
import platform
import json
from typing import Dict, Any, List

FG_HOME = "fg/fg_app/"

def home_path() -> str:
    """Retorna o caminho base do FHIR Guard."""
    try:
        return FG_HOME
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
            
        if not url:
            raise ValueError(f"URL do JDK não encontrada para {system}")
            
        return url
    except Exception as e:
        raise RuntimeError(f"Erro ao obter URL do JDK: {str(e)}")

def getDependencies(version: str) -> List[Dict[str, str]]:
    """Obtém a lista de dependências para uma versão específica."""
    try:
        version_dict = getVersion(version)
        
        if 'dependencies' not in version_dict:
            raise KeyError(f"A versão {version} não contém informações de dependências")
            
        dependencies = version_dict['dependencies']
        
        if not isinstance(dependencies, list):
            raise ValueError("Dependências devem ser uma lista")
            
        return dependencies
    except Exception as e:
        raise RuntimeError(f"Erro ao obter dependências: {str(e)}")



