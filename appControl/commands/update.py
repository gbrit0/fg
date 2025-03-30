from interfaces.command import Command

class UpdateCommand(Command):
   """
   Checa se uma versão mais nova do que a versão mais recente na home está disponível. Se houver, baixa, instala e configura-a como a versão padrão.

   Exibe:
      - Sucesso (em verde): Atualizado para a versão [versão]. Essa é a versão padrão agora.
      - Sem atualizações disponíveis (em amarelo): Sem versão mais nova disponível. VOcê possui a versão mais recente: [versão atual].
      - Erro (em vermelho): Erro ao atualizar: [erro].

   Conexão com a internet é necessária para verificar atualizações.
   """

   def execute(self):
      print("Verificando atualizações...")
      # if atualizacao_disponivel:
      #    print("Atualização disponível.")
      #    self._atualizar()
      print(f"Atualizando...")
      # Lógica de atualização do pacote
      
      print(f"Atualizado com sucesso.")

   def _atualizar(self):
      print("Baixando atualização...")
      print("Instalando atualização...")
      print("Configurando versão padrão...")
      
      print("Atualização concluída com sucesso.")