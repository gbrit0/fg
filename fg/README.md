# Análise e Recomendações para o Módulo Core da CLI (1.1)

## Tecnologias Recomendadas e Justificativas

### 1\. Processador de Comandos e Argumentos

Tecnologia escolhida: Typer  
Motivos:

* Typer é construído sobre Click, mas com foco em simplicidade e type hints nativos  
* Excelente suporte para autocompletion no terminal  
* Geração automática de help (--help)  
* Integração natural com Python type hints (alinhado com critérios de qualidade do projeto)  
* Menos boilerplate que Click puro  
* Suporte a subcomandos hierárquicos (como visto nos requisitos: fg start, fg stop, etc.)

Alternativa: Click seria uma boa opção também, mas exigiria mais código boilerplate.

### 2\. Gerenciador de Diretórios e Configurações

Tecnologias:

* pathlib (nativo do Python) para manipulação de caminhos multiplataforma  
* os (módulo nativo) para operações do sistema de arquivos  
* dotenv para variáveis de ambiente (opcional)

Motivos:

* pathlib é mais moderno e seguro que os.path  
* Manipulação consistente de caminhos entre Windows/Linux/macOS  
* Suporte nativo para operações como .fg no home directory

### 3\. Sistema de Logging

Tecnologia: Loguru  
Motivos:

* Muito mais simples que o módulo logging padrão  
* Suporte nativo a cores (importante para mensagens de erro/sucesso destacadas)  
* Formatação fácil de logs  
* Rotação de arquivos de log automática  
* Melhor experiência para o usuário final com mensagens claras

## Resultados Esperados do Seu Desenvolvimento

1. CLI Funcional:  
   * Todos os comandos principais (fg start, fg stop, fg list, etc.) devem ser reconhecidos e processados  
   * Sistema de ajuda integrado gerado automaticamente (--help)  
   * Parsing robusto de argumentos e opções (como \--dir, \--log-level)  
2. Gerenciamento de Diretórios:  
   * Criação automática da estrutura $FG\_HOME/versions/\[version\]  
   * Resolução correta do diretório padrão (\~/.fg) ou customizado (via \--dir ou FG\_HOME)  
   * Operações de arquivo seguras e multiplataforma  
3. Sistema de Logging:  
   * Mensagens formatadas e coloridas conforme o nível (erro=vermelho, sucesso=verde)  
   * Suporte aos níveis debug, info, warn, error  
   * Logs persistentes em arquivo quando necessário  
4. Integração com Outros Módulos:  
   * API clara para outros módulos registrarem comandos  
   * Mecanismo para compartilhar configurações globais (como FG\_HOME)  
5. Critérios de Qualidade:  
   * 100% de cobertura de testes para o core (já que é fundamental)  
   * Documentação completa de todas as funções públicas  
   * Type hints em todo o código  
   * Tempo de inicialização \<0.5s (como especificado)

## Relacionamento com Outros Módulos

### 1\. Módulo 1.2 (Gerenciamento de Versões)

* Como: Seu módulo irá chamar comandos como fg install que delegam para o 1.2  
* Interface: Defina uma API clara para operações de versão (ex: get\_installed\_versions())

### 2\. Módulo 1.3 (Controle de Aplicação)

* Como: Comandos como fg start/stop precisam se integrar com o gerenciador de processos  
* Interface: Crie um protocolo para iniciar/parar processos e verificar status

### 3\. Módulo 1.4 (Configuração)

* Como: Seu módulo precisa ler configurações básicas (como paths padrão)  
* Interface: Defina como configs são carregadas (ex: load\_global\_config())

### 4\. Módulo 1.6 (Comunicação de Rede)

* Como: Para operações como fg update que verificam versões online  
* Interface: Crie um cliente HTTP abstrato que o 1.6 implementa
