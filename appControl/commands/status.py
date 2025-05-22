from interfaces.command import Command
import psutil


class StatusCommand(Command):
    """
    Mostra o status das instâncias em execução.
    """

    def execute(self):
        print("PID     Nome               CPU%   Memória")
        print("----------------------------------------------")

        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
            try:
                if "fg" in proc.info['name']:
                    pid = proc.info['pid']
                    name = proc.info['name']
                    cpu = proc.cpu_percent(interval=0.1)
                    mem = proc.memory_info().rss // (1024 * 1024)  # em MB
                    print(f"{pid:<7} {name:<18} {cpu:<6} {mem} MB")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
