from interfaces.command import Command

class ConfigCommand(Command):
   """
   Exibe (somente leitura) a configuração detalhada de uma versão específica da aplicação.

   COnfigurações só podem ser modificadas editando manual o arquivo fonte YAML localizado em $FG_HOME/[version]/config.yaml.

   Exemplo de saída:

      Configuration for version 1.1.0:
      Source file: /home/user/.fg/versions/1.1.0/config.yaml

      Current settings (read-only):
      Server:
      - Host: 0.0.0.0
      - Port: 8080
      - Read Timeout: 30s
      - Write Timeout: 30s

      Security:
      - TLS: enabled
      - Auth: enabled
      - JWT Expiry: 24h

      Resources:
      - Max Memory: 1024MB
      - Max CPU: 2
      - Workers: 10

      [...]

      To modify these settings, edit the YAML file directly.
      See Configuration Reference for all available options.
   """

   def __init__(self, version):
      """
      Inicializa o comando de busca de configuração com a versão especificada.
      """
      super().__init__()
      self.version = version

   def execute(self):
      print(f"Exibindo configuração para a versão {self.version}...")
      # Lógica para exibir a configuração do pacote