from interfaces.command import Command

class InstallCommand(Command):
   """
   Instala uma versão específica do aplicativo.

   Suporta somente versionamento semântico: 'x.y.z' (ex: 1.0.0, 2.1.3).

   Cria um arquivo padrão de configuração localizado em $FG_HOME/[version]/config.yaml.

   Sucesso (em verde): Versão [versão] instalada com sucesso.
   Falha (em vermelho): Erro ao instalar a versão [versão]: [erro].
   """

   def __init__(self, version):
      """
      Inicializa o comando de instalação com a versão especificada.
      """
      super().__init__()
      self.version = version

   def execute(self):
      print(f"Instalando {self.version}...")
      # Lógica de instalação do pacote

      print(f"{self.version} instalada com sucesso.")