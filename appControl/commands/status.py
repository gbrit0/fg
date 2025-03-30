from interfaces.command import Command

class StatusCommand(Command):
   """
   Exibe o status atual de todos as instâncias da aplicação em execução.

   Inclui detalhes como PID, versão, porta, uptime, uso de memória, uso de CPU e número de tasks.

   Exemplo de saída:
   PID     Version  Port   Uptime   Memory   CPU   Tasks
   1234    1.1.0    8080   2h       256MB    2%    10
   5678    1.0.0    8081   30m      128MB    1%    5
   """

   def execute(self):
      print("PID     Version  Port   Uptime   Memory   CPU   Tasks")
      # Lógica para exibir o status de cada versão