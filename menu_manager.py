from PyQt5.QtWidgets import QMenuBar, QAction, QMenu, QInputDialog, QListWidgetItem, QTextEdit, QMainWindow
from PyQt5.QtGui import QKeySequence, QColor, QTextFormat, QTextCursor
from PyQt5.QtCore import Qt

import info  # Importiere das info-Modul
import shortcuts  # Importiere das shortcuts-Modul
from file_operations import install_package, update_package, uninstall_package
from process_manager import create_exe
from translator import translate_text



def create_menus(main_window):
    menu_bar = QMenuBar(main_window)
    main_window.setMenuBar(menu_bar)

    menu_bar = main_window.menuBar()
    menu_bar.setStyleSheet("QMenuBar { background-color: #353535; color: #FFFFFF; }")

    code_menu = QMenu('Code', main_window)
    code_menu.setObjectName('Code')
    menu_bar.addMenu(code_menu)

    code_check_menu = QMenu('Code prüfen', main_window)
    code_check_menu.setObjectName('Code prüfen')
    menu_bar.addMenu(code_check_menu)

    error_search_menu = QMenu('Fehler suche', main_window)
    error_search_menu.setObjectName('Fehler suche')
    code_check_menu.addMenu(error_search_menu)

    create_exe_menu = menu_bar.addMenu('Programm erstellen')
    clear_output_menu = menu_bar.addMenu('Konsole')
    info_menu = menu_bar.addMenu('Info')
    library_menu = menu_bar.addMenu('Bibliotheken')
    project_menu = menu_bar.addMenu('Projekt')
    view_menu = menu_bar.addMenu('Ansicht')
    settings_menu = menu_bar.addMenu('Einstellungen')
    main_window.plugin_menu = menu_bar.addMenu('Plugins')
    open_project_menu = project_menu.addMenu('Projekt öffnen')
    new_project_menu = project_menu.addMenu('Projekt erstellen')
    save_file_menu = menu_bar.addMenu('Speichern')

    run_interactive_action = QAction('Interaktives Programm ausführen', main_window)
    lint_action = QAction('Lint Code', main_window)
    lint_action.triggered.connect(main_window.lint_code)
    lint_action.setText('Fehler suche')  # Aktion umbenennen
    git_commit_action = QAction('Git Commit', main_window)
    add_snippet_action = QAction('Snippet hinzufügen', main_window)
    create_exe_action = QAction('erstellen', main_window)
    clear_output_action = QAction('Ausgabe löschen', main_window)
    clear_interactive_console_action = QAction('Interaktive Konsole löschen', main_window)
    translate_action = QAction('Text übersetzen', main_window)
    info_action = QAction('Info', main_window)
    shortcuts_action = QAction('Tastenkürzel', main_window)
    install_package_action = QAction('Neues Paket installieren', main_window)
    update_package_action = QAction('Paket aktualisieren', main_window)
    uninstall_package_action = QAction('Paket deinstallieren', main_window)
    open_project_action = QAction('öffnen', main_window)
    new_project_action = QAction('erstellen', main_window)
    save_file_action = QAction('geladenen code speichern', main_window)
    reset_editor_action = QAction('Editor zurücksetzen', main_window)  # Neue Aktion hinzufügen
    save_layout_action = QAction('Layout speichern')
    open_settings_action = QAction('Einstellungen öffnen', main_window)
    reset_dock_positions_action = QAction('Dock-Positionen zurücksetzen', main_window)
    
    toggle_project_files_action = main_window.project_files_dock.toggleViewAction()
    toggle_code_editor_action = main_window.code_editor_dock.toggleViewAction()
    toggle_terminal_action = main_window.console_output_dock.toggleViewAction()
    toggle_todo_list_action = main_window.todo_list_dock.toggleViewAction()
    toggle_interactive_console_action = main_window.interactive_console_dock.toggleViewAction()
    toggle_error_list_action = main_window.error_dock.toggleViewAction()  # Aktion für die Fehlerliste

    code_menu.addAction(run_interactive_action)
    code_menu.addAction(git_commit_action)
    code_menu.addAction(add_snippet_action)
    create_exe_menu.addAction(create_exe_action)
    clear_output_menu.addAction(clear_output_action)
    clear_output_menu.addAction(clear_interactive_console_action)
    info_menu.addAction(info_action)
    info_menu.addAction(shortcuts_action)
    info_menu.addAction(translate_action)
    library_menu.addAction(install_package_action)
    library_menu.addAction(update_package_action)
    library_menu.addAction(uninstall_package_action)
    open_project_menu.addAction(open_project_action)
    new_project_menu.addAction(new_project_action)
    save_file_menu.addAction(save_file_action)
    project_menu.addAction(reset_editor_action)  # Neue Aktion zum Menü hinzufügen
    view_menu.addAction(toggle_project_files_action)
    view_menu.addAction(toggle_code_editor_action)
    view_menu.addAction(toggle_terminal_action)
    view_menu.addAction(toggle_todo_list_action)
    view_menu.addAction(toggle_interactive_console_action)
    view_menu.addAction(toggle_error_list_action)  # Aktion zur Ansicht hinzufügen
    view_menu.addAction(reset_dock_positions_action)
    settings_menu.addAction(save_layout_action)
    settings_menu.addAction(open_settings_action)

    run_interactive_action.triggered.connect(main_window.interactive_console.run_interactive_script)
    git_commit_action.triggered.connect(main_window.git_commit)
    add_snippet_action.triggered.connect(main_window.add_snippet)
    create_exe_action.triggered.connect(lambda: create_exe(main_window))
    clear_output_action.triggered.connect(main_window.clear_output)
    clear_interactive_console_action.triggered.connect(main_window.clear_interactive_console)
    translate_action.triggered.connect(main_window.translate_selected_text)
    info_action.triggered.connect(info.show_info)
    shortcuts_action.triggered.connect(shortcuts.show_shortcuts)
    install_package_action.triggered.connect(lambda: install_package(main_window))
    update_package_action.triggered.connect(lambda: update_package(main_window))
    uninstall_package_action.triggered.connect(lambda: uninstall_package(main_window))
    open_project_action.triggered.connect(main_window.open_project)
    new_project_action.triggered.connect(main_window.new_project)
    save_file_action.triggered.connect(main_window.save_file)
    reset_editor_action.triggered.connect(main_window.reset_editor)  # Verbindung zur Aktion hinzufügen
    save_layout_action.triggered.connect(main_window.save_settings)
    open_settings_action.triggered.connect(main_window.open_settings_dialog)
    reset_dock_positions_action.triggered.connect(main_window.reset_dock_positions)

    # Add shortcuts for actions
    run_interactive_action.setShortcut('Ctrl+I')
    git_commit_action.setShortcut('Ctrl+Shift+C')
    add_snippet_action.setShortcut('Ctrl+Shift+N')
    clear_output_action.setShortcut('Ctrl+L')
    clear_interactive_console_action.setShortcut('Ctrl+Shift+L')
    open_project_action.setShortcut('Ctrl+O')
    new_project_action.setShortcut('Ctrl+N')
    save_file_action.setShortcut('Ctrl+S')
    info_action.setShortcut('Ctrl+H')
    shortcuts_action.setShortcut('Ctrl+K')
    translate_action.setShortcut('Ctrl+Shift+T')
    toggle_project_files_action.setShortcut('Ctrl+T')
    save_layout_action.setShortcut('Ctrl+Shift+S')

    # Shortcuts for navigating errors
    next_error_action = QAction('Nächsten Fehler anzeigen', main_window)
    next_error_action.setShortcut(QKeySequence('Ctrl+E'))
    next_error_action.triggered.connect(main_window.goto_next_error)
    error_search_menu.addAction(lint_action)
    error_search_menu.addAction(next_error_action)

def create_plugin_actions(main_window):
    plugins = main_window.plugin_manager.get_plugins()
    for plugin_name, plugin_instance in plugins:
        action = QAction(f"{plugin_name} aktivieren/deaktivieren", main_window)
        action.setCheckable(True)
        action.setChecked(main_window.plugin_manager.is_plugin_active(plugin_name))
        action.toggled.connect(lambda checked, name=plugin_name: main_window.plugin_manager.toggle_plugin(name))
        main_window.plugin_menu.addAction(action)
