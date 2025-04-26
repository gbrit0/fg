
import os
import platform
import json

FG_HOME = "fg/fg_app/"

def home_path():
    return FG_HOME

def openJson():
    with open("fg/dependencias/modelo.json", "r", encoding='utf-8') as file:
        return json.load(file)

def getVersion(version :str):

    data = openJson()

    try:
        return data[version]
    except:
        raise ValueError(f"Versão {version} não encontrada")

def getJdkUrl(version: str):
    version_dict = getVersion(version)

    system = platform.system()

    if system == "Windows":
        return version_dict['jdkUrl']["windows"]
    elif system == "Linux":
        return version_dict['jdkUrl']["linux"]
    elif system == "Darwin":
        return version_dict['jdkUrl']["mac"]
    else:
        raise NotImplementedError(f"Sistema operacional não suportado: {system}")

def getDependencies(version: str):
    version_dict = getVersion(version)

    return  version_dict['dependencies']





