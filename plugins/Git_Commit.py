import subprocess
from PyQt5.QtWidgets import QAction, QInputDialog
from plugin_interface import PluginInterface

class VersionControlPlugin(PluginInterface):
    def __init__(self, ide):
        super().__init__(ide)
        self.action_commit = QAction("Git Commit", self.ide)
        self.action_commit.triggered.connect(self.git_commit)
        self.action_push = QAction("Git Push", self.ide)
        self.action_push.triggered.connect(self.git_push)
        self.action_pull = QAction("Git Pull", self.ide)
        self.action_pull.triggered.connect(self.git_pull)
    
    def initialize(self):
        self.ide.add_action_to_menu('Code', self.action_commit)
        self.ide.add_action_to_menu('Code', self.action_push)
        self.ide.add_action_to_menu('Code', self.action_pull)
        self.ide.console_output.appendPlainText("Version Control Plugin aktiviert.")

    def deinitialize(self):
        self.ide.remove_action_from_menu('Code', self.action_commit)
        self.ide.remove_action_from_menu('Code', self.action_push)
        self.ide.remove_action_from_menu('Code', self.action_pull)
        self.ide.console_output.appendPlainText("Version Control Plugin deaktiviert.")
    
    def git_commit(self):
        self.ide.console_output.appendPlainText("Git Commit wird durchgeführt...")
        commit_message, ok = QInputDialog.getText(self.ide, 'Git Commit', 'Commit Message:')
        if ok and commit_message:
            process = subprocess.Popen(["git", "commit", "-am", commit_message], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            self.ide.console_output.appendPlainText(stdout + "\\n" + stderr)
            self.ide.console_output.appendPlainText("Git Commit abgeschlossen.")
    
    def git_push(self):
        self.ide.console_output.appendPlainText("Git Push wird durchgeführt...")
        process = subprocess.Popen(["git", "push"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()
        self.ide.console_output.appendPlainText(stdout + "\\n" + stderr)
        self.ide.console_output.appendPlainText("Git Push abgeschlossen.")
    
    def git_pull(self):
        self.ide.console_output.appendPlainText("Git Pull wird durchgeführt...")
        process = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()
        self.ide.console_output.appendPlainText(stdout + "\\n" + stderr)
        self.ide.console_output.appendPlainText("Git Pull abgeschlossen.")