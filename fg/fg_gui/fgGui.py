import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QLineEdit, QTextEdit, QListWidget, QTableWidget,
                             QTableWidgetItem, QGroupBox, QComboBox, QSpinBox, QProgressBar,
                             QMessageBox, QFileDialog, QSplitter, QTreeWidget, QTreeWidgetItem)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor, QFont
from packaging.version import Version
from manager import (install, uninstall)
from controller import (start, stop)
import monitor
import pathControll

class FHIRGuardGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FHIR Guard - Management Interface")
        self.setGeometry(100, 100, 1000, 700)
        self.default_version = None
        # Initialize data attributes first
        self.installed_versions = [v["nome"] for v in pathControll.list()]
        self.available_versions = [v["versao"] for v in pathControll.available()] #self.available_versions = ["1.0.0", "1.1.0", "1.2.0", "2.0.0", "6.5.19"] CASO QUEIRA TESTAR
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
        self.create_configuration_tab()
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
        self.update_timer.start(5000)  # Update every 5 seconds

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
        self.current_version_label = QLabel("1.1.0")
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
        cpu_layout = QHBoxLayout()
        cpu_layout.addWidget(QLabel("CPU Usage:"))
        self.cpu_progress = QProgressBar()
        self.cpu_progress.setValue(15)
        cpu_layout.addWidget(self.cpu_progress)
        resource_layout.addLayout(cpu_layout)
        
        # Memory usage
        memory_layout = QHBoxLayout()
        memory_layout.addWidget(QLabel("Memory Usage:"))
        self.memory_progress = QProgressBar()
        self.memory_progress.setValue(35)
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
        self.available_table.setColumnCount(2)
        self.available_table.setHorizontalHeaderLabels(["Version", "Release Date"])
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
        
        self.view_config_btn = QPushButton("View Configuration")
        self.view_config_btn.clicked.connect(self.view_configuration)
        details_layout.addWidget(self.view_config_btn)
        
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

    def create_configuration_tab(self):
        """Create the configuration tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Version selection
        config_top_layout = QHBoxLayout()
        config_top_layout.addWidget(QLabel("Select Version:"))
        
        self.config_version_combo = QComboBox()
        self.config_version_combo.addItems(self.installed_versions)
        self.config_version_combo.currentTextChanged.connect(self.load_configuration)
        config_top_layout.addWidget(self.config_version_combo)
        
        self.save_config_btn = QPushButton("Save Configuration")
        self.save_config_btn.clicked.connect(self.save_configuration)
        config_top_layout.addWidget(self.save_config_btn)
        
        self.reload_config_btn = QPushButton("Reload")
        self.reload_config_btn.clicked.connect(self.load_configuration)
        config_top_layout.addWidget(self.reload_config_btn)
        
        layout.addLayout(config_top_layout)
        
        # Configuration editor
        self.config_editor = QTextEdit()
        self.config_editor.setFont(QFont("Courier New", 10))
        layout.addWidget(self.config_editor)
        
        # Load initial configuration
        self.load_configuration()
        
        self.tab_widget.addTab(tab, "Configuration")

    def create_logs_tab(self):
        """Create the logs viewer tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Log controls
        log_controls = QHBoxLayout()
        
        self.log_pid_combo = QComboBox()
        self.log_pid_combo.addItems([instance["pid"] for instance in self.running_instances])
        log_controls.addWidget(QLabel("Instance PID:"))
        log_controls.addWidget(self.log_pid_combo)
        
        self.tail_spin = QSpinBox()
        self.tail_spin.setRange(10, 1000)
        self.tail_spin.setValue(100)
        log_controls.addWidget(QLabel("Tail lines:"))
        log_controls.addWidget(self.tail_spin)
        
        self.follow_check = QPushButton("Follow")
        self.follow_check.setCheckable(True)
        log_controls.addWidget(self.follow_check)
        
        self.refresh_logs_btn = QPushButton("Refresh")
        self.refresh_logs_btn.clicked.connect(self.refresh_logs)
        log_controls.addWidget(self.refresh_logs_btn)
        
        layout.addLayout(log_controls)
        
        # Log viewer
        self.log_viewer = QTextEdit()
        self.log_viewer.setReadOnly(True)
        self.log_viewer.setFont(QFont("Courier New", 9))
        layout.addWidget(self.log_viewer)
        
        # Load initial logs
        self.refresh_logs()
        
        self.tab_widget.addTab(tab, "Logs")

    def update_versions_list(self):
        """Update the list of installed and available versions"""
        self.installed_list.clear()
        self.installed_list.addItems(self.installed_versions)
        
        self.available_table.setRowCount(len(self.available_versions))
        for row, version in enumerate(self.available_versions):
            self.available_table.setItem(row, 0, QTableWidgetItem(version))
            self.available_table.setItem(row, 1, QTableWidgetItem("2024-01-01"))  # Simulated date
        
        # Update version combos
        self.start_version_combo.clear()
        self.start_version_combo.addItems(self.installed_versions)
        
        self.config_version_combo.clear()
        self.config_version_combo.addItems(self.installed_versions)
        
        # Update version combo in versions tab
        self.version_combo.clear()
        self.version_combo.addItems([v for v in self.available_versions if v not in self.installed_versions])

    def update_instances_table(self):
        """Update the running instances table"""
        self.instances_table.setRowCount(len(self.running_instances))
        
        for row, instance in enumerate(self.running_instances):
            self.instances_table.setItem(row, 0, QTableWidgetItem(instance["pid"]))
            self.instances_table.setItem(row, 1, QTableWidgetItem(instance["version"]))
            self.instances_table.setItem(row, 2, QTableWidgetItem(instance["port"]))
            self.instances_table.setItem(row, 3, QTableWidgetItem(instance["uptime"]))
            
            # Color memory usage based on value
            memory_item = QTableWidgetItem(instance["memory"])
            if int(instance["memory"].replace("MB", "")) > 200:
                memory_item.setForeground(QColor("red"))
            self.instances_table.setItem(row, 4, memory_item)
            
            # Color CPU usage based on value
            cpu_item = QTableWidgetItem(instance["cpu"])
            if int(instance["cpu"].replace("%", "")) > 50:
                cpu_item.setForeground(QColor("red"))
            self.instances_table.setItem(row, 5, cpu_item)
            
            self.instances_table.setItem(row, 6, QTableWidgetItem(instance["tasks"]))
        
        # Update PID combo in logs tab
        self.log_pid_combo.clear()
        self.log_pid_combo.addItems([instance["pid"] for instance in self.running_instances])
        
        # Update running instances count in dashboard
        self.running_instances_label.setText(str(len(self.running_instances)))

    def load_configuration(self):
        """Load configuration for selected version"""
        version = self.config_version_combo.currentText()
        if version:
            # Simulated configuration loading
            config_text = f"""# Configuration for FHIR Guard {version}
server:
  host: 0.0.0.0
  port: 8080
  read_timeout: 30s
  write_timeout: 30s

security:
  tls: enabled
  auth: enabled
  jwt_expiry: 24h

resources:
  max_memory: 1024MB
  max_cpu: 2
  workers: 10

logging:
  level: info
  path: /var/log/fhirguard/{version}.log
"""
            self.config_editor.setPlainText(config_text)

    def save_configuration(self):
        """Save the current configuration"""
        version = self.config_version_combo.currentText()
        if version:
            # In a real application, this would save to the config file
            QMessageBox.information(self, "Configuration Saved", 
                                  f"Configuration for version {version} has been saved.")
            self.status_bar.showMessage(f"Configuration for {version} saved successfully", 3000)

    def refresh_logs(self):
        pid = self.log_pid_combo.currentText()
        if not pid:
            return
        version = None
        for inst in self.running_instances:
            if inst["pid"] == pid:
                version = inst["version"]
                break
        if not version:
            QMessageBox.warning(self, "Unknown PID", "Version not found for selected PID.")
            return
        try:
            app = pathControll.getApps(version)[0]["nome"]
            log_lines = list(monitor.logs(app, version, tail=self.tail_spin.value(), follow=False))
            self.log_viewer.setPlainText("\n".join(log_lines))
        except Exception as e:
            self.log_viewer.setPlainText(f"Error reading logs: {str(e)}")

    def start_instance(self):
        version = self.default_version
        if not version:
            QMessageBox.warning(self, "No Default Version", "Please set a default version before starting an instance.")
            return
        try:
            apps = pathControll.getApps(version)
            if not apps:
                raise Exception("No apps found for this version.")

            jar_name = apps[0]["nome"]  # Pega o primeiro app como teste
            pid = str(start(version, jar_name))

            new_instance = {
                "pid": pid,
                "version": version,
                "port": "unknown",
                "uptime": "0m",
                "memory": "0MB",
                "cpu": "0%",
                "tasks": "0"
            }
            self.running_instances.append(new_instance)
            self.update_instances_table()
            self.logs_preview.append(f"{pid} - Instance started (version {version})")
            QMessageBox.information(self, "Instance Started", f"Instance {pid} started.")
            self.status_bar.showMessage(f"Instance {pid} started", 3000)
        except Exception as e:
            QMessageBox.critical(self, "Start Failed", str(e))

    def stop_instance(self):
        selected_rows = self.instances_table.selectedItems()
        if selected_rows:
            pid = selected_rows[0].text()
            reply = QMessageBox.question(self, "Confirm Stop", f"Stop instance {pid}?", QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                try:
                    stop(int(pid))
                    self.running_instances = [inst for inst in self.running_instances if inst["pid"] != pid]
                    self.update_instances_table()
                    self.logs_preview.append(f"{pid} - Instance stopped")
                    QMessageBox.information(self, "Stopped", f"Instance {pid} stopped.")
                    self.status_bar.showMessage(f"Instance {pid} stopped", 3000)
                except Exception as e:
                    QMessageBox.critical(self, "Stop Failed", str(e))

    def install_version(self):
        """Install the selected version"""
        version = self.version_combo.currentText()
        if version:
            if version in self.installed_versions:
                QMessageBox.information(self, "Already Installed", f"Version {version} is already installed.")
                return
            try:
                for progresso in install(version):
                    self.status_bar.showMessage(f"{progresso['nome']}: {progresso['porcentagem']:.2f}%", 1000)
                self.installed_versions.append(version)
                self.installed_versions.sort(reverse=True)
                self.update_versions_list()
                QMessageBox.information(self, "Installation Complete", f"FHIR Guard {version} installed.")
            except Exception as e:
                QMessageBox.critical(self, "Installation Failed", str(e))

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

                QMessageBox.information(self, "Uninstallation Complete", "All versions have been uninstalled.")
                self.status_bar.showMessage("All versions uninstalled successfully", 3000)

            except Exception as e:
                QMessageBox.critical(self, "Uninstallation Error", str(e))

    def set_default_version(self):
        """Set the selected version as default"""
        selected_items = self.installed_list.selectedItems()
        if selected_items:
            version = selected_items[0].text()
            self.default_version = version  # guarda a versão default
            self.current_version_label.setText(version)
            QMessageBox.information(self, "Default Version Set", 
                                f"FHIR Guard {version} is now the default version.")
            self.status_bar.showMessage(f"Version {version} set as default", 3000)
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

    def view_configuration(self):
        """View configuration for selected version in versions tab"""
        selected_items = self.installed_list.selectedItems()
        if selected_items:
            version = selected_items[0].text()
            self.config_version_combo.setCurrentText(version)
            self.tab_widget.setCurrentIndex(3)  # Switch to Configuration tab
        else:
            QMessageBox.warning(self, "No Selection", "Please select a version to view configuration")

    def update_status(self):
        """Periodically update system status"""
        # Simulate status updates
        if self.running_instances:
            # Update uptime
            for instance in self.running_instances:
                if "uptime" in instance:
                    mins = int(instance["uptime"].replace("m", "").replace("h", ""))
                    if "h" in instance["uptime"]:
                        mins += 5
                        instance["uptime"] = f"{mins//60}h{mins%60}m"
                    else:
                        mins += 1
                        instance["uptime"] = f"{mins}m"
            
            # Random resource fluctuations
            for instance in self.running_instances:
                instance["memory"] = f"{int(instance['memory'].replace('MB', '')) + 5}MB"
                instance["cpu"] = f"{int(instance['cpu'].replace('%', '')) + 1}%"
                if int(instance["memory"].replace("MB", "")) > 1000:
                    instance["memory"] = "128MB"
                if int(instance["cpu"].replace("%", "")) > 50:
                    instance["cpu"] = "5%"
            
            self.update_instances_table()
            
            # Update dashboard metrics
            self.cpu_progress.setValue((self.cpu_progress.value() + 5) % 100)
            self.memory_progress.setValue((self.memory_progress.value() + 3) % 100)


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