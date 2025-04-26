fhir-guard/
│
├── fg/                        # Core do CLI 
│   ├── fg.py                  # Executável do CLI, o main, a entrada
│   ├── manager.py             # Instalação, atualização, remoção de versões
│   ├── controller.py          # Start/stop/status de instâncias
│   ├── monitor.py             # Monitoramento (CPU, memória, logs)
│   ├── config.py              # Leitura e edição do config.yaml
│   └── registry.py            # Consulta e download de versões
│
├── fg_gui/                    # Interface gráfica (opcional)
│   ├── app.py                 # Inicializador da GUI
│   ├── views/                 # Telas principais (status, config, etc.)
│   └── components/            # Componentes visuais reutilizáveis
│
├── fg_app/                    # Aplicações Java (gerenciadas)
│   ├── v1.0.0/                # Versão 1.0.0 da app
│   │   ├── app.jar
│   │   └── libs/
│   ├── v1.1.0/
│   └── ...
│
├── config/                    # Arquivos de configuração
│   └── config.yaml            # Config global e por instância
│
├── logs/                      # Armazenamento de logs das instâncias
│   └── instance_001.log
│
├── registry/                  # Cache de versões disponíveis (opcional)
│   └── index.json
│
├── scripts/                   # Scripts auxiliares
│   └── install_jdk.sh         # Instalação automática do JDK
│
└── requirements.txt           # Dependências do projeto Python