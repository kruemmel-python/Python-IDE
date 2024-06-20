from plugin_interface import PluginInterface
from PyQt5.QtWidgets import QDockWidget, QPlainTextEdit, QAction, QMenu
from PyQt5.QtCore import Qt
import cProfile
import pstats
import io

class ProfilingPlugin(PluginInterface):
    def initialize(self):
        self.console_output = QPlainTextEdit(self.ide)
        self.console_output.setReadOnly(True)

        self.dock_widget = QDockWidget("Profiling Results", self.ide)
        self.dock_widget.setWidget(self.console_output)
        self.ide.addDockWidget(Qt.BottomDockWidgetArea, self.dock_widget)

        self.profiling_action = QAction("Profiling starten", self.ide)
        self.profiling_action.triggered.connect(self.run_profiling)
        self.ide.add_action_to_menu('Code', self.profiling_action)

        self.ide.console_output.appendPlainText("Profiling Plugin aktiviert")

    def deinitialize(self):
        self.ide.removeDockWidget(self.dock_widget)
        self.ide.remove_action_from_menu('Code', self.profiling_action)
        self.ide.console_output.appendPlainText("Profiling Plugin deaktiviert")

    def run_profiling(self):
        code = self.ide.code_editor.toPlainText()
        profile = cProfile.Profile()
        profile.enable()
        exec(code, globals())
        profile.disable()

        s = io.StringIO()
        ps = pstats.Stats(profile, stream=s).sort_stats(pstats.SortKey.CUMULATIVE)
        ps.print_stats()
        self.console_output.setPlainText(s.getvalue())

def create_plugin(ide):
    return ProfilingPlugin(ide)
