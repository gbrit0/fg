
import os
import subprocess
from typing import List
import platform
import signal

import pathControll

homePath = pathControll.home_path()
system = platform.system()


def start(
        version: str,
        jar_name: str,
        args: List[str],
):
    try:
        versionDict = pathControll.getVersion(version)

        jar_info = None
        for dependencie in versionDict['dependencies']:
            if dependencie['name'] == jar_name:
                jar_info = dependencie
                break
        
        if jar_info is None:
            return f"Error: Jar '{jar_name}' not found in version '{version}' dependencies"

        jar_path = os.path.join(homePath, version, jar_info['localName'])

        if not os.path.exists(jar_path):
            return f"Error: Jar file not found at {jar_path}"

        if system == "Windows":
            java_path = os.path.join(homePath, version, 'jdk/bin/java.exe')
        else:
            java_path = os.path.join(homePath, version, 'jdk/bin/java')

        if not os.path.exists(java_path):
            return f"Error: Java executable not found at {java_path}"

        cmd = [java_path, '-jar', jar_path]
        if args is not None:
            cmd += args

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
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    stdin=subprocess.PIPE,
                    preexec_fn=os.setsid
                )
            
            pid = process.pid
            return f"Application started successfully. PID: {pid}"

        except subprocess.SubprocessError as e:
            return f"Error starting application: {str(e)}"
        except Exception as e:
            return f"Unexpected error while starting application: {str(e)}"

    except KeyError as e:
        return f"Error: Missing key in version data - {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"


def stop(
        pid: int,
):
    try:
        if not isinstance(pid, int) or pid <= 0:
            return "Error: Invalid PID provided"

        if system == "Windows":
            try:
                subprocess.run(['taskkill', '/F', '/PID', str(pid)], check=True)
            except subprocess.CalledProcessError as e:
                return f"Error stopping process (PID: {pid}): {str(e)}"
        else:
            try:
                os.killpg(os.getpgid(pid), signal.SIGTERM)
            except ProcessLookupError:
                return f"Error: Process with PID {pid} not found"
            except PermissionError:
                return f"Error: Permission denied when trying to stop process {pid}"
            except Exception as e:
                return f"Error stopping process (PID: {pid}): {str(e)}"
        
        return f"Application instance (PID: {pid}) stopped successfully"

    except Exception as e:
        return f"Unexpected error while stopping application: {str(e)}"