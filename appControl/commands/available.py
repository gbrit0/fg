from interfaces.command import Command

class AvailableCommand(Command):
   """
   Lista todas as versões disponíveis, independente do que está instalado no diretório de trabalho

   Mostra as versões semânticas e as datas de lançamento.
   """

   def execute(self):
      print("Version     Release Date")
      print("---------   ------------")
      # for version in self.get_available_versions():
      #    print(f"{version['version']}   {version['release_date']}")

   def get_available_versions(self):
      """
      Retorna uma lista de versões disponíveis.
      """
      # Lógica para obter as versões disponíveis
      return [
         {"version": "1.0.0", "release_date": "2023-01-01"},
         {"version": "1.1.0", "release_date": "2023-02-01"},
         {"version": "2.0.0", "release_date": "2023-03-01"},
      ]
      # Exemplo de retorno de versões disponíveis