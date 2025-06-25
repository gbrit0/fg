import os
import subprocess
from typing import List
import platform
import signal
import shlex

import pathControll
import monitor

homePath = pathControll.home_path()
system = platform.system()


def montarComando(comando: str, versao: str, jar_name: str):
    if system == "Windows":
        java_path = os.path.join(homePath, versao, 'jdk/bin/java.exe')
    else:
        java_path = os.path.join(homePath, versao, 'jdk/bin/java')

    if not os.path.exists(java_path):
        raise FileNotFoundError(f"Java executable not found at {java_path}")

    partes = shlex.split(comando)
    novas_partes = []

    novas_partes.append(java_path)

    for parte in partes:
        if os.path.splitext(parte)[1] != '':        
            parte = os.path.join(homePath,versao,jar_name,parte)
            if not os.path.exists(parte):
                raise FileNotFoundError(f"Jar file not found at {parte}")
        novas_partes.append(parte)
    
    return novas_partes

def start(
        version: str,
        jar_name: str,
        #args: List[str],
):
    try:
        versionDict = pathControll.getVersion(version)

        comando = None
        for app in versionDict['apps']:
            if app['nome'] == jar_name:
                comando = app['comando']
                break

        if comando is None:
            raise RuntimeError(f"Jar '{jar_name}' not found in version '{version}' apps")


        cmd = montarComando(comando, version,jar_name)

        try:
            if system == "Windows":
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    stdin=subprocess.PIPE,
                    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
                )
            else:
                if hasattr(os, "setsid"):
                    process = subprocess.Popen(
                        cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        stdin=subprocess.PIPE,
                        preexec_fn=os.setsid
                    )
                else:
                    process = subprocess.Popen(
                        cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        stdin=subprocess.PIPE
                    )

            pid = process.pid
            monitor.save_pid(pid, version, " ".join(cmd))  # junta a lista de comando em uma str

            return pid

        except subprocess.SubprocessError as e:
            raise RuntimeError(f"Error starting application: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error while starting application: {str(e)}")

    except KeyError as e:
        raise KeyError(f"Missing key in version data - {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error: {str(e)}")


    
def stop(pid: int):
    if not isinstance(pid, int) or pid <= 0:
        raise ValueError("Invalid PID provided")

    if system == "Windows":
        try:
            subprocess.run(['taskkill', '/F', '/PID', str(pid)], check=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Error stopping process (PID: {pid}): {str(e)}")
    else:
        if hasattr(os, "getpgid"):
            pgid = os.getpgid(pid)
        else:
            pgid = pid
        try:
            os.killpg(pgid, signal.SIGTERM)
        except ProcessLookupError:
            raise ProcessLookupError(f"Process with PID {pid} not found")
        except PermissionError:
            raise PermissionError(f"Permission denied when trying to stop process {pid}")
        except Exception as e:
            raise RuntimeError(f"Error stopping process (PID: {pid}): {str(e)}")

    return f"Application instance (PID: {pid}) stopped successfully"

if __name__ == "__main__":


    win = ["timeout", "60"]
    lin = ["sleep", "60"]
    proc = subprocess.Popen(lin)
    print(f"Processo iniciado com PID {proc.pid}")

    

    import psutil

    def is_running(pid):
        return psutil.pid_exists(pid)
    
    print(is_running(proc.pid))

    stop(proc.pid) #parei o processo

    print(is_running(proc.pid))

    