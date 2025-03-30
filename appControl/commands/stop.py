from interfaces.command import Command

class StopCommand(Command):
   """
   Para uma instância da aplicação em execução.

   PID pode ser obtido do comando `fg status`.

   Desligamento gracioso (Gracefull shutdown) com timeout de 10 segundos por padrão;

   Sucesso (em verde): Instância da aplicação (PID: [pid]) parada com sucesso.
   Falha (em vermelho): Erro ao parar a instância da aplicação (PID: [pid]): [erro].
   """
   def __init__(self, pid):
      """
      Inicializa o comando de parada com o PID especificado.
      """
      super().__init__()
      self.pid = pid

   def execute(self ):
      print(f"Parando {self.pid}...")
      # Lógica de parada do pacote
      
      print(f"{self.pid} parado com sucesso.")