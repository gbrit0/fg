from interfaces.command import Command

class StartCommand(Command):
   """
   Inicializa uma versão específica da aplicação (previamente instalada).

   Valida a configuração antes de iniciar.

   Sucesso (em verde): Aplicação incializada com sucesso. PID: [pid].
   Erro (em vermelho): Erro ao iniciar a aplicação: [erro].
   """

   def __init__(self, version):
      """
      Inicializa o comando de inicialização com a versão especificada.
      """
      super.__init__()
      self.version = version

   def execute(self):
      """Inicializa uma versão específica."""
      print(f"Iniciando {self.version}...")
      # Lógica de inicialização do pacote
      
      print(f"{self.version} iniciado com sucesso.")
