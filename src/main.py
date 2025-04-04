from core.cli import run_cli
from config.yaml_parser import parse_config
from versioning.version_manager import VersionManager
from application.process_manager import ProcessManager
from gui.main_window import launch_gui
from network.http_client import HttpClient

def main():
    run_cli()
    parse_config()
    VersionManager.init()
    ProcessManager.init()
    launch_gui()
    HttpClient.init()

if __name__ == "__main__":
    main()