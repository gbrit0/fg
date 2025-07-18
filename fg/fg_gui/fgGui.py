import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QLineEdit, QTextEdit, QListWidget, QTableWidget,
                             QTableWidgetItem, QGroupBox, QComboBox, QSpinBox, QProgressBar,
                             QMessageBox, QFileDialog, QSplitter, QTreeWidget, QTreeWidgetItem, QInputDialog)
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QColor, QFont
from packaging.version import Version
from manager import (install, uninstall, set_default_version, clear_default_version)
from controller import (start, stop)
import monitor
import pathControll
import time
import psutil

class FHIRGuardGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FHIR Guard - Management Interface")
        self.setGeometry(100, 100, 1000, 700)
        self.default_version = pathControll.get_default_version()
        # Initialize data attributes first
        self.installed_versions = [v["nome"] for v in pathControll.list()]
        self.versoes_info = pathControll.available()
        self.available_versions = [v["versao"] for v in self.versoes_info]
        self.running_instances = monitor.status()
        
        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # Create tabs - order matters here
        self.create_dashboard_tab()
        self.create_versions_tab()
        self.create_instances_tab()  # Now installed_versions is available
        self.create_logs_tab()
        
        # Status bar
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Ready")
        
        # Update UI with initial data
        self.update_versions_list()
        self.update_instances_table()
        
        # Timer for periodic updates
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_status)
        self.update_timer.start(1000)  # Update every 1 seconds

    def create_dashboard_tab(self):
        """Create the dashboard tab with overview information"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Welcome section
        welcome_group = QGroupBox("FHIR Guard Management")
        welcome_layout = QVBoxLayout()
        welcome_label = QLabel("Welcome to FHIR Guard Management Interface")
        welcome_label.setFont(QFont("Arial", 14, QFont.Bold))
        welcome_layout.addWidget(welcome_label)
        
        # Quick actions
        quick_actions_label = QLabel("Quick Actions:")
        quick_actions_label.setFont(QFont("Arial", 10, QFont.Bold))
        welcome_layout.addWidget(quick_actions_label)
        
        button_layout = QHBoxLayout()
        self.start_btn = QPushButton("Start Instance")
        self.start_btn.clicked.connect(self.start_instance)
        self.stop_btn = QPushButton("Stop Instance")
        self.stop_btn.clicked.connect(self.stop_instance)
        self.update_btn = QPushButton("Check for Updates")
        self.update_btn.clicked.connect(self.check_for_updates)
        
        button_layout.addWidget(self.start_btn)
        button_layout.addWidget(self.stop_btn)
        button_layout.addWidget(self.update_btn)
        welcome_layout.addLayout(button_layout)
        
        welcome_group.setLayout(welcome_layout)
        layout.addWidget(welcome_group)
        
        # System status
        status_group = QGroupBox("System Status")
        status_layout = QVBoxLayout()
        
        # Current version info
        version_layout = QHBoxLayout()
        version_layout.addWidget(QLabel("Current Default Version:"))
        self.current_version_label = QLabel(self.default_version if self.default_version else "None")
        version_layout.addWidget(self.current_version_label)
        version_layout.addStretch()
        status_layout.addLayout(version_layout)
        
        # Running instances summary
        instances_layout = QHBoxLayout()
        instances_layout.addWidget(QLabel("Running Instances:"))
        self.running_instances_label = QLabel("2")
        instances_layout.addWidget(self.running_instances_label)
        instances_layout.addStretch()
        status_layout.addLayout(instances_layout)
        
        # Resource usage
        resource_group = QGroupBox("Resource Usage")
        resource_layout = QVBoxLayout()
        
        # CPU usage
        CPU_layout = QHBoxLayout()
        CPU_layout.addWidget(QLabel("CPU Usage:"))
        self.CPU_progress = QProgressBar()
        self.CPU_progress.setValue(0)
        CPU_layout.addWidget(self.CPU_progress)
        resource_layout.addLayout(CPU_layout)
        
        # Memory usage
        memory_layout = QHBoxLayout()
        memory_layout.addWidget(QLabel("Memory Usage:"))
        self.memory_progress = QProgressBar()
        self.memory_progress.setValue(0)
        memory_layout.addWidget(self.memory_progress)
        resource_layout.addLayout(memory_layout)
        
        resource_group.setLayout(resource_layout)
        status_layout.addWidget(resource_group)
        
        status_group.setLayout(status_layout)
        layout.addWidget(status_group)
        
        # Recent logs preview
        logs_group = QGroupBox("Recent Logs")
        logs_layout = QVBoxLayout()
        self.logs_preview = QTextEdit()
        self.logs_preview.setReadOnly(True)
        self.logs_preview.setPlainText("2023-05-15 10:30:45 [INFO] Application started\n2023-05-15 10:30:47 [INFO] Server listening on port 8080")
        logs_layout.addWidget(self.logs_preview)
        logs_group.setLayout(logs_layout)
        layout.addWidget(logs_group)
        
        self.tab_widget.addTab(tab, "Dashboard")

    def create_versions_tab(self):
        """Create the versions management tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Splitter for left/right panels
        splitter = QSplitter(Qt.Horizontal)
        
        # Left panel - version management
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        # Available versions
        available_group = QGroupBox("Available Versions")
        available_layout = QVBoxLayout()
        
        self.available_table = QTableWidget()
        self.available_table.setColumnCount(3)
        self.available_table.setHorizontalHeaderLabels(["Version", "Release Date", "JDK"])
        self.available_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.available_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        available_layout.addWidget(self.available_table)
        
        install_layout = QHBoxLayout()
        self.version_combo = QComboBox()
        install_layout.addWidget(self.version_combo)
        self.install_btn = QPushButton("Install")
        self.install_btn.clicked.connect(self.install_version)
        install_layout.addWidget(self.install_btn)
        available_layout.addLayout(install_layout)
        self.progressBar = QProgressBar()
        self.progressBar.setValue(0)
        self.progressBar.setTextVisible(True)
        available_layout.addWidget(self.progressBar)
        available_group.setLayout(available_layout)
        left_layout.addWidget(available_group)
        
        # Installed versions
        installed_group = QGroupBox("Installed Versions")
        installed_layout = QVBoxLayout()
        
        self.installed_list = QListWidget()
        installed_layout.addWidget(self.installed_list)
        
        button_layout = QHBoxLayout()
        self.set_default_btn = QPushButton("Set as Default")
        self.set_default_btn.clicked.connect(self.set_default_version)
        self.uninstall_btn = QPushButton("Uninstall")
        self.uninstall_btn.clicked.connect(self.uninstall_version)
        self.uninstall_all_btn = QPushButton("Uninstall All")
        self.uninstall_all_btn.clicked.connect(self.uninstall_all_versions)

        button_layout.addWidget(self.set_default_btn)
        button_layout.addWidget(self.uninstall_btn)
        button_layout.addWidget(self.uninstall_all_btn)
        installed_layout.addLayout(button_layout)
        
        installed_group.setLayout(installed_layout)
        left_layout.addWidget(installed_group)
        
        # Right panel - version details
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        details_group = QGroupBox("Version Details")
        details_layout = QVBoxLayout()
        
        self.version_details = QTextEdit()
        self.version_details.setReadOnly(True)
        details_layout.addWidget(self.version_details)
        
        details_group.setLayout(details_layout)
        right_layout.addWidget(details_group)
        
        # Add panels to splitter
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setStretchFactor(1, 2)
        
        layout.addWidget(splitter)
        self.tab_widget.addTab(tab, "Versions")

    def create_instances_tab(self):
        """Create the instances management tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Instance controls
        controls_group = QGroupBox("Instance Controls")
        controls_layout = QHBoxLayout()
        
        self.start_version_combo = QComboBox()
        self.start_version_combo.addItems(self.installed_versions)
        controls_layout.addWidget(QLabel("Version:"))
        controls_layout.addWidget(self.start_version_combo)
        
        self.start_btn_tab = QPushButton("Start Instance")
        self.start_btn_tab.clicked.connect(self.start_instance)
        controls_layout.addWidget(self.start_btn_tab)
        
        self.stop_btn_tab = QPushButton("Stop Selected")
        self.stop_btn_tab.clicked.connect(self.stop_instance)
        controls_layout.addWidget(self.stop_btn_tab)
        
        controls_group.setLayout(controls_layout)
        layout.addWidget(controls_group)
        
        # Running instances table
        self.instances_table = QTableWidget()
        self.instances_table.setColumnCount(7)
        self.instances_table.setHorizontalHeaderLabels(["PID", "Version", "Port", "Uptime", "Memory", "CPU", "Tasks"])
        self.instances_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.instances_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.instances_table.setSelectionMode(QTableWidget.SingleSelection)
        
        layout.addWidget(self.instances_table)
        
        self.tab_widget.addTab(tab, "Instances")

    def create_logs_tab(self):
        """Cria a aba de logs com seleção por aplicação"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Controles de log
        log_controls = QHBoxLayout()
        
        # Combo box para selecionar aplicação (ex: validator)
        self.log_app_combo = QComboBox()
        self.log_app_combo.addItems(self.get_running_apps())
        log_controls.addWidget(QLabel("Aplicação:"))
        log_controls.addWidget(self.log_app_combo)
        
        # Controles de tail/follow
        self.tail_spin = QSpinBox()
        self.tail_spin.setRange(10, 1000)
        self.tail_spin.setValue(100)
        log_controls.addWidget(QLabel("Últimas linhas:"))
        log_controls.addWidget(self.tail_spin)
        
        self.follow_check = QPushButton("Seguir")
        self.follow_check.setCheckable(True)
        log_controls.addWidget(self.follow_check)
        self.follow_check.toggled.connect(self.refresh_logs)
        
        self.refresh_logs_btn = QPushButton("Atualizar")
        self.refresh_logs_btn.clicked.connect(self.refresh_logs)
        log_controls.addWidget(self.refresh_logs_btn)
        
        layout.addLayout(log_controls)
        
        # Visualizador de logs
        self.log_viewer = QTextEdit()
        self.log_viewer.setReadOnly(True)
        self.log_viewer.setFont(QFont("Courier New", 9))
        layout.addWidget(self.log_viewer)
        
        self.tab_widget.addTab(tab, "Logs")

    def update_versions_list(self):
        """Update the list of installed and available versions"""
        self.installed_list.clear()
        self.installed_list.addItems(self.installed_versions)
        
        self.available_table.setRowCount(len(self.versoes_info))
        for row, info in enumerate(self.versoes_info):
            self.available_table.setItem(row, 0, QTableWidgetItem(info["versao"]))
            self.available_table.setItem(row, 1, QTableWidgetItem(info["data"]))
            self.available_table.setItem(row, 2, QTableWidgetItem(info["jdkVersao"]))
        
        # Update version combos
        self.start_version_combo.clear()
        self.start_version_combo.addItems(self.installed_versions)
        
        # Update version combo in versions tab
        self.version_combo.clear()
        self.version_combo.addItems([v for v in self.available_versions if v not in self.installed_versions])

    def update_instances_table(self):
        """Update the table while ensuring all fields exist"""
        self.running_instances = [inst for inst in self.running_instances if psutil.pid_exists(int(inst.get("PID", -1)))]
        self.instances_table.setRowCount(len(self.running_instances))
        
        for row, instance in enumerate(self.running_instances):
            # Ensure all fields have values
            pid = str(instance.get("PID", "N/A"))
            version = str(instance.get("Version", "unknown"))
            port = str(instance.get("Port", "unknown"))
            uptime = str(instance.get("Uptime", "0m"))
            memory = str(instance.get("Memory", "0MB"))
            cpu = str(instance.get("CPU", "0%"))
            tasks = str(instance.get("Tasks", "0"))
            
            # Create table items
            self.instances_table.setItem(row, 0, QTableWidgetItem(pid))
            self.instances_table.setItem(row, 1, QTableWidgetItem(version))
            self.instances_table.setItem(row, 2, QTableWidgetItem(port))
            self.instances_table.setItem(row, 3, QTableWidgetItem(uptime))
            
            # Memory with coloring
            memory_item = QTableWidgetItem(memory)
            try:
                if float(memory.replace("MB", "").strip()) > 800:
                    memory_item.setForeground(QColor("red"))
            except:
                pass
            self.instances_table.setItem(row, 4, memory_item)
            
            # CPU with coloring
            cpu_item = QTableWidgetItem(cpu)
            try:
                if float(cpu.replace("%", "").strip()) > 50:
                    cpu_item.setForeground(QColor("red"))
            except:
                pass
            self.instances_table.setItem(row, 5, cpu_item)
            
            self.instances_table.setItem(row, 6, QTableWidgetItem(tasks))
                
        # Update running apps in logs tab
        self.log_app_combo.clear()
        self.log_app_combo.addItems(self.get_running_apps())
        
        # Update running instances count
        self.running_instances_label.setText(str(len(self.running_instances)))
    def refresh_logs(self):
        """Atualiza os logs baseado no nome da aplicação"""
        app_name = self.log_app_combo.currentText()
        if not app_name:
            return

        try:
            # Encontra a versão associada à aplicação em execução
            version = None
            for instance in self.running_instances:
                if 'Version' in instance:
                    apps = pathControll.getApps(instance['Version'])
                    if any(app['nome'] == app_name for app in apps):
                        version = instance['Version']
                        break

            if not version:
                raise ValueError(f"Aplicação {app_name} não está em execução ou versão não encontrada")

            if self.follow_check.isChecked():
                # Modo "Seguir" - usar thread separada
                if hasattr(self, 'log_worker'):
                    self.log_worker.stop()
                    self.log_worker.wait()
                    
                self.log_worker = LogWorker(
                    app_name=app_name,
                    version=version,
                    tail=self.tail_spin.value()
                )
                self.log_worker.new_log.connect(self.append_log)
                self.log_worker.start()
                
            else:
                # Modo normal (sem seguir)
                if hasattr(self, 'log_worker'):
                    self.log_worker.stop()
                    self.log_worker.wait()
                    del self.log_worker

                # Obtém os logs com a versão correta
                log_lines = list(monitor.logs(
                    nome=app_name,
                    versao=version,
                    tail=self.tail_spin.value(),
                    follow=False
                ))
                
                self.log_viewer.setPlainText("\n".join(log_lines))

        except FileNotFoundError:
            self.log_viewer.setPlainText(f"Arquivo de log não encontrado para {app_name}")
        except Exception as e:
            self.log_viewer.setPlainText(f"Erro ao ler logs: {str(e)}")

    def append_log(self, text):
        """Adiciona uma linha de log ao visualizador"""
        self.log_viewer.append(text.strip())
        # Rolagem automática para a última linha
        cursor = self.log_viewer.textCursor()
        cursor.movePosition(cursor.End)
        self.log_viewer.setTextCursor(cursor)
        
    def start_instance(self):
        """Start a new instance by selecting an app from the default version"""
        version = self.default_version
        if not version:
            QMessageBox.warning(self, "No Default Version", "Please set a default version before starting an instance.")
            return

        try:
            apps = pathControll.getApps(version)
            if not apps:
                raise Exception("No apps available for this version.")

            app_names = [app["nome"] for app in apps]

            selected_app, ok = QInputDialog.getItem(self, "Select Application",
                                                f"Available apps for version {version}:", app_names, 0, False)
            if not ok or not selected_app:
                return

            # Get just the PID (since start() returns only PID)
            pid = start(version, selected_app)
            
            # Ensure PID is treated as string throughout the application
            pid_str = str(pid)
            
            # Create new instance with default port
            new_instance = {
                "PID": pid_str,  # Store as string
                "Version": version,
                "Port": "unknown",  # Default value
                "Uptime": "0m",
                "Memory": "0MB",
                "CPU": "0%",
                "Tasks": "0",
                "start_time": str(int(time.time())),  # Add timestamp
                "is_new": True  # Mark as new instance
            }
            
            # Add to running instances
            self.running_instances.append(new_instance)
            
            # Force immediate update
            self.update_instances_table()
            
            # Write to monitor's PID file (if needed)
            monitor.save_pid(pid_str, version, selected_app, port=None)
            
            self.logs_preview.append(f"{pid_str} - Instance started")
            QMessageBox.information(self, "Instance Started",
                                f"App started successfully\nPID: {pid_str}")
            self.status_bar.showMessage(f"Instance {pid_str} started", 3000)

        except Exception as e:
            QMessageBox.critical(self, "Start Error", str(e))

    def stop_instance(self):
        selected_rows = self.instances_table.selectedItems()
        if selected_rows:
            PID = selected_rows[0].text()
            reply = QMessageBox.question(self, "Confirm Stop", f"Stop instance {PID}?", QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                try:
                    stop(int(PID))
                    self.running_instances = [inst for inst in self.running_instances if str(inst.get("PID", "")) != PID]
                    self.update_instances_table()
                    self.logs_preview.append(f"{PID} - Instance stopped")
                    QMessageBox.information(self, "Stopped", f"Instance {PID} stopped.")
                    self.status_bar.showMessage(f"Instance {PID} stopped", 3000)
                except Exception as e:
                    QMessageBox.critical(self, "Stop Failed", str(e))
     
    def install_version(self):
        version = self.version_combo.currentText()
        if not version:
            QMessageBox.warning(self, "Nenhuma Versão Selecionada", "Por favor, selecione uma versão.")
            return

        if version in self.installed_versions:
            QMessageBox.information(self, "Already Installed", f"Version {version} is already installed.")
            return

        self.install_thread = InstallThread(version)
        self.install_thread.progress.connect(self.atualizar_barra_progresso)
        self.install_thread.finished.connect(self.instalacao_concluida)
        self.install_thread.error.connect(self.instalacao_falhou)

        self.progressBar.setValue(0)
        self.install_thread.start()

    def atualizar_barra_progresso(self, valor):
        self.progressBar.setValue(valor)

    def instalacao_concluida(self, versao):
        QMessageBox.information(self, "Instalação Concluída", f"Versão {versao} instalada com sucesso.")
        self.installed_versions = [v["nome"] for v in pathControll.list()]
        self.update_versions_list()
        self.status_bar.showMessage(f"Versão {versao} instalada com sucesso", 3000)

    def instalacao_falhou(self, erro):
        QMessageBox.critical(self, "Erro na Instalação", erro)
        self.status_bar.showMessage("Falha na instalação", 3000)

    def uninstall_version(self):
        """Uninstall the selected version"""
        selected_items = self.installed_list.selectedItems()
        if selected_items:
            version = selected_items[0].text()
            
            # Check if version is running
            running_versions = [inst["version"] for inst in self.running_instances]
            if version in running_versions:
                QMessageBox.warning(self, "Version in Use", 
                                  f"Cannot uninstall {version} while it's running. Stop all instances first.")
                return
            
            # Confirm uninstall
            reply = QMessageBox.question(self, "Confirm Uninstall", 
                                       f"Are you sure you want to uninstall version {version}?",
                                       QMessageBox.Yes | QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                try:
                    msg = uninstall(version)
                    QMessageBox.information(self, "Uninstallation Complete", msg)

                    # Atualiza listas
                    self.installed_versions = [v["nome"] for v in pathControll.list()]
                    self.update_versions_list()
                    if version == self.default_version:
                        clear_default_version()
                        self.default_version = None
                        self.current_version_label.setText("None")
                    self.status_bar.showMessage(f"Version {version} uninstalled", 3000)

                except Exception as e:
                    QMessageBox.critical(self, "Uninstallation Error", str(e))
        else:
            QMessageBox.warning(self, "No Selection", "Please select a version to uninstall")

    def uninstall_all_versions(self):
        """Uninstall all versions that are not currently running"""
        if not self.installed_versions:
            QMessageBox.information(self, "No Versions", "There are no installed versions to uninstall.")
            return

        # Verifica se alguma versão instalada está em uso
        running_versions = [inst["version"] for inst in self.running_instances]
        protected_versions = set(self.installed_versions).intersection(running_versions)

        if protected_versions:
            QMessageBox.warning(
                self,
                "Running Versions Detected",
                f"Cannot uninstall all. The following versions are currently running: {', '.join(protected_versions)}.\n"
                f"Stop them before proceeding."
            )
            return

        # Confirmação do usuário
        reply = QMessageBox.question(
            self,
            "Confirm Uninstall All",
            "Are you sure you want to uninstall ALL versions?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                for version in list(self.installed_versions):
                    uninstall(version)  # remove do disco
                self.installed_versions = [v["nome"] for v in pathControll.list()]
                self.update_versions_list()
                clear_default_version()
                self.default_version = None
                self.current_version_label.setText("None")
                QMessageBox.information(self, "Uninstallation Complete", "All versions have been uninstalled.")
                self.status_bar.showMessage("All versions uninstalled successfully", 3000)

            except Exception as e:
                QMessageBox.critical(self, "Uninstallation Error", str(e))

    def set_default_version(self):
        """Set the selected version as default"""
        selected_items = self.installed_list.selectedItems()
        if selected_items:
            version = selected_items[0].text()

            try:
                set_default_version(version)
                self.default_version = version
                self.current_version_label.setText(version)

                QMessageBox.information(self, "Default Version Set",
                                        f"FHIR Guard {version} is now the default version.")
                self.status_bar.showMessage(f"Version {version} set as default", 3000)

            except Exception as e:
                QMessageBox.critical(self, "Erro ao definir versão padrão", str(e))
        else:
            QMessageBox.warning(self, "No Selection", "Please select a version to set as default")

    def check_for_updates(self):
        """Check for available updates"""
        latest = max(self.available_versions, key=Version)  # pega a versão mais nova corretamente

        if latest not in self.installed_versions:
            reply = QMessageBox.question(self, "Update Available", 
                                    f"New version {latest} is available. Would you like to install it now?",
                                    QMessageBox.Yes | QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                self.version_combo.setCurrentText(latest)
                self.install_version()
        else:
            QMessageBox.information(self, "No Updates", 
                                "You have the latest version installed.")

    def update_status(self):
        """Update status without losing manually added instances"""
        try:
            # Get current status from monitor
            current_status = monitor.status() or []
            
            # Create lookup of current instances with string PIDs
            current_pids = {str(inst.get("PID", "")): inst for inst in current_status if "PID" in inst}
            
            # Update our instances list
            updated_instances = []
            
            # First add all monitored instances (converting PIDs to strings)
            for inst in current_status:
                if "PID" in inst:
                    inst_copy = inst.copy()
                    inst_copy["PID"] = str(inst_copy["PID"])  # Ensure PID is string
                    pid = inst_copy["PID"]
                    if pid not in [str(i.get("PID", "")) for i in updated_instances if "PID" in i]:
                        updated_instances.append(inst_copy)
            
            # Then add our new instances that monitor might not know about yet
            for our_inst in self.running_instances:
                if "PID" in our_inst:
                    our_pid = str(our_inst["PID"])
                    if our_inst.get("is_new") and our_pid not in current_pids:
                        updated_instances.append(our_inst)
            
            self.running_instances = updated_instances
            self.update_instances_table()
            cpu_total = 0.0
            mem_total_mb = 0.0
            count = 0

            for inst in self.running_instances:
                try:
                    # CPU calculation
                    cpu = float(inst.get("CPU", "0").replace("%", ""))
                    cpu_total += cpu
                    
                    # Memory calculation
                    mem_str = inst.get("Memory", "0MB")
                    mem_mb = float(mem_str.replace("MB", "").strip())
                    mem_total_mb += mem_mb
                    
                    count += 1
                except:
                    continue

            # Update CPU progress
            if count > 0:
                avg_cpu = min(100, cpu_total / count)
                self.CPU_progress.setValue(int(avg_cpu))
            else:
                self.CPU_progress.setValue(0)

            # Update Memory progress - calculate percentage of used system memory
            system_mem = psutil.virtual_memory()
            if system_mem.total > 0:
                # Calculate percentage of system memory used by FHIR instances
                mem_percent = (mem_total_mb * 1024 * 1024) / system_mem.total * 100
                self.memory_progress.setValue(int(mem_percent))
            else:
                self.memory_progress.setValue(0)
                
        except Exception as e:
            print(f"Status update error: {str(e)}")
   
    def get_running_apps(self):
        """Retorna lista de aplicações em execução com suas versões"""
        running_apps = set()
        for instance in self.running_instances:
            if 'Version' in instance:
                apps = pathControll.getApps(instance['Version'])
                running_apps.update(app['nome'] for app in apps)
        return sorted(running_apps)
  
    def closeEvent(self, event):
        """Garante que a thread de logs seja parada ao fechar"""
        if hasattr(self, 'log_worker'):
            self.log_worker.stop()
            self.log_worker.wait()
        event.accept()
    
class LogWorker(QThread):
    new_log = pyqtSignal(str)  # Sinal para emitir novas linhas de log
    
    def __init__(self, app_name, version, tail=None, parent=None):
        super().__init__(parent)
        self.app_name = app_name
        self.version = version
        self.tail = tail
        self.running = True
        
    def run(self):
        try:
            for line in monitor.logs(
                nome=self.app_name,
                versao=self.version,
                tail=self.tail,
                follow=True
            ):
                if not self.running:
                    break
                self.new_log.emit(line)
        except Exception as e:
            self.new_log.emit(f"Erro ao ler logs: {str(e)}")
            
    def stop(self):
        self.running = False
        
        
class InstallThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, version):
        super().__init__()
        self.version = version

    def run(self):
        try:
            id = -1
            def progresso_callback(p):
                self.progress.emit(p)

            for msg in install(self.version):
                if msg["indice"] != id:
                    id = msg["indice"]
                else:
                    progresso_callback(int(msg["porcentagem"]))
            self.finished.emit(self.version)

        except Exception as e:
            self.error.emit(str(e))

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Modern look
    
    # Set application font
    font = QFont()
    font.setFamily("Segoe UI")
    font.setPointSize(10)
    app.setFont(font)
    
    window = FHIRGuardGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()