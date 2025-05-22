from interfaces.command import Command
import subprocess


class LogsCommand(Command):
    """
    Exibe os logs de um PID.
    """

    def __init__(self, pid, tail=None, follow=False):
        self.pid = pid
        self.tail = tail
        self.follow = follow

    def execute(self):
        log_file = f"/var/log/fg/{self.pid}.log"  # Depende de onde os logs são gravados

        cmd = ["tail"]
        if self.tail:
            cmd += ["-n", str(self.tail)]
        if self.follow:
            cmd.append("-f")
        cmd.append(log_file)

        try:
            subprocess.run(cmd)
        except Exception as e:
            print(f"Erro ao ler logs: {e}")
