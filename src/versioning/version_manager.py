from .fg_manager import fg_install, fg_uninstall, fg_update, fg_list, fg_available
from .fg_utils import FG_HOME

class VersionManager:
    @staticmethod
    def init():
        FG_HOME.mkdir(parents=True, exist_ok=True)
        print("Módulo Controle de Versões iniciado.")

    @staticmethod
    def install(version):
        fg_install(version)

    @staticmethod
    def uninstall(version):
        fg_uninstall(version)

    @staticmethod
    def update():
        fg_update()

    @staticmethod
    def list_installed():
        fg_list()

    @staticmethod
    def list_available():
        fg_available()
