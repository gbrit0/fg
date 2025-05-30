import json
import os
import psutil
import time

import pathControll

PIDS_FILE = "fg/dependencias/pids.json"

def pids_path():
    return PIDS_FILE

def save_pid(
    pid,
    version: str,
    command: str,
    port: int = None, # Porta é opcional
):
    pids = {}
    if os.path.exists(pids_path()):
        with open(pids_path(), "r") as f:
            try:
                pids = json.load(f)
            except json.JSONDecodeError:
                pids = {}

    pids[str(pid)] = {
        "version": version,
        "port": port,
        "start_time": time.time(), # Agora salva o horário que o processo foi iniciado
        "command": command
    }

    with open(pids_path(), "w") as f:
        json.dump(pids, f, indent=4)

        
def clean_dead_pids():
    if not os.path.exists(pids_path()):
        return
    with open(pids_path(), "r") as f:
        pids = json.load(f)

    alive_pids = {}
    for pid_str, command in pids.items():
        pid = int(pid_str)
        if psutil.pid_exists(pid):
            alive_pids[pid_str] = command

    with open(pids_path(), "w") as f:
        json.dump(alive_pids, f)

def status():
    clean_dead_pids()

    if not os.path.exists(PIDS_FILE):
        return []

    with open(PIDS_FILE, "r") as f:
        pids = json.load(f)

    status_list = []

    for pid_str, info in pids.items():
        pid = int(pid_str)
        try:
            proc = psutil.Process(pid)

            # Calcula o uptime
            start_time = info.get("start_time", time.time())
            uptime_seconds = time.time() - start_time
            uptime_str = format_uptime(uptime_seconds)

            # Pega memory usage em MB
            memory_mb = proc.memory_info().rss / (1024 * 1024)

            # CPU usage percentual
            cpu_percent = proc.cpu_percent(interval=0.1)
            cpu_percent /= psutil.cpu_count() #divide pelo número de núcloes 

            # Número de threads (tasks)
            tasks = len(proc.threads())

            status_list.append({
                "PID": pid,
                "Version": info.get("version", "unknown"),
                "Port": info.get("port", "unknown"),
                "Uptime": uptime_str,
                "Memory": f"{memory_mb:.2f} MB",
                "CPU": f"{cpu_percent:.2f}%",
                "Tasks": tasks
            })

        except psutil.NoSuchProcess:
            # Se o processo morreu depois da clean_dead_pids, ignora aqui
            continue
        except Exception as e:
            # Algum outro erro, você pode logar se quiser
            continue
    return status_list

def format_uptime(seconds):
    """Formata o uptime em dias, horas, minutos e segundos."""
    minutes, sec = divmod(int(seconds), 60)
    hour, minutes = divmod(minutes, 60)
    day, hour = divmod(hour, 24)
    if day > 0:
        return f"{day}d {hour}h {minutes}m {sec}s"
    elif hour > 0:
        return f"{hour}h {minutes}m {sec}s"
    elif minutes > 0:
        return f"{minutes}m {sec}s"
    else:
        return f"{sec}s"
    

def logs(
    nome: str,
    versao: str,
    tail: int = None,
    follow: bool = False
):
    logsPath = None
    for app in pathControll.getApps(versao):
        if app['nome'] == nome:
            logsPath = os.path.join(pathControll.home_path(), versao, nome, app['logs'])
            break

    if logsPath is None or not os.path.exists(logsPath):
        raise FileNotFoundError(f"Log file for app '{nome}' not found.")

    def ler_ultimas_linhas(caminho: str, n: int):
        with open(caminho, 'rb') as f:
            f.seek(0, os.SEEK_END)
            pos = f.tell()
            linhas = []
            buffer = b''
            while pos > 0 and len(linhas) < n:
                pos -= 1
                f.seek(pos)
                char = f.read(1)
                if char == b'\n':
                    if buffer:
                        linhas.append(buffer[::-1].decode(errors='ignore'))
                        buffer = b''
                else:
                    buffer += char
            if buffer:
                linhas.append(buffer[::-1].decode(errors='ignore'))
        return linhas[::-1]

    if follow and tail is not None:
        # Mostrar as últimas tail linhas em tempo real
        linhas_mostradas = 0
        with open(logsPath, 'r', encoding='utf-8', errors='ignore') as f:
            
            f.seek(0, os.SEEK_END)
            while linhas_mostradas < tail:
                nova_linha = f.readline()
                if nova_linha:
                    yield nova_linha.strip()
                    linhas_mostradas += 1
                else:
                    time.sleep(0.5)
    elif follow:
        with open(logsPath, 'r', encoding='utf-8', errors='ignore') as f:
            f.seek(0, os.SEEK_END)
            while True:
                nova_linha = f.readline()
                if nova_linha:
                    yield nova_linha.strip()
                else:
                    time.sleep(0.5)
    elif tail is not None:
        for linha in ler_ultimas_linhas(logsPath, tail):
            yield linha.strip()
    else:
        with open(logsPath, 'r', encoding='utf-8', errors='ignore') as f:
            for linha in f:
                yield linha.strip()
    