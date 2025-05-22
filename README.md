# Plano de Construção de Software: FHIR Guard CLI

## 1. Arquitetura

A arquitetura do sistema será composta pelos seguintes componentes principais:

### 1.1. Módulo Core da CLI
- Processador de comandos e argumentos
- Gerenciador de diretórios e configurações
- Sistema de logging

### 1.2. Módulo de Gerenciamento de Versões
- Gerenciador de download e instalação
- Controlador de versões (listagem, atualização, remoção)
- Validador de versões semânticas

### 1.3. Módulo de Controle de Aplicação
- Gerenciador de processos (iniciar, parar, status)
- Monitor de recursos (memória, CPU, tarefas)
- Coletor de logs

### 1.4. Módulo de Configuração
- Parser e validador de YAML
- Gerenciador de configurações padrão
- Utilitário de exibição de configurações

### 1.5. Módulo GUI
- Interface gráfica de usuário
- Adaptadores para funcionalidades da CLI

### 1.6. Módulo de Comunicação de Rede
- Cliente HTTP para verificação de versões
- Gerenciador de downloads

---

## 2. Tecnologias (Python)

### 2.1. Linguagem Principal
- Python 3.9+: para compatibilidade entre plataformas e recursos modernos

### 2.2. Frameworks e Bibliotecas
- **Click ou Typer**: para processamento de comandos e argumentos CLI
- **PyYAML**: para processamento de arquivos YAML de configuração
- **Loguru ou logging**: para sistema de logging
- **Requests**: para comunicação HTTP
- **psutil**: para monitoramento de processos e recursos
- **rich**: para saída formatada e colorida no terminal
- **PyQt6 ou Tkinter**: para interface gráfica (módulo GUI)
- **pytest**: para testes unitários e de integração
- **tox**: para testes em múltiplos ambientes

### 2.3. Ferramentas de Desenvolvimento
- **Poetry ou Pipenv**: para gerenciamento de dependências e ambiente virtual
- **VS Code ou PyCharm**: como IDE principal
- **Git**: para controle de versão
- **GitHub Actions**: para CI/CD
- **pre-commit**: para verificação de qualidade de código antes de commits
- **black**: para formatação de código
- **flake8 ou pylint**: para linting
- **mypy**: para verificação de tipos (opcional)

### 2.4. Ferramentas de Empacotamento e Distribuição
- **PyInstaller ou cx_Freeze**: para criar executáveis standalone
- **setuptools e wheel**: para criação de pacotes Python
- **flit**: para publicação simplificada de pacotes

---

## 3. Critérios de Aceitação

### 3.1. Testes

#### 3.1.1. Testes Unitários
- Cobertura mínima de **80%** para código de produção
- Testes de unidade para todas as classes de utilidade

#### 3.1.2. Testes de Integração
- Testes para todos os componentes principais
- Testes de integração end-to-end para fluxos principais

#### 3.1.3. Testes de Sistema
- Testes de execução completa em ambientes **Windows, Linux e macOS**
- Testes de carga para verificar consumo de recursos

### 3.2. Qualidade de Código
- Conformidade com **PEP 8** (estilo de código Python)
- Documentação de **docstrings** para todas as funções e classes
- **Type hints** para melhorar manutenção e suporte em IDEs

### 3.3. Desempenho
- Tempo de inicialização da CLI inferior a **0.5 segundo**
- Uso eficiente de recursos para operações de longa duração

### 3.4. Compatibilidade
- Compatível com **Windows 10/11, macOS 11+ e Linux** (Ubuntu 20.04+, Fedora 34+)
- Funcional em sistemas com **Python 3.9 ou superior**

### 3.5. Usabilidade
- Mensagens de erro claras e acionáveis
- Ajuda contextual para todos os comandos (**--help**)
- Feedback de progresso para operações longas (**barras de progresso**)

### 3.6. Documentação
- Manual de usuário completo
- Guia de instalação para cada plataforma
- Documentação técnica de arquitetura
- Exemplos de uso para todos os comandos

---

## 4. Estratégia para Comunicação entre Membros da Equipe

### 4.1. Ferramentas de Comunicação
- **Discord**: para comunicação diária e discussões rápidas
- **GitHub**: para armazenamento de código e pull requests
- **Google Meet**: para reuniões virtuais

### 4.2. Processos de Comunicação

#### 4.2.1. Revisões de Código
- **Pull requests** obrigatórios para todas as mudanças
- Revisão por pelo menos **um outro membro da equipe**

#### 4.2.2. Documentação
- Decisões técnicas documentadas
- Código documentado
- Atualizações de documentação no mesmo **PR** que as mudanças de código

#### 4.2.3. Comunicação Assíncrona
- Canal específico no **Discord** para cada componente principal
- Canal de **anúncios** para comunicações importantes

## 5. Divisão de módulos

### 5.1. Módulo Core da CLI
- Moisés

### 5.2. Módulo de Gerenciamento de Versões
- Gabriel Mota

### 5.3. Módulo de Controle de Aplicação
- Gabriel Ribeiro
  
### 5.4. Módulo de Configuração
- Jarison

### 5.5. Módulo GUI
- Victor

### 5.6. Módulo de Comunicação de Rede
- Matheus
  

## Fluxograma da aplicação (Arquitetura)
<a href="https://lucid.app/lucidchart/12082aa2-ffb3-4a34-bfcb-d6fd9770d4ca/edit?beaconFlowId=A5BDFFA03A4A1A5E&invitationId=inv_10730c73-8163-4eee-b5f3-1e05ed490456&page=0_0#" target="_blank">Link</a> da arquitetura no Lucidchart

# Histórico de Sprints

### Sprint 1 – Esclarecimentos Iniciais
Reunião inicial com todos os membros do grupo para alinhar o escopo do projeto.

Discussões sobre os principais objetivos da ferramenta FHIR Guard.

Definição preliminar dos módulos e levantamento de dúvidas sobre tecnologias a serem utilizadas.

Adoção da estratégia de sprints semanais com entregas incrementais.

### Sprint 2 – Planejamento e Divisão do Trabalho
Divisão oficial dos módulos entre os membros do grupo, conforme suas especializações/interesses.

Escolha das principais bibliotecas e frameworks que serão utilizados no projeto.

### Sprint 3 - Início do Desenvolvimento
Primeiras implementações de código para os módulos atribuídos.

### Sprint 4 – Estrutura Arquitetural e Gerenciamento de Versões
Criação da branch arquitetura-inicial, com foco na estrutura base do sistema.

Implementação inicial do módulo de Gerenciamento de Versões

Integração inicial entre o módulo core da CLI e o módulo de versões.

### Sprint 5 – Simulação de Controle da Aplicação
Adição na branch main do código para simular o controle da aplicação.

Testes iniciais de execução dos comandos da CLI com esses novos recursos.

### Sprint 6??? – Estruturação da Base do Projeto Real (GUI + CLI)
Construção do esqueleto/base do projeto real que incluirá a interface gráfica (GUI).

Implementação dos comandos fundamentais na CLI, seguindo a arquitetura planejada.
