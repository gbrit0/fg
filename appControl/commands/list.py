from interfaces.command import Command

class ListCommand(Command):
   """
   Esibe todas as versões da aplicação instaladas.

   A versão mais recente instalada é automaticamente definida como a versão padrão e marcada com um asterisco (*);

   Exemplo:
   
      Versões instaladas:
      * 1.1.0 (padrão - mais recente)
        1.0.0
        0.9.0
   
   """