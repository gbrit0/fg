from interfaces.command import Command

class UninstallCommand(Command):
   """
   Remove uma versão específica da aplicação.

   Requer confirmação: "Confirma a desinstalação da versão [versão]? (s/n)".

   Não pode desinstalar uma versão que esteja rodando.

   Sucesso (em verde): "Versão [versão] desinstalada com sucesso."
   Falha (em vermelho): "Erro ao desinstalar a versão [versão]: [erro]".
   """

   def __init__(self, version):
      """
      Inicializa o comando de desinstalação com a versão especificada.
      """
      super().__init__()
      self.version = version

   def execute(self):
      """
      Executa o comando de desinstalação para o pacote especificado.
      """
      print(f"Desinstalando {self.version}...")
      # Lógica de desinstalação do pacote
      
      print(f"{self.version} desinstalado com sucesso.")