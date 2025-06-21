# OS 
import os
import sys
import subprocess
import random
import shutil
import json  
import datetime 

from send2trash import send2trash
from pathlib import Path

# Image stuff
import cv2
import numpy as np
from pygame import mixer


# PyQT 
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt, QEvent, QItemSelectionModel
from PyQt5 import QtGui
from PyQt5.QtGui import QColor
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import *
import sip

# App 
from main_window import Ui_MainWindow
from session_display import Ui_session_display
import resources_config_rc 




class MainApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None, show_main_window=False):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('Reference practice - Inkdrawing')
        self.session_schedule = {}

        self.valid_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.tiff','.jfif', '.bmp'}

        # Install event filter
        self.installEventFilter(self)
        
        # Disable tab focus for all widgets
        for widget in self.findChildren(QtWidgets.QWidget):
            widget.setFocusPolicy(QtCore.Qt.ClickFocus)


        # Initialize label dictionaries
        self.labels_color_dictionary = {"Default": "#00000000"}
        self.preset_labels_dictionary = {}


        # Define default shortcuts
        self.default_shortcuts = {
            "main_window": {
                "start": "S", 
                "close": "Escape",
                "cycle_label": "\u00b2"
            },
            "session_window": {
                "toggle_resize": "R",
                "rotate_right": "Q",
                "rotate_left": "F",
                "always_on_top": "A",
                "flip_horizontal": "H",
                "flip_vertical": "V",
                "prev_image": "Left",
                "pause_timer": "Space",
                "close": "Escape",
                "next_image": "Right",
                "open_folder": "O",
                "copy_path": "Ctrl+C",
                "delete_image": "Ctrl+D",
                "grayscale": "T",
                "grid_settings": "Ctrl+G",
                "toggle_grid": "G",
                "zoom_in": "S",
                "zoom_out": "D",
                "zoom_in_numpad": "+",
                "zoom_out_numpad": "-",
                "show_main_window": "Tab",
                "mute": "M",
                "add_30_seconds": "Up",
                "add_60_seconds": "Ctrl+Up",
                "restart_timer": "Ctrl+Shift+Up"
            }
        }




        # Use the executable's directory for absolute paths 
        if getattr(sys, 'frozen', False):  # Check if the application is frozen (compiled as an EXE)
            self.base_dir = os.path.dirname(sys.executable)
            self.temp_dir = sys._MEIPASS
        else:
            self.base_dir = os.path.dirname(os.path.abspath(__file__))
            self.temp_dir = None




        self.presets_dir = os.path.join(self.base_dir, 'drawing_presets')
        self.images_presets_dir = os.path.join(self.presets_dir, 'images_presets')
        self.session_presets_dir = os.path.join(self.presets_dir, 'session_presets')
        self.theme_presets_dir = os.path.join(self.presets_dir, 'theme_presets') 
        self.default_themes_dir = os.path.join(self.base_dir,'default_themes')  


        self.rainmeter_presets_dir = os.path.join(self.presets_dir,'rainmeter_presets')  
        self.rainmeter_files_dir = os.path.join(self.base_dir,'rainmeter_files')  
        self.rainmeter_deleted_files_dir = os.path.join(self.rainmeter_presets_dir,'Deleted Files') 

        
        self.default_themes = ['default_theme.txt','dark_theme.txt', 'light_theme.txt']
        self.current_theme = "default_theme.txt"

        print('------------------')
        print(' Base Directory:', self.base_dir)
        print(' Temporary Directory:', self.temp_dir)
        print(' Default Themes Directory:', self.default_themes_dir)
        print(' Theme Presets Directory:', self.theme_presets_dir)
        
        print(' Rainmeter Presets Directory:', self.rainmeter_presets_dir)
        print(' Rainmeter Files Directory:', self.rainmeter_files_dir)
        print(' Rainmeter Deleted Files Directory:', self.rainmeter_deleted_files_dir)

        print('------------------')


        self.create_directories()
        self.ensure_default_themes()

        
        # Initialize the randomize_settings variable or False depending on your default
        self.randomize_settings = True  
        self.auto_start_settings = False

        # Initialize cache variables
        self.image_names_cache = []
        self.session_names_cache = []


        self.table_images_selection.setItem(0, 0, QTableWidgetItem('112'))

        # Enable sorting on table headers
        self.table_images_selection.setSortingEnabled(True)
        self.table_session_selection.setSortingEnabled(True)


        # Alternative method (ensures interactivity)
        self.table_images_selection.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
        self.table_session_selection.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Interactive)




        

        self.schedule = []
        self.total_time = 0
        self.total_images = 0
        self.selection = {'folders': [], 'files': []}


        # Load session settings at startup
        self.load_session_settings()
        self.init_buttons()
        self.apply_shortcuts_main_window()

        

        # Hide the main window initially
        #self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)


        self.display = None  # Initialize with None
        # Automatically start the session if auto_start is True
        if self.auto_start_settings:
            self.start_session_from_files()

        # Show the main window if show_main_window is True
        elif show_main_window == True:
            self.show()

        # Initialize position for dragging
        self.oldPos = self.pos()
        self.init_styles()
        self.load_presets()

        
        
    def init_message_boxes(self):
        """Initialize custom message box settings."""
        self.message_box = QtWidgets.QMessageBox(self)
        self.message_box.setIcon(QtWidgets.QMessageBox.NoIcon)  # Set to no icon by default
    
    def show_info_message(self, title, message):

        self.message_box.setWindowTitle(title)
        self.message_box.setText(message)
        self.message_box.exec_()




    def ensure_default_themes(self):
        """Ensure default theme files are present in theme_presets_dir and replace any missing or corrupted files."""

        self.current_theme = 'default_theme.txt'
        # Determine the base directory based on whether the app is running as a PyInstaller bundle
        if getattr(sys, 'frozen', False):
            temp_dir = sys._MEIPASS
            self.base_dir = os.path.dirname(sys.executable)
            self.default_themes_dir = os.path.join(temp_dir, 'default_themes')
        else:
            self.base_dir = os.path.dirname(os.path.abspath(__file__))
            self.default_themes_dir = os.path.join(self.base_dir, 'default_themes')

        # Ensure the theme presets directory exists
        os.makedirs(self.theme_presets_dir, exist_ok=True)

        for theme_file in self.default_themes:
            source_file = os.path.join(self.default_themes_dir, theme_file)
            destination_file = os.path.join(self.theme_presets_dir, theme_file)

            # If the destination file does not exist, or it's corrupted, replace it with the default theme
            if not os.path.exists(destination_file):
                self.copy_theme_file(source_file, destination_file)
            else:
                try:
                    # Check if the existing file is readable and not corrupted
                    with open(destination_file, 'r') as dst:
                        content = dst.read()
                        if not content.strip():
                            print(f"{theme_file} is empty or corrupted. Replacing with default.")
                            self.copy_theme_file(source_file, destination_file)
                except Exception as e:
                    print(f"Error reading {theme_file}: {e}. Replacing with default.")
                    self.copy_theme_file(source_file, destination_file)

    def copy_theme_file(self, source_file, destination_file):
        """Copy a theme file from source to destination."""
        if os.path.exists(source_file):
            try:
                with open(source_file, 'r') as src:
                    content = src.read()

                with open(destination_file, 'w') as dst:
                    dst.write(content)

                print(f"Copied {source_file} to {destination_file}")
            except Exception as e:
                print(f"Error copying {source_file} to {destination_file}: {e}")
        else:
            print(f"Source theme file {source_file} does not exist.")


    def reset_default_themes(self):
        """Replace corrupted or missing theme files in theme_presets_dir with default ones."""

        self.current_theme = 'default_theme.txt'
        # Determine the base directory based on whether the app is running as a PyInstaller bundle
        if getattr(sys, 'frozen', False):
            temp_dir = sys._MEIPASS
            self.base_dir = self.base_dir = os.path.dirname(sys.executable)
            self.default_themes_dir = os.path.join(temp_dir, 'default_themes')
        else:
            self.base_dir = os.path.dirname(os.path.abspath(__file__))
            self.default_themes_dir = os.path.join(self.base_dir, 'default_themes')


        for theme_file in self.default_themes:
            source_file = os.path.join(self.default_themes_dir, theme_file)
            destination_file = os.path.join(self.theme_presets_dir, theme_file)
            
            # Remove the existing file if it exists
            if os.path.exists(destination_file):
                os.remove(destination_file)
            
            # Read from the source file and write to the destination file
            if os.path.exists(source_file):
                try:
                    with open(source_file, 'r') as src:
                        content = src.read()

                    with open(destination_file, 'w') as dst:
                        dst.write(content)

                    print(f"THEME RESTAURED : Replaced {theme_file} in {self.theme_presets_dir}")
                    self.init_styles()
                    

                except Exception as e:
                    print(f"Error copying {theme_file}: {e}")
            else:
                print(f"Source theme file {source_file} does not exist.")
        self.show_info_message( 'Invalid theme', f'Invalid theme file, theme restaured to default.')






    def showEvent(self, event):
        """Override showEvent to control window visibility."""
        if not self.isVisible():
            event.ignore()  # Ignore the event to keep the window hidden
        else:
            super().showEvent(event)  # Otherwise, handle normally

    def init_buttons(self):
        # Buttons for selection
        self.add_folders_button.clicked.connect(self.create_preset)
        self.delete_images_preset.clicked.connect(self.delete_images_files)
        
        # Buttons for preset
        self.save_session_presets_button.clicked.connect(self.save_session_presets) 
        self.delete_session_preset.clicked.connect(self.delete_presets_files)

        self.open_preset_button.clicked.connect(self.open_preset)

        self.update_preset_button.clicked.connect(self.update_preset) 


        # Buttons for rainmeter
        self.rainmeter_preset_button.clicked.connect(self.create_rainmeter_preset) 

        # Start session button with tooltip
        self.start_session_button.clicked.connect(self.start_session_launcher)
        self.start_session_button.setToolTip(f"[{self.shortcut_settings['main_window']['start']}] Start the session.")

        # Close window button with tooltip
        self.close_window_button.clicked.connect(self.save_session_settings)
        self.close_window_button.clicked.connect(self.close)
        self.close_window_button.setToolTip(f"[{self.shortcut_settings['main_window']['close']}] Close the setting window.")

        # Toggles
        self.randomize_toggle.stateChanged.connect(self.update_randomize_settings)
        self.auto_start_toggle.stateChanged.connect(self.update_auto_start_settings)

        # Table selection handlers
        #self.table_images_selection.itemChanged.connect(self.rename_presets)
        #self.table_session_selection.itemChanged.connect(self.rename_presets)

        self.table_images_selection.itemSelectionChanged.connect(self.update_selection_cache)
        self.table_session_selection.itemSelectionChanged.connect(self.update_selection_cache)


        self.table_images_selection.itemChanged.connect(self.handle_preset_rename)
        self.table_session_selection.itemChanged.connect(self.handle_preset_rename)

        # Track editing state to prevent duplicate signals
        self.currently_editing = False
        self.current_edited_item = None

        # Connect itemDoubleClicked to start tracking edits
        self.table_images_selection.itemDoubleClicked.connect(self.start_edit_tracking)
        self.table_session_selection.itemDoubleClicked.connect(self.start_edit_tracking)
        


        # Theme selector button
        self.theme_options_button.clicked.connect(self.open_theme_selector)


        # Preset search
        self.search_preset.textChanged.connect(self.filter_presets)

        # Connect label options button
        self.labels_options_button.clicked.connect(self.open_label_manager)



        # Add context menu to table_images_selection
        self.table_images_selection.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table_images_selection.customContextMenuRequested.connect(self.show_image_context_menu)





    def show_image_context_menu(self, position):
        """Show context menu for the image table with direct label assignment options."""
        selected_row = self.table_images_selection.currentRow()
        if selected_row < 0:
            return
            
        file_item = self.table_images_selection.item(selected_row, 1)  # Name column
        if not file_item:
            return
            
        filename = file_item.text() + ".txt"
        
        context_menu = QMenu(self)
        
        # Add label options directly to the context menu
        for label_name, color in sorted(self.labels_color_dictionary.items()):
            action = context_menu.addAction(label_name)
            pixmap = QtGui.QPixmap(16, 16)
            pixmap.fill(QColor(color))
            action.setIcon(QtGui.QIcon(pixmap))
            
            # Check the current label
            current_label = self.preset_labels_dictionary.get(filename, "Default")
            if label_name == current_label:
                action.setCheckable(True)
                action.setChecked(True)
                
            # Connect the action
            action.triggered.connect(lambda checked, ln=label_name: self.assign_label(filename, ln))
            
        # Show the menu
        context_menu.exec_(self.table_images_selection.viewport().mapToGlobal(position))


    def assign_label(self, filename, label_name):
        """Assign a label to a preset file."""
        self.preset_labels_dictionary[filename] = label_name
        self.save_session_settings()
        
        # Update the UI
        selected_row = self.table_images_selection.currentRow()
        if selected_row >= 0:
            color_item = self.table_images_selection.item(selected_row, 0)
            if color_item:
                color = self.labels_color_dictionary.get(label_name, "#00000000")
                color_item.setBackground(QColor(color))
                color_item.setToolTip(label_name)
        self.load_presets()



    def start_edit_tracking(self, item):
        """Called when double-clicking to edit an item"""
        self.currently_editing = True
        self.current_edited_item = item
        self.original_text = item.text()  # Store original value

    def eventFilter(self, source, event):
        """Handle Return/Enter key press during editing"""
        if (event.type() == QtCore.QEvent.KeyPress and
            event.key() in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter) and
            source.state() == QtWidgets.QAbstractItemView.EditingState):
            
            # Force close the editor
            source.closePersistentEditor(source.currentItem())
            return True  # Event handled
        
        return super().eventFilter(source, event)


    def handle_preset_rename(self, item):
        """Handle the actual renaming after edit completes"""
        if not self.currently_editing or item != self.current_edited_item:
            return
        
        # Store these values before potentially modifying state
        was_editing = self.currently_editing
        original_text = self.original_text
        
        # Reset editing state BEFORE making changes
        self.currently_editing = False
        self.current_edited_item = None
        
        # Only proceed if text actually changed
        if item.text() != original_text:
            if self.sender() == self.table_images_selection or self.sender() == self.table_session_selection:
                # Pass success/failure back from rename_presets
                success = self.rename_presets(item)
                if not success:
                    # Set the text back to original without triggering events
                    self.blockSignals(True)
                    item.setText(original_text)
                    self.blockSignals(False)



    def init_styles(self, dialog=None, dialog_grid=None, session=None):
        """
        Initialize custom styles for various UI elements including buttons, spin boxes,
        table widgets, checkboxes, dialogs, and the main window. Optionally apply styles
        to a specific dialog or session window.
        """

        # Load the selected theme file
        selected_theme_path = os.path.join(self.theme_presets_dir, self.current_theme)
        if selected_theme_path:
            try:
                with open(selected_theme_path, 'r') as f:
                    theme_styles = f.read()
            except FileNotFoundError:
                print("No theme selected or theme file not found. Applying default styles.")
                self.ensure_default_themes()
                return

            try:
                # Parse theme styles as JSON
                styles_dict = json.loads(theme_styles)

                # Apply styles to each element based on the keys in the theme file
                for element_group, element_styles in styles_dict.items():
                    # Split group of elements (comma-separated)
                    element_names = [name.strip() for name in element_group.split(',')]

                    for element_name in element_names:
                        if hasattr(self, element_name):
                            element = getattr(self, element_name)
                            style_sheet = ""
                            for selector, style in element_styles.items():
                                style_sheet += f"{selector} {{{style}}}\n"
                            element.setStyleSheet(style_sheet)

                        elif element_name == "MainWindow":
                            # Apply style directly to the MainWindow
                            style_sheet = ""
                            for selector, style in element_styles.items():
                                if selector == "window_icon":
                                    if self.temp_dir : 
                                        file_path = os.path.join(self.temp_dir, style)
                                    else: 
                                        file_path = os.path.join(self.base_dir, style)
                                        print(file_path)
                                    self.setWindowIcon(QtGui.QIcon(file_path))
                                elif selector == "icon":
                                    if self.temp_dir : 
                                        file_path = os.path.join(self.temp_dir, style)
                                    else: 
                                        file_path = os.path.join(self.base_dir, style)
                                    self.label.setText(f"<html><head/><body><p><img src=\"{file_path}\"/></p></body></html>")
                                else:
                                    style_sheet += f"{selector} {{{style}}}\n"

                            self.setStyleSheet(style_sheet)
                            self.init_message_boxes()

      


                        elif dialog and element_name == "dialog_styles":
                            # Apply styles to the dialog if it matches the name in the theme file
                            style_sheet = ""
                            style_sheet_header = ""
                            for selector, style in element_styles.items():
                                
                                if selector == "QHeaderView::section":
                                    style_sheet_header += f"{selector} {{{style}}}\n"
                                else:

                                    style_sheet += f"{selector} {{{style}}}\n"
                            dialog.setStyleSheet(style_sheet)
                            if isinstance(dialog, LabelManagerDialog):
                                dialog.label_list.horizontalHeader().setStyleSheet(style_sheet_header)

                        elif "dictionary_controls" in styles_dict and dialog and isinstance(dialog, MultiFolderSelector):
                            style_dict = styles_dict["dictionary_controls"]

                        elif dialog_grid and element_name == "GridSettingsDialog":
                            # Apply styles specifically to GridSettingsDialog
                            style_sheet = ""
                            for selector, style in element_styles.items():
                                style_sheet += f"{selector} {{{style}}}\n"
                            dialog_grid.setStyleSheet(style_sheet)

                        elif session and element_name == "session_display":
                            # Apply style to session_display if it matches the name in the theme file
                            style_sheet = ""
                            for selector, style in element_styles.items():
                                if selector == "window_icon":
                                    if self.temp_dir : 
                                        file_path = os.path.join(self.temp_dir, style)
                                    else: 
                                        file_path = os.path.join(self.base_dir, style)
                                    session.setWindowIcon(QtGui.QIcon(file_path))

                                style_sheet += f"{style}\n"
                            session.setStyleSheet(style_sheet)

                            if "background:" not in session.styleSheet():
                                print('No background color')
                                session.setStyleSheet("background: rgb(0,0,0)")




                        elif session and element_name == "text_display":
                            # Apply style to text_display if it matches the name in the theme file
                            style_sheet = ""
                            for selector, style in element_styles.items():
                                if selector == "highlight_names":
                                    session.highlight_names_settings=style
                                elif selector == "highlight_keywords":   
                                    session.highlight_keywords_settings=style
                                elif selector == "always_on_top_border":   
                                    session.always_on_top_borde_settings=style
                                else:
                                    style_sheet += f"{selector} {{{style}}}\n"
                                if hasattr(session, 'text_display'):
                                    session.text_display.setStyleSheet(style_sheet)

                        elif session and element_name == "session_display_labels":
                            session_display_label_styles = styles_dict["session_display_labels"]
                            for label_name in ["session_info", "timer_display"]:
                                if hasattr(session, label_name):
                                    label = getattr(session, label_name)
                                    style_sheet = ""
                                    for selector, style in session_display_label_styles.items():
                                        style_sheet += f"{selector} {{{style}}}\n"
                                    label.setStyleSheet(style_sheet)

                # Apply font settings to session labels only if specified
                if session and "label_fonts" in styles_dict:
                    font_settings = styles_dict["label_fonts"]
                    font = QtGui.QFont()
                    font.setFamily(font_settings.get("family", "Arial"))
                    font.setPointSize(font_settings.get("size", 10))
                    font.setBold(font_settings.get("bold", False))
                    font.setItalic(font_settings.get("italic", False))
                    font.setWeight(font_settings.get("weight", 50))

                    # Apply font only to session labels
                    for label_name in ["session_info", "timer_display"]:
                        if hasattr(session, label_name):
                            label = getattr(session, label_name)
                            label.setFont(font)

                # Apply common button styles to QPushButton widgets
                if "common_button_styles" in styles_dict:
                    button_styles = styles_dict["common_button_styles"]
                    for button_name in ["theme_options_button","labels_options_button", "add_folders_button", "delete_images_preset", "open_preset_button","update_preset_button","rainmeter_preset_button",
                                        "delete_session_preset", "save_session_presets_button", "start_session_button", "close_window_button"]:
                        if hasattr(self, button_name):
                            button = getattr(self, button_name)
                            style_sheet = ""
                            for selector, style in button_styles.items():
                                style_sheet += f"{selector} {{{style}}}\n"
                            button.setStyleSheet(style_sheet)

                # Apply styles to other elements if needed
                if "labels" in styles_dict:
                    label_styles = styles_dict["labels"]
                    for label_name in ["select_images", "label_7", "image_amount_label", "duration_label", "label_5", "label_6"]:
                        if hasattr(self, label_name):
                            label = getattr(self, label_name)
                            style_sheet = ""
                            for selector, style in label_styles.items():
                                style_sheet += f"{selector} {{{style}}}\n"
                            label.setStyleSheet(style_sheet)

                if "common_spinbox_styles" in styles_dict:
                    spinbox_styles = styles_dict["common_spinbox_styles"]
                    for spinbox_name in ["set_seconds", "set_number_of_images", "set_minutes"]:
                        if hasattr(self, spinbox_name):
                            spinbox = getattr(self, spinbox_name)
                            style_sheet = ""
                            for selector, style in spinbox_styles.items():
                                style_sheet += f"{selector} {{{style}}}\n"
                            spinbox.setStyleSheet(style_sheet)

                if "common_checkbox_styles" in styles_dict:
                    checkbox_styles = styles_dict["common_checkbox_styles"]
                    style_sheet = ""
                    for selector, style in checkbox_styles.items():
                        style_sheet += f"{selector} {{{style}}}\n"
                    # Assuming self has checkboxes that need styling
                    for checkbox_name in ["auto_start_toggle", "randomize_toggle"]:
                        if hasattr(self, checkbox_name):
                            checkbox = getattr(self, checkbox_name)
                            checkbox.setStyleSheet(style_sheet)

                if session and "session_buttons" in styles_dict:
                    button_styles = styles_dict["session_buttons"]
                    button_names = [
                        "grid_button", "grayscale_button", "lock_scale_button",
                        "flip_horizontal_button", "flip_vertical_button",
                        "previous_image", "pause_timer", "stop_session",
                        "next_image", "copy_image_path_button",
                        "open_folder_button","delete_image_button","show_main_window_button"
                    ]
                    for button_name in button_names:
                        if hasattr(session, button_name):
                            button = getattr(session, button_name)
                            style_sheet = ""
                            for selector, style in button_styles.items():
                                style_sheet += f"{selector} {{{style}}}\n"
                            button.setStyleSheet(style_sheet)

            except json.JSONDecodeError:
                print("Error parsing theme file. Applying default styles.")
                self.reset_default_themes()
        else:
            print("No theme selected or theme file not found. Applying default styles.")
            self.reset_default_themes()



    def update_selection_cache(self):
        """Update the selected filename cache based on current table selections."""
        # Only proceed if signals aren't blocked
        if not self.table_images_selection.signalsBlocked() and not self.table_session_selection.signalsBlocked():
            # print("-- updating cache --")
            # Track image selection by filename
            selected_row = self.table_images_selection.currentRow()
            if selected_row >= 0:
                name_item = self.table_images_selection.item(selected_row, 1)  # Name column
                if name_item:
                    # Store both filename and row number
                    self.selected_image_filename = name_item.text() + ".txt"
                    self.selected_image_row = selected_row

            # Track session selection by filename
            selected_row = self.table_session_selection.currentRow()
            if selected_row >= 0:
                name_item = self.table_session_selection.item(selected_row, 0)  # Name column
                if name_item:
                    # Store both filename and row number
                    self.selected_session_filename = name_item.text() + ".txt"
                    self.selected_session_row = selected_row

    def filter_presets(self):
        """Filter table_images_selection based on search_preset input."""
        search_text = self.search_preset.text().strip().lower()
        
        for row in range(self.table_images_selection.rowCount()):
            item = self.table_images_selection.item(row, 1)  # Assuming filenames are in column 1
            if item:
                filename = item.text().lower()
                self.table_images_selection.setRowHidden(row, search_text not in filename)



    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Tab:
            # Custom Tab key handling
            if self.search_preset.hasFocus():
                # Clear focus from all widgets
                focused_widget = QtWidgets.QApplication.focusWidget()
                if focused_widget:
                    focused_widget.clearFocus()
                
                # Explicitly clear focus for the entire window
                self.clearFocus()
            else:
                # Set focus to search_preset
                self.search_preset.setFocus()
                self.search_preset.selectAll()
            
            # Prevent default Tab behavior
            event.accept()
            return
        
        # Call the parent class's keyPressEvent for other key events
        super().keyPressEvent(event)

    def eventFilter(self, obj, event):
        # Optionally keep your existing event filter logic
        return super().eventFilter(obj, event)


######### PRESET SECTION ######### 

    def create_preset(self, folder_list=None, preset_name=None, output_folder=None, is_gui=True):
        """
        Opens a dialog to select multiple folders or processes a given list of folders.
        For command-line usage, folder_list and preset_name are used directly, and is_gui is set to False.
        """
        self.load_presets()
        
        # Determine the preset name
        if not preset_name:
            preset_name = f'preset_{self.get_next_preset_number()}'
        
        # Use folder_list if provided; otherwise, open the dialog
        if folder_list:
            selected_dirs = folder_list
        else:
            dialog = MultiFolderSelector(self, preset_name)
            self.init_styles(dialog=dialog)
            if dialog.exec_() == QtWidgets.QDialog.Accepted:
                selected_dirs = dialog.get_selected_folders()
                preset_name = dialog.get_preset_name()  # Retrieve the preset name from dialog
                
                # Only show "No Selection" message if accepted with no selection
                if not selected_dirs:
                    if is_gui:
                        self.show_info_message('No Selection', 'No folders were selected.')
                    else:
                        print('No folders were selected.')
                    return
            else:
                # Dialog was canceled, just return without showing message
                return

        # Check if we have folders to process (for non-dialog case)
        if not selected_dirs:
            if is_gui:
                self.show_info_message('No Selection', 'No folders were selected.')
            else:
                print('No folders were selected.')
            return

        all_files = set()
        # Collect image files from the specified directories
        for directory in selected_dirs:
            try:
                for file in os.listdir(directory):
                    file_path = os.path.join(directory, file)
                    if os.path.isfile(file_path):  # Check if it's a file
                        all_files.add(file_path)
            except PermissionError:
                if is_gui:
                    self.show_info_message('Permission Error', f'Access denied to folder: {directory}')
                else:
                    print(f'Access denied to folder: {directory}')

        # Validate files
        checked_files = self.check_files(all_files)
        
        # Determine the output folder
        target_folder = output_folder if output_folder else self.images_presets_dir
        os.makedirs(target_folder, exist_ok=True)
        
        # Write valid file paths to the preset file
        preset_filename = os.path.join(target_folder, f'{preset_name}.txt')
        with open(preset_filename, 'w', encoding='utf-8') as f:
            for file_path in sorted(checked_files['valid_files']):
                formatted_path = os.path.normpath(file_path)  # Normalize to platform-specific path separators
                f.write(f'{formatted_path}\n')
        
        # Notify the user
        valid_count = len(checked_files["valid_files"])
        invalid_count = len(checked_files["invalid_files"])
        
        if is_gui:
            if invalid_count:
                self.show_info_message(
                    'Files Processed',
                    f'{preset_name} : {valid_count} file(s) added.\n'
                    f'{invalid_count} file(s) not added. '
                    f'Supported file types: {", ".join(self.valid_extensions)}.'
                )
            else:
                self.show_info_message(
                    'Success', f'{preset_name} : {valid_count} file(s) saved to {preset_filename}'
                )
            # Reload presets
            self.load_presets()
        else:
            # Print output for command-line usage
            print(f'Preset "{preset_name}" created with {valid_count} valid file(s) and saved to {preset_filename}.')
            if invalid_count:
                print(f'{invalid_count} invalid file(s) were not added. Supported file types: {", ".join(self.valid_extensions)}.')

    def get_next_preset_number(self):
        preset_files = [f for f in os.listdir(self.images_presets_dir) if f.startswith('preset_') and f.endswith('.txt')]
        existing_numbers = [int(f[len('preset_'):-len('.txt')]) for f in preset_files if f[len('preset_'):-len('.txt')].isdigit()]
        return max(existing_numbers, default=0) + 1

    def check_files(self, all_files):
        """
        Validate the collected files based on valid extensions.
        """
        valid_files = set()
        invalid_files = set()

        for file in all_files:
            if os.path.splitext(file)[1].lower() in self.valid_extensions:
                valid_files.add(file)
            else:
                invalid_files.add(file)
        
        return {'valid_files': valid_files, 'invalid_files': invalid_files}



    def create_directories(self):
        # Create the directories if they do not exist
        os.makedirs(self.presets_dir, exist_ok=True)
        os.makedirs(self.images_presets_dir, exist_ok=True)
        os.makedirs(self.session_presets_dir, exist_ok=True)
        os.makedirs(self.theme_presets_dir, exist_ok=True)  # Create the theme presets directory

        os.makedirs(self.rainmeter_presets_dir, exist_ok=True)  # Create the theme presets directory
        os.makedirs(self.rainmeter_deleted_files_dir, exist_ok=True)  # Create the theme presets directory



        print(f"Created directories: {self.presets_dir}, {self.images_presets_dir}, {self.session_presets_dir}, {self.theme_presets_dir}, {self.rainmeter_presets_dir}, {self.rainmeter_deleted_files_dir}")


    def save_session_presets(self):
        """Saves session details into a separate text file for each session."""
        print("--- Saving session preset ---")
        number_of_images = self.set_number_of_images.value()
        minutes = self.set_minutes.value()
        seconds = self.set_seconds.value()

        # Validate that number_of_images and duration are greater than 0
        if number_of_images <= 0 or (minutes <= 0 and seconds <= 0):
            self.show_info_message( 'Invalid Input', 'Number of images and duration must be greater than 0.')
            return

        # Create dictionary with session details
        session_data = {
            "session_name": "Session_1",  # Placeholder for session name, replace as needed
            "total_images": number_of_images,
            "time": f"{minutes}m {seconds}s"
        }


        # Check for existing preset files to determine the next available number
        files = os.listdir(self.session_presets_dir)
        preset_files = [f for f in files if f.startswith('session_presets_') and f.endswith('.txt')]
        
        # Extract numbers from filenames
        existing_numbers = []
        for filename in preset_files:
            try:
                number = int(filename.split('_')[-1].split('.')[0])
                existing_numbers.append(number)
            except ValueError:
                continue
        
        # Determine the next available number
        next_number = 1
        if existing_numbers:
            next_number = max(existing_numbers) + 1

        # Create the filename using the next available number
        session_preset_file = os.path.join(self.session_presets_dir, f'session_presets_{next_number}.txt')

        try:
            # Save dictionary to a new file in JSON format
            with open(session_preset_file, 'w') as file:
                json.dump(session_data, file)
            
            # Show success message
            print('Success',
                                                     f"Session Name: {session_data['session_name']}\n"
                                                     f"Total Images: {session_data['total_images']}\n"
                                                     f"Time: {session_data['time']}")

        except Exception as e:
            # Show error message if saving fails
            self.show_info_message('Error', f"Failed to save preset. Error: {str(e)}")

        
        # Save the preset
        self.load_presets()

        # Find the row with the new preset by its name
        preset_name = f'session_presets_{next_number}'  # This matches the name used for saving the preset
        rows = self.table_session_selection.rowCount()
        for row in range(rows):
            item = self.table_session_selection.item(row, 0)  # First column (Name)
            if item and item.text() == preset_name:
                self.table_session_selection.selectRow(row)
                break


    def delete_images_files(self):
        """Deletes the selected preset file by sending it to the Recycle Bin and updates the preset table."""
        # Get the selected row
        selected_row = self.table_images_selection.currentRow()
        
        # Check if a row is actually selected
        if selected_row == -1:
            print('Warning', 'No preset selected for deletion.')
            return
        
        # Get the file name from the name column of the selected row
        file_item = self.table_images_selection.item(selected_row, 1)  # Column index 1 for name
        if not file_item:
            self.show_info_message('Warning', 'No file associated with the selected preset.')
            return
        
        file_name = file_item.text() + ".txt"
        file_path = os.path.join(self.images_presets_dir, file_name)
        
        # Move the file to the Recycle Bin if it exists
        if os.path.exists(file_path):
            try:
                send2trash(file_path)
                # Remove from preset_labels_dictionary if it exists
                if file_name in self.preset_labels_dictionary:
                    del self.preset_labels_dictionary[file_name]
                    self.save_session_settings()  # Save the updated label assignments
            except Exception as e:
                self.show_info_message('Error', f'Failed to send preset to Recycle Bin. Error: {str(e)}')
                return
        else:
            self.show_info_message('Warning', f'File "{file_name}" does not exist.')
        
        # Reload the presets
        self.load_presets()
                
        # After deletion, select the appropriate row if the table isn't empty
        if self.table_images_selection.rowCount() > 0:
            # If we deleted the last row, select the new last row
            if selected_row >= self.table_images_selection.rowCount():
                new_selected_row = self.table_images_selection.rowCount() - 1
            else:
                # Otherwise, select the row at the same position
                new_selected_row = selected_row
            
            self.table_images_selection.selectRow(new_selected_row)
            self.update_selection_cache()

    def open_preset(self):
        """Open the selected preset file in the default text editor."""
        
        # Get the selected row
        selected_row = self.table_images_selection.currentRow()
        
        # Check if a row is actually selected
        if selected_row == -1:
            return

        # Get the file name from the first column of the selected row
        file_item = self.table_images_selection.item(selected_row, 0)
        if not file_item:
            self.show_info_message('Warning', 'No file associated with the selected preset.')
            return

        # Construct the full file name and path
        file_name = file_item.text() + ".txt"
        file_path = os.path.join(self.images_presets_dir, file_name)

        # Open the file if it exists
        if os.path.exists(file_path):
            try:
                # Open the file with the default text editor (Notepad)
                subprocess.Popen(['notepad.exe', file_path])
            except Exception as e:
                self.show_info_message('Error', f'Failed to open preset. Error: {str(e)}')
        else:
            self.show_info_message('Warning', f'File "{file_name}" does not exist.')



    def update_preset(self, preset_path=None, is_gui=True):
        """
        Updates the selected preset or a specified preset path.
        For command-line usage, preset_path is used directly, and is_gui is set to False.
        """
        # Use the provided preset_path or select one from the UI
        if preset_path:
            preset_file_path = preset_path
        else:
            selected_row = self.table_images_selection.currentRow()
            if selected_row == -1:
                if is_gui:
                    self.show_info_message('Warning', 'No preset selected for update.')
                else:
                    print('Warning: No preset selected for update.')
                return
            file_item = self.table_images_selection.item(selected_row, 0)
            if not file_item:
                if is_gui:
                    self.show_info_message('Warning', 'No file associated with the selected preset.')
                else:
                    print('Warning: No file associated with the selected preset.')
                return
            preset_name = file_item.text()
            preset_file_path = os.path.join(self.images_presets_dir, f"{preset_name}.txt")

        if not os.path.exists(preset_file_path):
            if is_gui:
                self.show_info_message('Error', f'Preset file "{preset_file_path}" does not exist.')
            else:
                print(f'Error: Preset file "{preset_file_path}" does not exist.')
            return

        # Read existing file paths
        try:
            with open(preset_file_path, 'r', encoding='utf-8') as f:
                filepaths = [line.strip() for line in f if line.strip()]
        except Exception as e:
            if is_gui:
                self.show_info_message('Error', f"Failed to read preset file. Error: {str(e)}")
            else:
                print(f'Error: Failed to read preset file. Error: {str(e)}')
            return

        # Collect image files from unique directories
        unique_directories = {os.path.dirname(path) for path in filepaths if os.path.exists(os.path.dirname(path))}
        updated_filepaths = set()
        for directory in unique_directories:
            try:
                for file in os.listdir(directory):
                    file_path = os.path.join(directory, file)
                    if os.path.isfile(file_path) and os.path.splitext(file_path)[1].lower() in self.valid_extensions:
                        updated_filepaths.add(file_path)
            except PermissionError:
                if is_gui:
                    self.show_info_message('Permission Error', f'Access denied to folder: {directory}')
                else:
                    print(f'Permission Error: Access denied to folder: {directory}')

        # Write updated file paths back to the preset
        try:
            with open(preset_file_path, 'w', encoding='utf-8') as f:
                for path in sorted(updated_filepaths):
                    f.write(path + '\n')

            if is_gui:
                self.show_info_message('Success', f'Preset "{os.path.basename(preset_file_path)}" updated with {len(updated_filepaths)} images.')
            else:
                print(f'Preset "{os.path.basename(preset_file_path)}" updated with {len(updated_filepaths)} images.')
        except Exception as e:
            if is_gui:
                self.show_info_message('Error', f"Failed to update preset file. Error: {str(e)}")
            else:
                print(f'Error: Failed to update preset file. Error: {str(e)}')

        # Reload presets
        if is_gui:
            self.load_presets()



    def create_rainmeter_preset(self):
        """Create a Rainmeter preset based on the selected image preset."""
        # Get the selected row
        selected_row = self.table_images_selection.currentRow()

        # Check if a row is actually selected
        if selected_row == -1:
            self.show_info_message('Warning', 'No preset selected.')
            return

        # Get the file name from the first column of the selected row
        file_item = self.table_images_selection.item(selected_row, 1)
        if not file_item:
            self.show_info_message('Warning', 'No file associated with the selected preset.')
            return

        # Construct the preset name
        preset_name = file_item.text()
        #preset_folder_name = f"rainmeter_image_{preset_name}"

        # Determine the base directory based on whether the app is running as a PyInstaller bundle
        if getattr(sys, 'frozen', False):
            temp_dir = sys._MEIPASS
            self.rainmeter_files_dir = os.path.join(temp_dir, 'rainmeter_files')
        else:
            self.rainmeter_files_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rainmeter_files')

        # Define the destination path
        destination_folder = os.path.join(self.rainmeter_presets_dir, preset_name)

        # Remove the existing folder if it exists
        if os.path.exists(destination_folder):
            for root, dirs, files in os.walk(destination_folder, topdown=False):
                for file in files:
                    os.remove(os.path.join(root, file))
                for dir in dirs:
                    os.rmdir(os.path.join(root, dir))
            os.rmdir(destination_folder)

        # Create the destination folder
        os.makedirs(destination_folder, exist_ok=True)

        # Define file paths
        ini_file_source = os.path.join(self.rainmeter_files_dir, "IMG_SLIDESHOW.ini")
        lua_file_source = os.path.join(self.rainmeter_files_dir, "IMG_SLIDESHOW.lua")
        ini_file_destination = os.path.join(destination_folder, "IMG_SLIDESHOW.ini")
        lua_file_destination = os.path.join(destination_folder, "IMG_SLIDESHOW.lua")

        try:
            # Copy the Lua file without modifications
            if os.path.exists(lua_file_source):
                with open(lua_file_source, 'rb') as src:
                    with open(lua_file_destination, 'wb') as dst:
                        dst.write(src.read())
            else:
                raise FileNotFoundError(f"Lua file not found at {lua_file_source}")

            # Read and modify the INI file
            if os.path.exists(ini_file_source):
                with open(ini_file_source, "r") as ini_file:
                    ini_content = ini_file.read()

                # Replace placeholders in the INI file
                selected_preset_path = os.path.join(self.images_presets_dir, f"{preset_name}.txt")
                ini_content = ini_content.replace(r'Title = Title', r'Title =' + preset_name)
                ini_content = ini_content.replace(r'ImagePreset = ImagePreset', r'ImagePreset=' + selected_preset_path)
                ini_content = ini_content.replace(r'DeletedFilesFolder = DeletedFilesFolder', r'DeletedFilesFolder=' + self.rainmeter_deleted_files_dir + '\\')

                # Write the modified content to the destination INI file
                with open(ini_file_destination, "w") as ini_file:
                    ini_file.write(ini_content)
            else:
                raise FileNotFoundError(f"INI file not found at {ini_file_source}")

            # Open File Explorer and select the newly created folder
            subprocess.run(["explorer", "/select,", os.path.abspath(destination_folder)])

            self.show_info_message("Success", f'Rainmeter preset "{preset_name}" created successfully!')

        except Exception as e:
            self.show_info_message("Error", f"Failed to create Rainmeter preset. Error: {str(e)}")


    def delete_presets_files(self):
        """Deletes the selected preset file by sending it to the Recycle Bin and updates the preset table."""
        # Get the selected row
        selected_row = self.table_session_selection.currentRow()
        
        # Check if a row is actually selected
        if selected_row == -1:
            print('Warning', 'No preset selected for deletion.')
            return
        
        # Get the file name from the first column of the selected row
        file_item = self.table_session_selection.item(selected_row, 0)
        if not file_item:
            self.show_info_message('Warning', 'No file associated with the selected preset.')
            return
        
        file_name = file_item.text() + ".txt"
        file_path = os.path.join(self.session_presets_dir, file_name)
        
        # Move the file to the Recycle Bin if it exists
        if os.path.exists(file_path):
            try:
                send2trash(file_path)
            except Exception as e:
                self.show_info_message('Error', f'Failed to send preset to Recycle Bin. Error: {str(e)}')
                return
        else:
            self.show_info_message('Warning', f'File "{file_name}" does not exist.')
        
        # Reload the presets
        self.load_presets()
        
        # After deletion, select the appropriate row if the table isn't empty
        if self.table_session_selection.rowCount() > 0:
            # If we deleted the last row, select the new last row
            if selected_row >= self.table_session_selection.rowCount():
                new_selected_row = self.table_session_selection.rowCount() - 1
            else:
                # Otherwise, select the row at the same position
                new_selected_row = selected_row
            
            self.table_session_selection.selectRow(new_selected_row)
            self.update_selection_cache()



    def rename_presets(self, item):
        """Rename the preset file based on the new text typed in the row."""

        print("-- Renaming file")
        try:
            # Determine which table triggered the rename
            if item.tableWidget() == self.table_images_selection:
                cache = self.image_names_cache
                rename_directory = self.images_presets_dir
                name_col_index = 1
            elif item.tableWidget() == self.table_session_selection:
                cache = self.session_names_cache
                rename_directory = self.session_presets_dir
                name_col_index = 0
            else:
                # Unexpected table widget, exit early
                return False
                
            row = item.row()
            if row >= len(cache):
                return False

            # Get the old filename from the cache
            old_filename = cache[row]
            new_filename = item.text().strip() + ".txt"
            
            # Debugging output
            print(f"Row: {row}")
            print(f"Old filename: {old_filename}")
            print(f"New filename: {new_filename}")

            old_filepath = os.path.join(rename_directory, old_filename)
            new_filepath = os.path.join(rename_directory, new_filename)

            # Check if the old file exists
            if not os.path.exists(old_filepath):
                self.show_info_message('Error', f"Cannot rename: Original file '{old_filename}' does not exist.")
                return False

            # Check if the new filename already exists or if it is invalid
            if os.path.exists(new_filepath):
                self.show_info_message('Error', f"Cannot rename: '{new_filename}' already exists.")
                return False

            # Rename the file
            os.rename(old_filepath, new_filepath)

            # Update label assignment if this is a sentence preset
            if item.tableWidget() == self.table_images_selection and old_filename in self.preset_labels_dictionary:
                label = self.preset_labels_dictionary[old_filename]
                del self.preset_labels_dictionary[old_filename]
                self.preset_labels_dictionary[new_filename] = label
            
            # Update the cache after renaming
            cache[row] = new_filename
            
            # Save settings to persist label changes
            self.save_session_settings()
            self.update_selection_cache()
            return True

        except Exception as e:
            self.show_info_message('Error', f"Failed to rename preset. Error: {str(e)}")
            return False





    def load_presets(self):
        """Load existing presets into the tables and apply row selection from already loaded settings."""
        # Block signals during reload
        self.table_images_selection.blockSignals(True)
        self.table_session_selection.blockSignals(True)
        
        try:
            # Load image presets
            self.load_table_images_selection()
            
            # Load session presets
            self.load_session_presets()
            
            # Apply row selections after tables are loaded
            selected_image_row = self.selected_image_row
            selected_session_row = self.selected_session_row
            
            # Apply image selection
            if 0 <= selected_image_row < self.table_images_selection.rowCount():
                self.table_images_selection.selectRow(selected_image_row)
                self.image_selection_cache = selected_image_row
            
            # Apply session selection
            if 0 <= selected_session_row < self.table_session_selection.rowCount():
                self.table_session_selection.selectRow(selected_session_row)
        finally:
            # Always unblock signals when done
            self.table_images_selection.blockSignals(False)
            self.table_session_selection.blockSignals(False)
            # Manually update cache once at the end
            self.update_selection_cache()



    # Add new method to open the label manager
    def open_label_manager(self):
        """Open the label manager dialog."""
        dialog = LabelManagerDialog(self, self.labels_color_dictionary)
        self.init_styles(dialog=dialog)
        if dialog.exec_():
            self.labels_color_dictionary = dialog.get_labels()

            self.save_session_settings()  # Save the updated label settings
            self.load_presets()  # Reload with new labels






    def load_table_images_selection(self):
        """Load image preset files into the table and restore selection properly."""
        # Remember the currently selected filename before clearing
        self.table_images_selection.blockSignals(True)
        try:

            selected_filename = getattr(self, 'selected_image_filename', None)


            # Temporarily disable sorting during loading
            was_sorting_enabled = self.table_images_selection.isSortingEnabled()
            self.table_images_selection.setSortingEnabled(False)
            
            # Clear the table
            self.table_images_selection.setRowCount(0)
            
            # Load files from cache or directory
            self.image_names_cache = []
            try:
                files = sorted(os.listdir(self.images_presets_dir))
            except FileNotFoundError:
                files = []
            
            # Set up table columns
            self.table_images_selection.setColumnCount(3)
            self.table_images_selection.setHorizontalHeaderLabels(['Label', 'Name', 'Images'])
            
            # Set column widths
            self.table_images_selection.setColumnWidth(0, 40)
            self.table_images_selection.setColumnWidth(1, 295)
            self.table_images_selection.setColumnWidth(2, 80)

            # Dictionary to map labels to sort order prefixes (01_, 02_, etc.)
            ordered_labels = self.get_ordered_labels_from_settings()
            label_sort_prefixes = {}
            
            # Create sort prefixes based on the order in settings (01_, 02_, etc.)
            for i, label in enumerate(ordered_labels):
                # Use two digits with leading zero for better sorting
                prefix = f"{i+1:02d}_"
                label_sort_prefixes[label] = prefix

            table_delegate = TableLabelDelegate(self.table_images_selection)
            self.table_images_selection.setItemDelegateForColumn(0, table_delegate)

            max_length_delegate = MaxLengthDelegate(max_length=60)
            self.table_images_selection.setItemDelegateForColumn(1, max_length_delegate)

            # Prevent column resizing for table_imagess_selection
            header_images = self.table_images_selection.horizontalHeader()
            header_images.setSectionResizeMode(QHeaderView.Fixed)
            header_images.setSectionsClickable(True)  # Make header non-clickable



            # Create a mapping of filenames to row positions
            filename_to_row = {}
            
            # Load files into table rows
            for filename in files:
                if filename.endswith(".txt"):
                    # Get display name (remove .txt extension)
                    display_name = os.path.splitext(filename)[0]
                    
                    # Insert new row
                    row_position = self.table_images_selection.rowCount()
                    self.table_images_selection.insertRow(row_position)
                    
                    # Store mapping of filename to row position
                    filename_to_row[filename] = row_position
                    
                    # Get label info
                    label_name = self.preset_labels_dictionary.get(filename, "Default")
                    label_color = self.labels_color_dictionary.get(label_name, "#00000000")
                    sort_prefix = label_sort_prefixes.get(label_name, "99_")  # Use high prefix for undefined labels

                    # Add color label item (Column 0)
                    color_item = QtWidgets.QTableWidgetItem(sort_prefix)
                    color_item.setBackground(QColor(label_color))
                    color_item.setToolTip(label_name)
                    color_item.setFlags(color_item.flags() & ~Qt.ItemIsEditable)
                    self.table_images_selection.setItem(row_position, 0, color_item)
                    
                    # Add name item (Column 1)
                    name_item = QtWidgets.QTableWidgetItem(display_name)
                    name_item.setFlags(name_item.flags() | Qt.ItemIsEditable)
                    self.table_images_selection.setItem(row_position, 1, name_item)
                    
                    # Count images in preset file (Column 2)
                    file_path = os.path.join(self.images_presets_dir, filename)
                    image_count = 0
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            image_count = len(f.readlines())
                    except:
                        try:
                            with open(file_path, 'r', encoding='iso-8859-1') as f:
                                image_count = len(f.readlines())
                        except:
                            image_count = 0
                    
                    count_item = QtWidgets.QTableWidgetItem(str(image_count))
                    count_item.setTextAlignment(QtCore.Qt.AlignCenter)
                    count_item.setFlags(count_item.flags() & ~Qt.ItemIsEditable)
                    self.table_images_selection.setItem(row_position, 2, count_item)
                    
                    # Cache the filename
                    self.image_names_cache.append(filename)
            
            # Re-enable sorting if it was enabled before
            self.table_images_selection.setSortingEnabled(was_sorting_enabled)
            
            # Restore selection using filename mapping
            if selected_filename in filename_to_row:
                self.table_images_selection.selectRow(filename_to_row[selected_filename])
                self.table_images_selection.setFocus()
            elif hasattr(self, 'selected_image_row') and 0 <= self.selected_image_row < self.table_images_selection.rowCount():
                # Fallback to row number if filename not found
                self.table_images_selection.selectRow(self.selected_image_row)
                self.table_images_selection.setFocus()

        finally:
            self.table_images_selection.blockSignals(False)

    def get_ordered_labels_from_settings(self):
        """
        Retrieve the ordered list of labels from settings.
        Implement this method to read the order from your settings file.
        """
        # Example implementation - replace with your actual code to read from settings
        # This should return a list of labels in the order they appear in your settings
        return list(self.labels_color_dictionary.keys())


    def load_session_presets(self):
        """Load session preset files with proper selection restoration."""

        self.table_session_selection.blockSignals(True)
        

        # Remember the currently selected filename before clearing
        selected_filename = getattr(self, 'selected_session_filename', None)
        try:
            # Temporarily disable sorting during loading
            was_sorting_enabled = self.table_session_selection.isSortingEnabled()
            self.table_session_selection.setSortingEnabled(False)
            
            # Clear the table
            self.table_session_selection.setRowCount(0)
            
            # Load files from cache or directory

            self.session_names_cache = []
            try:
                files = sorted(os.listdir(self.session_presets_dir))
            except FileNotFoundError:
                files = []
        
            # Set up table with 3 columns
            self.table_session_selection.setColumnCount(3)
            self.table_session_selection.setHorizontalHeaderLabels(['Name', 'Images', 'Time'])
            
            # Set column widths
            self.table_session_selection.setColumnWidth(0, 380)
            self.table_session_selection.setColumnWidth(1, 60)
            self.table_session_selection.setColumnWidth(2, 20)
        

            # Set item delegates and header settings for table
            max_length_delegate = MaxLengthDelegate(max_length=60)

            self.table_session_selection.setItemDelegateForColumn(1, max_length_delegate)
            # Prevent column resizing for table_session_selection


            header_session = self.table_session_selection.horizontalHeader()
            header_session.setSectionResizeMode(QHeaderView.Fixed)
            header_session.setSectionsClickable(True)  # Make header non-clickable


            # Ensure the selection behavior is correctly set after applying styles
            self.table_session_selection.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
            self.table_session_selection.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)



            # Create a mapping of filenames to row positions
            filename_to_row = {}
            
            # Load files into table rows
            for filename in files:
                if filename.endswith(".txt"):
                    # Get display name (remove .txt extension)
                    display_name = os.path.splitext(filename)[0]
                    
                    # Insert new row
                    row_position = self.table_session_selection.rowCount()
                    self.table_session_selection.insertRow(row_position)
                    
                    # Store mapping of filename to row position
                    filename_to_row[filename] = row_position
                    
                    # Add name item (Column 0)
                    name_item = QtWidgets.QTableWidgetItem(display_name)
                    name_item.setFlags(name_item.flags() | Qt.ItemIsEditable)
                    self.table_session_selection.setItem(row_position, 0, name_item)
                    
                    # Load session data from file
                    file_path = os.path.join(self.session_presets_dir, filename)
                    total_images = 0
                    time_str = "0m 0s"
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            session_data = json.load(f)
                            total_images = session_data.get("total_images", 0)
                            time_str = session_data.get("time", "0m 0s")
                    except:
                        pass
                    
                    # Add images count (Column 1)
                    count_item = QtWidgets.QTableWidgetItem(str(total_images))
                    count_item.setTextAlignment(QtCore.Qt.AlignCenter)
                    count_item.setFlags(count_item.flags() & ~Qt.ItemIsEditable)
                    self.table_session_selection.setItem(row_position, 1, count_item)
                    
                    # Add time string (Column 2)
                    time_item = QtWidgets.QTableWidgetItem(time_str)
                    time_item.setTextAlignment(QtCore.Qt.AlignCenter)
                    time_item.setFlags(time_item.flags() & ~Qt.ItemIsEditable)
                    self.table_session_selection.setItem(row_position, 2, time_item)
                    
                    # Cache the filename
                    self.session_names_cache.append(filename)
            
            # Re-enable sorting if it was enabled before
            self.table_session_selection.setSortingEnabled(was_sorting_enabled)
            
            # Restore selection using filename mapping
            if selected_filename in filename_to_row:
                self.table_session_selection.selectRow(filename_to_row[selected_filename])
                self.table_session_selection.setFocus()
            elif hasattr(self, 'selected_session_row') and 0 <= self.selected_session_row < self.table_session_selection.rowCount():
                # Fallback to row number if filename not found
                self.table_session_selection.selectRow(self.selected_session_row)
                self.table_session_selection.setFocus()

        finally:
            self.table_session_selection.blockSignals(False)
     

    def start_session_launcher(self):
        self.save_session_settings()
        self.start_session_from_files()

    def start_session_from_files(self, image_preset_path=None, session_preset_path=None, randomize_settings=True):
        """
        Starts a session using specified presets or selected files.
        """
        # Helper function to convert time string to seconds
        def convert_time_to_seconds(time_str):
            minutes, seconds = 0, 0
            if 'm' in time_str:
                minutes = int(time_str.split('m')[0])
                time_str = time_str.split('m')[1].strip()
            if 's' in time_str:
                seconds = int(time_str.split('s')[0])
            return minutes * 60 + seconds

        def remove_missing_files(image_file_path):
                """
                Removes missing image files from the given preset file and updates it.
                """
                selected_images = []

                # Read image paths from the image preset file
                try:
                    with open(image_file_path, 'r', encoding='utf-8') as f:
                        selected_images = [line.strip() for line in f.readlines() if line.strip()]
                        print(f"Loaded {len(selected_images)} images from {image_file_path}.")
                except FileNotFoundError:
                    print(f"Image file not found: {image_file_path}")
                    
                    return False

                # Remove missing files from the list
                selected_images = [img for img in selected_images if os.path.exists(img)]
                print(f"Filtered to {len(selected_images)} existing images from {image_file_path}.")

                # Save the updated list of images back to the preset file
                try:
                    with open(image_file_path, 'w', encoding='utf-8') as f:
                        f.writelines([img + '\n' for img in selected_images])
                        print(f"Updated image preset file saved: {image_file_path}")
                except IOError as e:
                    print(f"Error writing to image file: {image_file_path} - {e}")
                return selected_images


        if self.selected_image_filename == None or self.selected_session_filename == None:
            self.show()
            return
             
        if image_preset_path == None:
            image_preset_path = os.path.join(self.images_presets_dir, self.selected_image_filename )
        if session_preset_path == None:
            session_preset_path = os.path.join(self.session_presets_dir, self.selected_session_filename)

        randomize_settings = self.randomize_settings




        selected_images = remove_missing_files(image_preset_path)

        if selected_images == False:
            self.show()
            return
        try:
            with open(session_preset_path, 'r') as f:
                session_details = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"Error reading session preset: {session_preset_path}")
            self.show()
            return


        # Randomize images if applicable
        if randomize_settings:
            random.shuffle(selected_images)
            print("-- Images have been shuffled randomly.")

        # Get session details
        session_time = convert_time_to_seconds(session_details.get('time', '0m 0s'))
        total_images_to_display = session_details.get('total_images', len(selected_images))

        # Limit the number of images to display
        selected_images = selected_images[:total_images_to_display]

        # Initialize and display the session
        self.session_schedule = {
            0: [session_details.get('session_name', 'Session'), total_images_to_display, session_time]
        }
        self.total_scheduled_images = total_images_to_display

        if self.display is not None:
            self.display.close()
            self.display = None

        self.display = SessionDisplay(
            shortcuts=self.shortcut_settings,
            schedule=self.session_schedule,
            items=selected_images,
            total=self.total_scheduled_images
        )
        self.init_styles(session=self.display)

        self.display.load_entry()
        self.display.show()


    def load_session_settings(self):
        """Load session settings with filename-based selection tracking."""
        session_settings_path = os.path.join(self.presets_dir, 'session_settings.txt')
        
        # Default settings
        default_settings = {
            "selected_image_row": -1,
            "selected_session_row": -1,
            "selected_image_filename": None,
            "selected_session_filename": None,
            "randomize_settings": False,
            "auto_start_settings": False,
            "theme_settings": 'default_theme.txt',
            "shortcuts": self.default_shortcuts,
            "labels_color_dictionary": {"Default": "#00000000"},
            "preset_labels_dictionary": {},
            "image_names_cache": [],
            "session_names_cache": []
        }
        
        # Try to load settings from file
        try:
            if os.path.exists(session_settings_path):
                with open(session_settings_path, 'r', encoding='utf-8') as f:
                    loaded_settings = json.load(f)
                    
                    # Merge with default settings
                    for key in default_settings:
                        if key in loaded_settings:
                            default_settings[key] = loaded_settings[key]
        except Exception as e:
            print(f"Error loading session settings: {str(e)}")
        
        # Apply settings
        self.selected_image_row = default_settings["selected_image_row"]
        self.selected_session_row = default_settings["selected_session_row"]
        self.selected_image_filename = default_settings["selected_image_filename"]
        self.selected_session_filename = default_settings["selected_session_filename"]
        self.randomize_settings = default_settings["randomize_settings"]
        self.auto_start_settings = default_settings["auto_start_settings"]
        self.current_theme = default_settings["theme_settings"]
        self.shortcut_settings = default_settings["shortcuts"]
        self.labels_color_dictionary = default_settings["labels_color_dictionary"]
        self.preset_labels_dictionary = default_settings["preset_labels_dictionary"]
        
        # Set UI elements
        self.randomize_toggle.setChecked(self.randomize_settings)
        self.auto_start_toggle.setChecked(self.auto_start_settings)
        
        # Initialize caches if they exist in settings
        if "image_names_cache" in default_settings:
            self.image_names_cache = default_settings["image_names_cache"]
        if "session_names_cache" in default_settings:
            self.session_names_cache = default_settings["session_names_cache"]


    def save_session_settings(self):
        """Save session settings including selected filenames."""
        session_settings_path = os.path.join(self.presets_dir, 'session_settings.txt')
        
        # Get current selections by filename
        selected_image_filename = None
        selected_session_filename = None
        
        # Get image selection
        selected_image_row = self.table_images_selection.currentRow()
        if selected_image_row >= 0:
            name_item = self.table_images_selection.item(selected_image_row, 1)
            if name_item:
                selected_image_filename = name_item.text() + ".txt"
        
        # Get session selection
        selected_session_row = self.table_session_selection.currentRow()
        if selected_session_row >= 0:
            name_item = self.table_session_selection.item(selected_session_row, 0)
            if name_item:
                selected_session_filename = name_item.text() + ".txt"
        
        # Create settings dictionary
        settings = {
            "selected_image_row": selected_image_row,  # Keep for backward compatibility
            "selected_session_row": selected_session_row,  # Keep for backward compatibility
            "selected_image_filename": selected_image_filename,
            "selected_session_filename": selected_session_filename,
            "randomize_settings": self.randomize_settings,
            "auto_start_settings": self.auto_start_settings,
            "theme_settings": self.current_theme,
            "shortcuts": self.shortcut_settings,
            "labels_color_dictionary": self.labels_color_dictionary,
            "preset_labels_dictionary": self.preset_labels_dictionary,
            "image_names_cache": self.image_names_cache if hasattr(self, 'image_names_cache') else [],
            "session_names_cache": self.session_names_cache if hasattr(self, 'session_names_cache') else []
        }
        
        # Save to file
        try:
            with open(session_settings_path, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=4)
        except Exception as e:
            print(f"Error saving session settings: {str(e)}")



    def apply_shortcuts_main_window(self):
        """Apply the shortcuts for the main window."""

        self.main_window_start_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence(self.shortcut_settings["main_window"]["start"]), self)
        self.main_window_start_shortcut.activated.connect(self.start_session_launcher)

        self.main_window_close_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence(self.shortcut_settings["main_window"]["close"]), self)
        self.main_window_close_shortcut.activated.connect(self.close)

        self.main_window_cycle_label = QtWidgets.QShortcut(QtGui.QKeySequence(self.shortcut_settings["main_window"]["cycle_label"]), self)
        self.main_window_cycle_label.activated.connect(self.cycle_label)


    def cycle_label(self):
        selected_row = self.table_images_selection.currentRow()
        if selected_row >= 0:
            # Get the selected file name
            file_item = self.table_images_selection.item(selected_row, 1)  # Name column
            if file_item:
                filename = file_item.text() + ".txt"
                
                # Get all label names sorted
                label_names = sorted(list(self.labels_color_dictionary.keys()))
                
                # Get current label
                current_label = self.preset_labels_dictionary.get(filename, "Default")
                
                # Find next label in the sequence
                try:
                    current_index = label_names.index(current_label)
                    next_index = (current_index + 1) % len(label_names)
                    next_label = label_names[next_index]
                except ValueError:
                    # If current label not found (shouldn't happen unless corrupted data)
                    next_label = "Default"
                
                # Set the new label
                self.preset_labels_dictionary[filename] = next_label
                
                # Update the color cell
                color_item = self.table_images_selection.item(selected_row, 0)
                if color_item:
                    color = self.labels_color_dictionary.get(next_label, "#00000000")
                    color_item.setBackground(QColor(color))
                    color_item.setToolTip(next_label)

                # Save the settings & Reload table
                self.save_session_settings()
                self.load_presets()


                return True  # Event handled


    def update_randomize_settings(self, state):
        """Update the randomize_settings variable based on the checkbox state."""
        # Check if the checkbox is checked (Qt.Checked is 2, Qt.Unchecked is 0)
        if state == Qt.Checked:
            self.randomize_settings = True
        else:
            self.randomize_settings = False
        self.save_session_settings()


    def update_auto_start_settings(self, state):
        """Update the randomize_settings variable based on the checkbox state."""
        # Check if the checkbox is checked (Qt.Checked is 2, Qt.Unchecked is 0)
        if state == Qt.Checked:
            self.auto_start_settings = True
        else:
            self.auto_start_settings = False
        self.save_session_settings()




    def grab_schedule(self):
        """Builds self.session_schedule with data from the schedule"""
        self.session_schedule = {}
        for row in range(self.table_session_selection.rowCount()):
            self.session_schedule[row] = []
            for column in range(self.table_session_selection.columnCount()):
                if self.table_session_selection.item(row, column).text() == '0':
                    pass
                self.session_schedule[row].append(self.table_session_selection.item(row, column).text())


    def open_theme_selector(self):
        """Open the theme selection dialog."""
        dialog = ThemeSelectorDialog(self, self.theme_presets_dir, self.current_theme)
        self.init_styles(dialog=dialog)
        if dialog.exec_():
            selected_theme = dialog.get_selected_theme()
            if selected_theme:
                self.current_theme = selected_theme
                self.save_session_settings()  # Save the updated theme setting

                self.init_styles() # Load the theme




# Delegate for the main table's label column (column 0)
class TableLabelDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(TableLabelDelegate, self).__init__(parent)
        
    def paint(self, painter, option, index):
        # Check if this is column 0 (the label column)
        if index.column() == 0:
            # Get the original background color stored in the item
            color = index.data(Qt.BackgroundRole)
            
            # If the item is selected, we still want to show some indication
            if option.state & QStyle.State_Selected:
                # Draw a border to indicate selection but keep the original background
                painter.save()
                painter.setPen(Qt.white)
                painter.fillRect(option.rect, color)
                painter.drawRect(option.rect.adjusted(1, 1, -1, -1))
                painter.restore()
            else:
                # Not selected, just fill with the original color
                painter.fillRect(option.rect, color)
            
            return
        
        # For all other columns, use the default delegate painting
        super(TableLabelDelegate, self).paint(painter, option, index)

# Delegate for the label manager's color column (column 1)
class LabelColorDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(LabelColorDelegate, self).__init__(parent)
        
    def paint(self, painter, option, index):
        # Check if this is column 1 (the color column)
        if index.column() == 1:
            # Get the original background color stored in the item
            color = index.data(Qt.BackgroundRole)
            
            # If the item is selected, we still want to show some indication
            if option.state & QStyle.State_Selected:
                # Draw a border to indicate selection but keep the original background
                painter.save()
                painter.setPen(Qt.white)
                painter.fillRect(option.rect, color)
                painter.drawRect(option.rect.adjusted(1, 1, -1, -1))
                painter.restore()
            else:
                # Not selected, just fill with the original color
                painter.fillRect(option.rect, color)
            
            return
        
        # For all other columns, use the default delegate painting
        super(LabelColorDelegate, self).paint(painter, option, index)

class SessionDisplay(QWidget, Ui_session_display):
    closed = QtCore.pyqtSignal() # Needed here for close event to work.

    def __init__(self, shortcuts = None, schedule=None, items=None, total=None):
        super().__init__()
        self.setupUi(self)

        # Initialize grid state
        self.grid_displayed = False
        self.setWindowTitle('Practice')
        # Create grid overlay
        self.grid_overlay = QLabel(self.image_display)  # Parent it to the image display
        self.grid_overlay.setGeometry(self.image_display.geometry())  # Match its geometry
        self.grid_overlay.setStyleSheet("background-color: transparent;")
        self.grid_overlay.hide()  # Start hidden
        self.vertical_lines_grid = 4
        self.horizontal_lines_grid = 4

        self.rotation_index = 0  # Starting rotation at 0 degrees
        self.rotation_factor = 5  # Rotation increment in degrees

        self.always_on_top_borde_settings = "rgb(255, 0, 0)"


        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        # Create the border overlay QLabel
        self.border_overlay = QLabel(self)
        self.border_overlay.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.border_overlay.setStyleSheet("background: transparent;")
        self.border_overlay.hide()  # Hide it initially

        self.init_sizing()
        self.init_scaling_size()
        self.schedule = schedule
        self.shortcuts = shortcuts
        self.playlist = items
        self.playlist_position = 0
        self.total_scheduled_images = total

        self.scaled_images_cache = None 
        self.offset_cache = [0,0]

        self.init_timer()
        self.init_entries()
        self.installEventFilter(self)
        self.init_image_mods()
        self.init_sounds()
        self.init_mixer()
        self.init_session_buttons()
        self.apply_shortcuts_session_window()
        self.skip_count = 1



        # Connect the resize event to update the border overlay
        self.resizeEvent = self.update_border_overlay_geometry
        self.setMinimumSize(QtCore.QSize(640, 1))

        # Other initialization logic
        self.old_position = None  # Initialize old_position for dragging




    def resizeEvent(self, event):
        super(SessionDisplay, self).resizeEvent(event)
        # Adjust the grid overlay to match the new image size and position
        self.grid_overlay.setGeometry(self.image_display.geometry())
        
        # Reapply the grid if it's currently displayed
        if self.grid_displayed:
            self.apply_grid()

    def update_border_overlay_geometry(self, event=None):
        # Update the geometry to cover the entire window
        self.border_overlay.setGeometry(self.rect())

        # Optionally redraw the border if it is currently shown
        if self.border_overlay.isVisible():
            self.apply_border(True)


    def copy_image_path(self):
        # Example image path retrieval; replace with actual method to get current image path
        current_image_path = os.path.normpath(self.playlist[self.playlist_position]) 
        clipboard = QApplication.clipboard()
        clipboard.setText(current_image_path)
        print(f"Copied image path: {current_image_path}")



    def open_image_folder(self):
        # Retrieve the current image path
        current_image_path = os.path.normpath(self.playlist[self.playlist_position]) 

        # Check if the image path exists
        if os.path.exists(current_image_path):

            # Using os.startfile to open the folder and select the image
            subprocess.Popen(f'explorer /select,"{current_image_path}"')
            print(f"Opened folder containing: {current_image_path}")
        else:
            print("Image path does not exist.")

    def delete_image(self):
        # Retrieve the current image path
        current_image_path = os.path.normpath(self.playlist[self.playlist_position]) 

        # Check if the image path exists
        if os.path.exists(current_image_path):

            # Using send2trash to send image to recycle bin
            send2trash(current_image_path)

            #Delete item from playlist
            self.playlist.pop(self.playlist_position)
            self.playlist_position -= 1
            self.load_next_image()


            print(f"Image deleted : {current_image_path}")

        else:
            print("Image path does not exist.")




    def show_main_window(self):
        if view.isMinimized():  # Check if the window is minimized
            view.showNormal()  # Restore the window if minimized
        view.show()  # Show the main window
        view.init_styles()  # Initialize window style           
        view.raise_()  # Bring the window to the front
        view.activateWindow()  # Focus on the window

    def init_sizing(self):
        """
        Resizes the window to half of the current screen's resolution,
        sets states for window flags,
        and initializes self.image_size_cache.
        
        """
        self.resize(self.screen().availableSize() / 2)
        self.toggle_resize_status = False
        self.toggle_always_on_top_status = False
        self.frameless_status = False
        self.sizePolicy().setHeightForWidth(True)
        self.image_size_cache = self.size()

    def init_scaling_size(self):
        """
        Creates a scaling box size that is used as a basis for
        images to scale off of. The box dimensions are determined by the 
        smallest side of half of the given rectangle from the
        current screen's available resolution.

        """
        half_screen = self.screen().availableSize() / 2
        min_length = min(half_screen.height(), half_screen.width())
        self.scaling_size = QtCore.QSize(min_length, min_length)

    def init_timer(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.countdown)
        self.timer.start(500)

    def init_entries(self):
        self.entry = {
            'current': 0,
            'total': [*self.schedule][-1] + 1,
            'amount of items': int(self.schedule[0][1]),
            'time': int(self.schedule[0][2])}
        self.new_entry = True
        if self.entry['amount of items'] > 1:
            self.end_of_entry = False
        else:
            self.end_of_entry = True
        
    def init_image_mods(self):
        self.image_mods = {
            'hflip': False,
            'vflip': False,
            'grayscale': False,
            'scale_factors': [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5,
             1.6, 1.7, 1.8, 1.9, 2, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3],
            'default_scale_index':7,
            'default_width': 900,
            'scale_index' : 7}


    def pixmap_to_numpy(self, pixmap):
        size = pixmap.size()
        h = size.height()
        w = size.width()

        # Get QImage from QPixmap
        qimage = pixmap.toImage()
        qimage = qimage.convertToFormat(QtGui.QImage.Format_RGB888)

        # Get pointer to image data
        ptr = qimage.bits()
        ptr.setsize(h * w * 3)  # 3 channels (RGB)

        # Create numpy array
        arr = np.array(ptr).reshape(h, w, 3)
        return arr


    def rotate_image(self, image, angle):
        """
        Rotate the given image by the specified angle.

        Parameters:
            image (numpy.ndarray): The image to rotate.
            angle (float): The angle by which to rotate the image.

        Returns:
            numpy.ndarray: The rotated image.
        """
        if image is None:
            print("No image provided for rotation.")
            return None

        # Check if the image has an alpha channel
        has_alpha = image.shape[2] == 4 if len(image.shape) == 3 else False

        # Get image dimensions
        (h, w) = image.shape[:2]
        image_center = (w / 2, h / 2)

        # Create rotation matrix for the given angle
        matrix = cv2.getRotationMatrix2D(image_center, angle, 1.0)

        # Perform the rotation
        if has_alpha:
            # Split channels (BGR + Alpha)
            bgr = image[..., :3]  # BGR channels
            alpha = image[..., 3]

            # Rotate the BGR and Alpha channels separately
            rotated_bgr = cv2.warpAffine(bgr, matrix, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0))
            rotated_alpha = cv2.warpAffine(alpha, matrix, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0,))

            # Recombine the rotated BGR and Alpha
            rotated_image = np.dstack([rotated_bgr, rotated_alpha])
        else:
            # Rotate image without alpha channel
            rotated_image = cv2.warpAffine(image, matrix, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0))

        # Ensure the rotated image is in RGB format for Qt
        if rotated_image.shape[2] == 3:
            rotated_image = cv2.cvtColor(rotated_image, cv2.COLOR_BGR2RGB)
        elif rotated_image.shape[2] == 4:
            rotated_image = cv2.cvtColor(rotated_image, cv2.COLOR_BGRA2RGBA)

        return rotated_image


    def rotate_image_right(self):
            self.rotation_index -= self.rotation_factor  # Clockwise
            self.display_image(play_sound=False, update_status = False)

    def rotate_image_left(self):
            self.rotation_index += self.rotation_factor  # Clockwise
            self.display_image(play_sound=False, update_status = False)






    def init_sounds(self):
        """
        Gets absolute path to sounds. 
        PyInstaller creates a temp folder, and stores dependencies path in _MEIPASS.
        If the temp folder is not found, then use the current file path.

        """
        relative_path = "sounds"
        try:
            base_path = sys._MEIPASS
        except (Exception, FileNotFoundError):
            base_path = os.path.dirname(os.path.abspath(__file__))
        self.sounds_dir = os.path.join(base_path, relative_path)
        
    def init_mixer(self):
        mixer.init()
        try:
            """
            If view.mute exists, then a session has been started before.
            Set mute and volume according to previous session's sound settings.
            """
            if view.mute is True: # if view.mute exists and is True
                self.mute = True
                self.volume = mixer.music.get_volume()
                mixer.music.set_volume(0.0)
            else: # if view.mute exists and is False
                self.mute = False
                self.volume = view.volume
        except: # view.mute does not exist, so init settings with default.
            self.volume = mixer.music.get_volume()
            self.mute = False






    def init_session_buttons(self):
        # Session tools
        self.grid_button.clicked.connect(self.toggle_grid)
        self.grid_button.setToolTip(f"[{self.shortcuts['session_window']['toggle_grid']}] Toggle grid, [{self.shortcuts['session_window']['grid_settings']}] Grid settings")
        
        self.grayscale_button.clicked.connect(self.grayscale)
        self.grayscale_button.setToolTip(f"[{self.shortcuts['session_window']['grayscale']}] Toggle grayscale")

        self.lock_scale_button.clicked.connect(self.toggle_resize)
        self.lock_scale_button.setToolTip(f"[{self.shortcuts['session_window']['toggle_resize']}] Prevent rescaling of the window")

        # Vertical and Horizontal flips
        self.flip_horizontal_button.clicked.connect(self.flip_horizontal)
        self.flip_horizontal_button.setToolTip(f"[{self.shortcuts['session_window']['flip_horizontal']}] Horizontal Flip")

        self.flip_vertical_button.clicked.connect(self.flip_vertical)
        self.flip_vertical_button.setToolTip(f"[{self.shortcuts['session_window']['flip_vertical']}] Vertical Flip")

        # Session navigation
        self.previous_image.clicked.connect(self.load_prev_image)
        self.previous_image.setToolTip(f"[{self.shortcuts['session_window']['prev_image']}] Previous image")

        self.pause_timer.clicked.connect(self.pause)
        self.pause_timer.setToolTip(f"[{self.shortcuts['session_window']['pause_timer']}] Pause Timer")

        self.stop_session.clicked.connect(self.close)
        self.stop_session.setToolTip(f"[{self.shortcuts['session_window']['close']}] Stop Session and closes window")

        self.next_image.clicked.connect(self.load_next_image)
        self.next_image.setToolTip(f"[{self.shortcuts['session_window']['next_image']}] Next Image")

        # Image path and folder
        self.copy_image_path_button.clicked.connect(self.copy_image_path)
        self.copy_image_path_button.setToolTip(f"[{self.shortcuts['session_window']['copy_path']}] Copy image path to clipboard")

        self.open_folder_button.clicked.connect(self.open_image_folder)
        self.open_folder_button.setToolTip(f"[{self.shortcuts['session_window']['open_folder']}] Open image folder")

        self.delete_image_button.clicked.connect(self.delete_image)
        self.delete_image_button.setToolTip(f"[{self.shortcuts['session_window']['delete_image']}] Delete image")

        # Setting window
        self.show_main_window_button.clicked.connect(self.show_main_window)
        self.show_main_window_button.setToolTip(f"[{self.shortcuts['session_window']['show_main_window']}] Open settings window")

        
        

        


    def apply_shortcuts_session_window(self):
        """Apply the shortcuts for the session window."""

        self.toggle_resize_key = QtWidgets.QShortcut(QtGui.QKeySequence(self.shortcuts["session_window"]["toggle_resize"]), self)
        self.toggle_resize_key.activated.connect(self.toggle_resize)

        self.right_rotation_key = QtWidgets.QShortcut(QtGui.QKeySequence(self.shortcuts["session_window"]["rotate_right"]), self)
        self.right_rotation_key.activated.connect(self.rotate_image_right)

        self.left_rotation_key = QtWidgets.QShortcut(QtGui.QKeySequence(self.shortcuts["session_window"]["rotate_left"]), self)
        self.left_rotation_key.activated.connect(self.rotate_image_left)

        self.always_on_top_key = QtWidgets.QShortcut(QtGui.QKeySequence(self.shortcuts["session_window"]["always_on_top"]), self)
        self.always_on_top_key.activated.connect(self.toggle_always_on_top)

        self.hflip_key = QtWidgets.QShortcut(QtGui.QKeySequence(self.shortcuts["session_window"]["flip_horizontal"]), self)
        self.hflip_key.activated.connect(self.flip_horizontal)

        self.vflip_key = QtWidgets.QShortcut(QtGui.QKeySequence(self.shortcuts["session_window"]["flip_vertical"]), self)
        self.vflip_key.activated.connect(self.flip_vertical)

        self.prev_image_key = QtWidgets.QShortcut(QtGui.QKeySequence(self.shortcuts["session_window"]["prev_image"]), self)
        self.prev_image_key.activated.connect(self.load_prev_image)

        self.pause_timer_key = QtWidgets.QShortcut(QtGui.QKeySequence(self.shortcuts["session_window"]["pause_timer"]), self)
        self.pause_timer_key.activated.connect(self.pause)

        self.close_key = QtWidgets.QShortcut(QtGui.QKeySequence(self.shortcuts["session_window"]["close"]), self)
        self.close_key.activated.connect(self.close)

        self.next_image_key = QtWidgets.QShortcut(QtGui.QKeySequence(self.shortcuts["session_window"]["next_image"]), self)
        self.next_image_key.activated.connect(self.load_next_image)

        self.open_key = QtWidgets.QShortcut(QtGui.QKeySequence(self.shortcuts["session_window"]["open_folder"]), self)
        self.open_key.activated.connect(self.open_image_folder)

        self.copy_key = QtWidgets.QShortcut(QtGui.QKeySequence(self.shortcuts["session_window"]["copy_path"]), self)
        self.copy_key.activated.connect(self.copy_image_path)

        self.delete_image_key = QtWidgets.QShortcut(QtGui.QKeySequence(self.shortcuts["session_window"]["delete_image"]), self)
        self.delete_image_key.activated.connect(self.delete_image)

        self.grayscale_key = QtWidgets.QShortcut(QtGui.QKeySequence(self.shortcuts["session_window"]["grayscale"]), self)
        self.grayscale_key.activated.connect(self.grayscale)

        self.grid_settings_key = QtWidgets.QShortcut(QtGui.QKeySequence(self.shortcuts["session_window"]["grid_settings"]), self)
        self.grid_settings_key.activated.connect(self.open_grid_settings_dialog)

        self.grid_key = QtWidgets.QShortcut(QtGui.QKeySequence(self.shortcuts["session_window"]["toggle_grid"]), self)
        self.grid_key.activated.connect(self.toggle_grid)

        self.zoom_in_key = QtWidgets.QShortcut(QtGui.QKeySequence(self.shortcuts["session_window"]["zoom_in"]), self)
        self.zoom_in_key.activated.connect(self.zoom_minus)

        self.zoom_out_key = QtWidgets.QShortcut(QtGui.QKeySequence(self.shortcuts["session_window"]["zoom_out"]), self)
        self.zoom_out_key.activated.connect(self.zoom_plus)

        self.zoom_in_numpad_key = QtWidgets.QShortcut(QtGui.QKeySequence(self.shortcuts["session_window"]["zoom_in_numpad"]), self)
        self.zoom_in_numpad_key.activated.connect(self.zoom_plus)

        self.zoom_out_numpad_key = QtWidgets.QShortcut(QtGui.QKeySequence(self.shortcuts["session_window"]["zoom_out_numpad"]), self)
        self.zoom_out_numpad_key.activated.connect(self.zoom_minus)

        self.show_main_window_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence(self.shortcuts["session_window"]["show_main_window"]), self)
        self.show_main_window_shortcut.activated.connect(self.show_main_window)

        self.mute_key = QtWidgets.QShortcut(QtGui.QKeySequence(self.shortcuts["session_window"]["mute"]), self)
        self.mute_key.activated.connect(self.toggle_mute)

        self.add_30 = QtWidgets.QShortcut(QtGui.QKeySequence(self.shortcuts["session_window"]["add_30_seconds"]), self)
        self.add_30.activated.connect(self.add_30_seconds)

        self.add_60 = QtWidgets.QShortcut(QtGui.QKeySequence(self.shortcuts["session_window"]["add_60_seconds"]), self)
        self.add_60.activated.connect(self.add_60_seconds)

        self.restart = QtWidgets.QShortcut(QtGui.QKeySequence(self.shortcuts["session_window"]["restart_timer"]), self)
        self.restart.activated.connect(self.restart_timer)




    def closeEvent(self, event):
        """
        Handles cleanup when the window is closed.
        """
        view.display = None
        # Stop any active timers
        if hasattr(self, 'timer') and self.timer.isActive():
            self.timer.stop()

        # Disconnect any signals or shortcuts
        try:
            self.close
            # Add any other signal disconnections here
        except Exception as e:
            print(f"Error disconnecting signals: {e}")

        # Emit the closed signal
        self.closed.emit()

        # Call the parent class's closeEvent
        super(SessionDisplay, self).closeEvent(event)

        # Ensure the widget is deleted
        self.deleteLater()


    def wheelEvent(self, event):
        # Check if Ctrl key is pressed
        ctrl_pressed = event.modifiers() & QtCore.Qt.ControlModifier

        if ctrl_pressed:
            # Rotate image based on wheel movement
            if event.angleDelta().y() > 0:
                self.rotate_image_right()
            else:
                self.rotate_image_left()
        else:
            # Zoom in or out based on wheel movement
            if event.angleDelta().y() > 0:
                self.zoom_plus()
            else:
                self.zoom_minus()



    def mousePressEvent(self, event):
        """Capture the mouse press event to initiate dragging."""
        if event.button() == QtCore.Qt.LeftButton:
            self.old_position = event.globalPos()

    def mouseMoveEvent(self, event):
        """Handle the mouse movement for dragging the window."""
        if event.buttons() == QtCore.Qt.LeftButton and self.old_position:
            delta = event.globalPos() - self.old_position
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_position = event.globalPos()

    def mouseReleaseEvent(self, event):
        """Reset the dragging state after the mouse button is released."""
        if event.button() == QtCore.Qt.LeftButton:
            self.old_position = None

    # region Session processing functions
    def eventFilter(self, source, event):
        if source is self and event.type() == QtCore.QEvent.Resize:
            
            
            if self.toggle_resize_status:
                self.image_display.setPixmap(
                    self.image.scaled(
                        self.size(),
                        aspectRatioMode=QtCore.Qt.KeepAspectRatio,
                        transformMode=QtCore.Qt.SmoothTransformation))


            else:
                self.image_display.setPixmap(
                    self.image.scaled(
                        self.image_display.size(),
                        aspectRatioMode=QtCore.Qt.KeepAspectRatio,
                        transformMode=QtCore.Qt.SmoothTransformation))



        return super(SessionDisplay, self).eventFilter(source, event)


    def toggle_mute(self):
        if self.mute is True:
            self.mute = False
            mixer.music.set_volume(self.volume)
        else:
            self.mute = True
            self.volume = mixer.music.get_volume()
            mixer.music.set_volume(0.0)












    def display_image(self, play_sound=True, update_status=True):
        # Check if the QLabel `session_info` is still valid
        if not hasattr(self, 'session_info') or sip.isdeleted(self.session_info):
            return  # Exit if session_info doesn't exist or has been deleted

        # Existing code to update `session_info`...

        if self.playlist_position >= len(self.playlist):
            self.display_end_screen()
            return

        # Sounds
        if self.new_entry:
            mixer.music.load(self.sounds_dir + "\\new_entry.mp3")
            if play_sound:
                mixer.music.play()
            # self.new_entry = False
        elif self.entry['amount of items'] == 0:  # Last image in entry
            mixer.music.load(self.sounds_dir + "\\last_entry_image.mp3")
            if play_sound:

                mixer.music.play()
        elif self.entry['time'] > 10:
            mixer.music.load(self.sounds_dir + "\\new_image.mp3")
            if play_sound:
                mixer.music.play()

        if self.playlist_position > len(self.playlist):  # Last image
            self.timer.stop()
            self.timer_display.setText(f'Done!')
            return
        else:



            self.session_info.setText(
                
                f'{int(self.schedule[self.entry["current"]][1]) - self.entry["amount of items"]}'
                f'/{int(self.schedule[self.entry["current"]][1])}')



            self.prepare_image_mods(update = update_status)
        if update_status:
            self.reset_timer()  # Reset the timer each time a new image is displayed
        self.update_session_info()



    def prepare_image_mods(self, update=True):
        """
        Modifies self.image depending on the values in self.image_mods.
        If update=True, loads and caches the image.
        If update=False, retrieves the image from cache.
        """
        file_path = Path(self.playlist[self.playlist_position])

        # Supported image formats
        valid_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.tiff', '.jfif', '.bmp'}
        
        # Extract file extension and check if it's valid
        file_extension = file_path.suffix.lower()

        if update:
            if file_extension in valid_extensions:
                try:
                    # Convert image to CV format
                    cvimage = self.convert_to_cvimage() if file_extension == '.jpg' else cv2.imread(str(file_path))

                    # Check if the image was loaded correctly
                    if cvimage is None:
                        raise FileNotFoundError(f"Failed to load image: {file_path}")

                    # Get image dimensions and prepare for QImage
                    height, width = cvimage.shape[:2]
                    bytes_per_line = cvimage.strides[0]

                except (Exception, FileNotFoundError) as e:
                    print(f'Error with processing image: {e}')
                    self.setWindowTitle('Error processing image')
                    return

                # Downscale the image to default_width if necessary
                default_width = self.image_mods['default_width']
                if width > default_width:
                    scaling_factor = default_width / width
                    new_width = default_width
                    new_height = int(height * scaling_factor)
                    cvimage = cv2.resize(cvimage, (new_width, new_height), interpolation=cv2.INTER_AREA)

                # Cache the downscaled image
                self.scaled_images_cache = cvimage

            else:
                print(f"Unsupported file extension: {file_extension}")
                return
        else:
            # Retrieve the cached image
            cvimage = self.scaled_images_cache
            if cvimage is None:
                print(f"Image not found in cache: {file_path}")
                return

        # Apply grayscale modification if needed
        if self.image_mods['grayscale']:
            cvimage = cv2.cvtColor(cvimage, cv2.COLOR_BGR2GRAY)
            # Convert grayscale image to 3-channel format
            cvimage = cv2.cvtColor(cvimage, cv2.COLOR_GRAY2RGB)

        # Apply horizontal and vertical flips
        if self.image_mods['hflip']:
            cvimage = np.fliplr(cvimage)
        if self.image_mods['vflip']:
            cvimage = np.flipud(cvimage)

        if self.image_mods['hflip']:
            cvimage = self.rotate_image(cvimage, -self.rotation_index)
        else:
            cvimage = self.rotate_image(cvimage, self.rotation_index)


        # Convert CV image to QImage
        height, width, channels = cvimage.shape
        bytes_per_line = channels * width
        qt_image_format = QtGui.QImage.Format_RGBA8888 if channels == 4 else QtGui.QImage.Format_RGB888

        # Convert to QImage
        qt_image = QtGui.QImage(cvimage.data, width, height, bytes_per_line, qt_image_format)

        # Convert to QPixmap
        self.image = QtGui.QPixmap.fromImage(qt_image)

        # Scaling and display logic
        scale_index = self.image_mods['scale_index']
        scale_factors = self.image_mods['scale_factors']
        scale_value = scale_factors[scale_index]
        # Calculate the new size based on zoom value and default width
        new_width = int(self.image.width() * scale_value)
        new_height = int(self.image.height() * scale_value)

        zoom_size = QtCore.QSize(new_width, new_height)

        # Rescale the pixmap according to the zoom level
        scaled_pixmap = self.image.scaled(
            zoom_size,
            aspectRatioMode=QtCore.Qt.KeepAspectRatio,
            transformMode=QtCore.Qt.SmoothTransformation
        )

        zoom_size = QtCore.QSize(new_width, new_height)
        # Display image
        if self.toggle_resize_status:
            self.image_display.setPixmap(
                scaled_pixmap.scaled(
                    self.size(),
                    aspectRatioMode=QtCore.Qt.KeepAspectRatio,
                    transformMode=QtCore.Qt.SmoothTransformation
                )
            )
        else:
            if self.image_size_cache == [new_width, new_height]:
                self.image_display.setPixmap(
                    self.image.scaled(
                        self.image_display.size(),
                        aspectRatioMode=QtCore.Qt.KeepAspectRatio,
                        transformMode=QtCore.Qt.SmoothTransformation
                    )
                )
            else:
                self.image_display.resize(scaled_pixmap.size())
                self.image_display.setPixmap(scaled_pixmap)
                self.resize(
                    scaled_pixmap.size().width(),
                    scaled_pixmap.size().height()
                )

        self.image_size_cache = [new_width, new_height]
        pixmap_size = self.image_display.pixmap().size()
        self.pixmap_size_cache = [pixmap_size.width(), pixmap_size.height()]

        if self.grid_displayed:
            self.apply_grid()


    def open_grid_settings_dialog(self):
        dialog = GridSettingsDialog(self, default_vertical = self.vertical_lines_grid, default_horizontal = self.horizontal_lines_grid)
        view.init_styles(dialog_grid=dialog)
        if dialog.exec_() == QDialog.Accepted:
            vertical_lines, horizontal_lines = dialog.get_values()
            self.vertical_lines_grid = vertical_lines
            self.horizontal_lines_grid = horizontal_lines

            if self.grid_displayed:
                self.display_image(play_sound=False, update_status = False)

            else:
                self.toggle_grid()

    def toggle_grid(self):

        self.grid_displayed = not self.grid_displayed
        self.display_image(play_sound=False, update_status = False)
        if self.grid_displayed:

            self.apply_grid()
            self.grid_button.setChecked(True)
            
        else:
            # Hide the grid overlay
            self.grid_overlay.hide()
            self.grid_button.setChecked(False)

        

            
    def toggle_resize(self):
        if self.toggle_resize_status is not True:
            # Toggle resize on
            self.toggle_resize_status = True
            self.sizePolicy().setHeightForWidth(False)
            self.lock_scale_button.setChecked(True)
            self.resize_to_image_size(value = -1)
            print("Resize window: On")
        else:
            # Toggle resize off
            self.toggle_resize_status = False
            self.sizePolicy().setHeightForWidth(True)
            self.lock_scale_button.setChecked(False)
            if self.toggle_resize_status:
                self.apply_grid()

            print("Resize window: Off")

            # Resize the display window once
            self.apply_grid()



    def apply_grid(self, grid_opacity=0.6):
        # Calculate the size and position of the displayed image within QLabel
        pixmap = self.image_display.pixmap()

        if pixmap is None:
            return
        # Get the size of the pixmap (image)
        pixmap_size = pixmap.size()

        # Decide which size to use based on resize status
        if self.toggle_resize_status:
            label_size = self.size()  # Use window size when resizing is off
        else:
            label_size = self.image_display.size()  # Use image display size

        # Calculate aspect ratios
        pixmap_aspect_ratio = pixmap_size.width() / pixmap_size.height()
        label_aspect_ratio = label_size.width() / label_size.height()

        # Determine how the image is scaled within the QLabel
        if pixmap_aspect_ratio > label_aspect_ratio:  # Image is scaled by width
            displayed_width = label_size.width()
            displayed_height = displayed_width / pixmap_aspect_ratio
        else:
            # Image is scaled by height
            displayed_height = label_size.height()
            displayed_width = displayed_height * pixmap_aspect_ratio


        offset_x = (label_size.width() - displayed_width) / 2
        offset_y = (label_size.height() - displayed_height) / 2

        # Round the offsets
        offset_x = round(offset_x)
        offset_y = round(offset_y)


        # Check if offset is zero
        if offset_x == 0 and offset_y == 0:
                print("Offsets are zero. Refreshing window and image...")
                # Calculate position to center the image within QLabel
                offset_x = (self.width() - displayed_width) / 2
                offset_y = (self.height() - displayed_height) / 2

                if abs(offset_x) < abs(offset_y):
                    offset_x = 0
                else:

                    offset_y = 0

        if (offset_y > offset_x)or (offset_x == 0 and offset_y == 0):
            label_size = self.image_display.size()
            displayed_width = self.width()
            """
            print("self width ! ",self.width())
            print('label width : ',label_size.width())
            print('pixmap width : ',pixmap_size.width()) 

            print("self height ! ",self.height())
            print('label height : ',label_size.height())
            print('pixmap height : ',pixmap_size.height()) 
            """
            displayed_height = displayed_width / pixmap_aspect_ratio

            offset_y = (label_size.height() - displayed_height) / 2

        # Set the geometry of the grid overlay to cover the displayed image area
        self.grid_overlay.setGeometry(
            int(self.image_display.x() + offset_x),
            int(self.image_display.y() + offset_y),
            int(displayed_width),
            int(displayed_height)
        )

        # Create a pixmap for the grid that matches the displayed image size
        grid_pixmap = QtGui.QPixmap(int(displayed_width), int(displayed_height))
        grid_pixmap.fill(QtCore.Qt.transparent)

        # Create a QPainter to draw the grid on the pixmap
        painter = QtGui.QPainter(grid_pixmap)
        painter.setOpacity(grid_opacity)
        white_pen = QtGui.QPen(QtCore.Qt.white, 1)
        black_pen = QtGui.QPen(QtCore.Qt.black, 1)

        vertical_lines = self.vertical_lines_grid
        horizontal_lines = self.horizontal_lines_grid



        # Calculate the size of each grid cell
        grid_size_x = displayed_width / vertical_lines
        grid_size_y = displayed_height / horizontal_lines


         # Draw vertical lines
        for i in range(1, vertical_lines):
            painter.setPen(white_pen)
            painter.drawLine(int(i * grid_size_x), 0, int(i * grid_size_x), int(displayed_height))
            painter.setPen(black_pen)
            painter.drawLine(int(i * grid_size_x + 1), 0, int(i * grid_size_x + 1), int(displayed_height))

        # Draw horizontal lines
        for j in range(1, horizontal_lines):
            painter.setPen(white_pen)
            painter.drawLine(0, int(j * grid_size_y), int(displayed_width), int(j * grid_size_y))
            painter.setPen(black_pen)
            painter.drawLine(0, int(j * grid_size_y + 1), int(displayed_width), int(j * grid_size_y + 1))

        painter.end()

        # Set the pixmap to the grid overlay label
        self.grid_overlay.setPixmap(grid_pixmap)

        # Debug print for grid overlay geometry
        """ print(f"Grid Overlay - Width: {self.grid_overlay.width()}, Height: {self.grid_overlay.height()}, "
              f"Position: ({self.grid_overlay.x()}, {self.grid_overlay.y()})")"""

        # Show the grid overlay and bring it to the front
        self.grid_overlay.show()
        self.grid_overlay.raise_()  # Ensure it's on top of the image display

    def apply_border(self, show_border=True, border_width=1):
        border_color=self.always_on_top_borde_settings

        if show_border:
            self.border_overlay.show()
            self.border_overlay.raise_()  # Make sure it's above all other widgets

            # Create a pixmap for the border overlay that matches the window size
            border_pixmap = QtGui.QPixmap(self.size())
            border_pixmap.fill(QtCore.Qt.transparent)  # Transparent background

            # Parse the RGB color string into a QColor object
            if isinstance(border_color, str) and border_color.startswith("rgb"):
                # Extract the RGB values from the string
                rgb_values = [int(x) for x in border_color.replace("rgb(", "").replace(")", "").split(",")]
                q_color = QtGui.QColor(*rgb_values)
            else:
                # If it's already a QColor, use it directly
                q_color = QtGui.QColor(border_color)

            # Create a QPainter to draw the border
            painter = QtGui.QPainter(border_pixmap)
            pen = QtGui.QPen(q_color, border_width)
            painter.setPen(pen)

            # Draw the border as a rectangle around the edges
            # Use QRect adjusted to account for the pen width
            painter.drawRect(
                border_width // 2,
                border_width // 2,
                self.width() - border_width,
                self.height() - border_width
            )

            painter.end()

            # Set the pixmap to the border overlay label
            self.border_overlay.setPixmap(border_pixmap)
        else:
            self.border_overlay.hide()


    def convert_to_cvimage(self):
        file_path = self.playlist[self.playlist_position]
        try:
            file = QtCore.QFile(file_path)
            if not file.open(QtCore.QFile.ReadOnly):
                raise FileNotFoundError(f"Unable to open file: {file_path}")
            
            ba = file.readAll()
            ba = ba.data()
            ba = np.frombuffer(ba, np.uint8)  # Use frombuffer for better handling
            file.close()
            
            # Decode the image using OpenCV
            cvimage = cv2.imdecode(ba, cv2.IMREAD_COLOR)  # Use cv2.IMREAD_COLOR for color images
            if cvimage is None:
                raise ValueError(f"Failed to decode image from file: {file_path}")
            return cvimage
        
        except Exception as e:
            print(f"Error converting file to cvimage: {e}")
            return None

    def flip_horizontal(self):
        if self.image_mods['hflip']:
            self.image_mods['hflip'] = False
            self.flip_horizontal_button.setChecked(False)
        else:
            self.image_mods['hflip'] = True
            self.flip_horizontal_button.setChecked(True)
        self.display_image(play_sound=False, update_status = False)

    def flip_vertical(self):
        if self.image_mods['vflip']:
            self.image_mods['vflip'] = False
            self.flip_vertical_button.setChecked(False)
        else:
            self.image_mods['vflip'] = True
            self.flip_vertical_button.setChecked(True)
        self.display_image(play_sound=False, update_status = False)

    def grayscale(self):
        if self.image_mods['grayscale']:
            self.image_mods['grayscale'] = False
            self.grayscale_button.setChecked(False)
        else:
            self.image_mods['grayscale'] = True
            self.grayscale_button.setChecked(True)
        self.display_image(play_sound=False, update_status = False)


    def zoom_plus(self):
        current_scale_index = self.image_mods['scale_index']

        if current_scale_index < len(self.image_mods['scale_factors']) - 1: 
            new_scale_index = current_scale_index + 1
            self.image_mods['scale_index'] = new_scale_index

            #print("Zooming Out" + str(self.image_mods['scale_factors'][new_scale_index]))
            self.display_image(play_sound=False, update_status = False)




            # If the grid is currently displayed, reapply it to the new size
            if self.grid_displayed:
                self.apply_grid()


    def zoom_minus(self):
        current_scale_index = self.image_mods['scale_index']

        if current_scale_index > 0: 
            new_scale_index= current_scale_index - 1
            self.image_mods['scale_index'] = new_scale_index

            self.display_image(play_sound=False, update_status = False)

            self.grid_overlay.setGeometry(self.image_display.geometry())

            # If the grid is currently displayed, reapply it to the new size
            if self.grid_displayed:
                self.apply_grid()






    def toggle_always_on_top(self):
        if not self.toggle_always_on_top_status:
            self.toggle_always_on_top_status = True
            self.setWindowFlag(
                QtCore.Qt.X11BypassWindowManagerHint,
                self.toggle_always_on_top_status
            )
            self.setWindowFlag(
                QtCore.Qt.WindowStaysOnTopHint,
                self.toggle_always_on_top_status
            )
            
            # Apply the border using the overlay
            self.apply_border(True)
            print('Always on top: On')
        else:
            self.toggle_always_on_top_status = False
            self.setWindowFlag(
                QtCore.Qt.WindowStaysOnTopHint,
                self.toggle_always_on_top_status
            )

            # Remove the border
            self.apply_border(False)
            print('Always on top: Off')
        
        self.show()

            ##################

    def load_entry(self):
        """
        Load the entry based on the current session settings.
        """
        # Check if the window is still valid
        if sip.isdeleted(self):
            print("SessionDisplay object has been deleted.")
            return

        if self.entry['current'] >= self.entry['total']:
            self.load_last_entry()
            return

        self.entry['time'] = int(self.schedule[self.entry['current']][2])
        self.timer.stop()
        self.time_seconds = self.entry['time']
        self.timer.start(500)
        self.entry['amount of items'] = int(self.schedule[self.entry['current']][1]) - 1
        self.display_image()

    def load_next_image(self):
        """
        Loads the next image in the playlist or displays a black screen if at the end.
        Resets the timer for a new image.
        """
        self.image_mods['scale_index'] = self.image_mods['default_scale_index']

        # Check if we are at the last image
        if self.playlist_position < len(self.playlist) - 1:
            self.playlist_position += 1
            self.rotation_index = 0
            self.new_entry = False
            self.reset_timer()  # Reset the timer for a new image
            self.display_image()
            
        else:
            self.display_end_screen()  # Display black screen when at the end

        self.update_session_info()


        # If there are any other buttons to untoggle, add them here

    def load_prev_image(self):
        """
        Loads the previous image in the playlist or does nothing if at the start.
        """
        self.image_mods['scale_index'] = self.image_mods['default_scale_index']

        # Check if we are at the first image
        if self.playlist_position > 0:
            self.playlist_position -= 1
            self.rotation_index = 0
            self.new_entry = False
            self.display_image()  # Display the previous image
            
        else:
            return
        
        self.update_session_info()



    def reset_timer(self):
        """
        Resets the timer to the initial time for the current image entry.
        """
        self.timer.stop()
        self.entry['time'] = int(self.schedule[self.entry['current']][2])  # Reset to the entry's time
        self.time_seconds = self.entry['time']
        self.timer.start(500)
        self.pause_timer.setChecked(False)
        self.timer_display.setFrameShape(QFrame.NoFrame)
        self.update_timer_display()

    def display_end_screen(self):
        """
        Display an end screen with a very small or transparent image and change the text to 'Done'.
        """
        # Create a transparent 1x1 pixel image
        transparent_pixmap = QtGui.QPixmap(1, 1)
        transparent_pixmap.fill(QtCore.Qt.transparent)

        # Set the image display to show the transparent image
        self.image_display.setPixmap(transparent_pixmap)

        # Stop the timer
        self.timer.stop()

        # Reset image modifications or any other state
        self.reset_image_mods()

        # Change the timer display text
        self.timer_display.setText('Done!')

    def reset_image_mods(self):
        self.init_image_mods()

        self.grid_button.setChecked(False)
        self.grayscale_button.setChecked(False)
        self.flip_horizontal_button.setChecked(False)
        self.flip_vertical_button.setChecked(False)
        self.grid_displayed = False
        self.grid_overlay.hide()
        self.grid_button.setChecked(False)


    def toggle_resize(self):
        if not self.toggle_resize_status:
            # Toggle resize on
            self.toggle_resize_status = True
            self.sizePolicy().setHeightForWidth(False)
            self.lock_scale_button.setChecked(True)
            print("Resize window: On")
        else:
            # Toggle resize off
            self.toggle_resize_status = False
            self.sizePolicy().setHeightForWidth(True)
            self.lock_scale_button.setChecked(False)
            print("Resize window: Off")

            # Refresh the display window by resizing it to the image size

    def resize_to_image_size(self):
        """
        Resize the display window to fit the current image size.
        """
        # Assuming 'self.image' holds the current image pixmap
        if self.image:
            # Get the size of the current image
            image_size = self.image.size()

            # Resize the window to the image size
            self.resize(image_size.width(), image_size.height())


    def update_timer_display(self):
        """
        Update the timer display based on the remaining time.
        """
        hours = int(self.time_seconds / 3600)
        minutes = int((self.time_seconds % 3600) / 60)
        seconds = int(self.time_seconds % 60)

        self.hr_list = self.format_time_unit(hours)
        self.minutes_list = self.format_time_unit(minutes)
        self.sec = self.format_time_unit(seconds)

        self.display_time()


    def update_session_info(self):
        """
        Update the session info display based on the current image.
        """
        if hasattr(self, 'session_info') and not sip.isdeleted(self.session_info):
            self.session_info.setText(
                f'{self.playlist_position + 1}/{len(self.playlist)}'  # Update counter here
            )


        #############

    def update_entry_time(self):
        """Update the entry time and time_seconds."""
        self.entry['time'] = int(self.schedule[self.entry['current']][2])
        self.time_seconds = self.entry['time']

    def stop_timer(self):
        """Stop the timer."""
        self.timer.stop()

    def start_timer(self):
        """Start the timer."""
        self.timer.start(500)

    def countdown(self):
        """Countdown timer with sound alerts and image transitions."""
        # Check if the window is still valid
        if sip.isdeleted(self):
            self.timer.stop()
            return

        self.update_timer_display()
        if self.entry['time'] >= 30 and self.time_seconds == self.entry['time'] // 2:
            self.play_sound("halfway.mp3")

        if self.time_seconds <= 10:
            self.handle_final_seconds()

        if self.time_seconds == 0:
            QTest.qWait(500)
            self.load_next_image()
            return

        self.time_seconds -= 0.5

    def handle_final_seconds(self):
        """Handle the sound alerts and flags for the final countdown seconds."""
        if not self.new_entry and not self.end_of_entry:
            if self.time_seconds == 10:
                self.play_sound("first_alert.mp3")
            elif self.time_seconds == 5:
                self.play_sound("second_alert.mp3")
            elif self.time_seconds == 0.5:
                self.play_sound("third_alert.mp3")
        else:
            self.new_entry = False
            self.end_of_entry = False


    def play_sound(self, filename):
        """Play a sound file."""
        mixer.music.load(os.path.join(self.sounds_dir, filename))
        mixer.music.play()

    def update_timer_display(self):
        """Update the timer display based on the remaining time."""
        hours = int(self.time_seconds / 3600)
        minutes = int((self.time_seconds % 3600) / 60)
        seconds = int(self.time_seconds % 60)

        self.hr_list = self.format_time_unit(hours)
        self.minutes_list = self.format_time_unit(minutes)
        self.sec = self.format_time_unit(seconds)

        self.display_time()

    def format_time_unit(self, value):
        """Format a time unit to be at least two digits."""
        return list(f"{value:02}")

    def pause(self):
        """Pause or resume the timer."""
        if self.timer.isActive():
            self.stop_timer()
            self.timer_display.setFrameShape(QFrame.WinPanel)
            self.pause_timer.setChecked(True)
            QTest.qWait(20)
        else:
            self.timer_display.setFrameShape(QFrame.NoFrame)
            self.pause_timer.setChecked(False)
            self.start_timer()

        self.display_time()


    def display_time(self):
        """Displays the amount of time left depending on how many seconds are left."""
        if not hasattr(self, 'timer_display') or self.timer_display is None:
            return  # Exit if timer_display doesn't exist or has been deleted

        # Ensure the QLabel has not been deleted
        if not sip.isdeleted(self.timer_display):
            if self.time_seconds >= 3600:
                # Hour or longer
                self.timer_display.setText(
                    f"{self.hr_list[0]}{self.hr_list[1]}:"
                    f"{self.minutes_list[0]}{self.minutes_list[1]}:"
                    f"{self.sec[0]}{self.sec[1]}"
                )
            elif self.time_seconds >= 60:
                # Minute or longer
                self.timer_display.setText(
                    f"{self.minutes_list[0]}{self.minutes_list[1]}:"
                    f"{self.sec[0]}{self.sec[1]}"
                )
            else:
                # Less than a minute left
                self.timer_display.setText(f"{self.sec[0]}{self.sec[1]}")


    def add_seconds(self, seconds):
        """Add seconds to the current timer."""
        self.time_seconds += seconds
        self.update_timer_display()

    def add_30_seconds(self):
        self.add_seconds(30)

    def add_60_seconds(self):
        self.add_seconds(60)

    def restart_timer(self):
        """Restart the timer with the current entry's time."""
        self.time_seconds = int(self.schedule[self.entry['current']][2])
        self.update_timer_display()

class GridSettingsDialog(QDialog):
    def __init__(self, parent=None,default_vertical = 4, default_horizontal = 4):
        super().__init__(parent)
        self.setWindowTitle("Grid Settings")

        # Remove the question mark from the title bar
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)

        # Layout for the dialog
        layout = QVBoxLayout()

        # Input fields for vertical and horizontal lines
        self.vertical_input = QSpinBox()
        self.vertical_input.setMinimum(1)
        self.vertical_input.setMaximum(20)
        self.vertical_input.setValue(default_vertical)  # Default value

        self.horizontal_input = QSpinBox()
        self.horizontal_input.setMinimum(1)
        self.horizontal_input.setMaximum(20)
        self.horizontal_input.setValue(default_horizontal)  # Default value

        # Labels
        layout.addWidget(QLabel("Vertical:"))
        layout.addWidget(self.vertical_input)
        layout.addWidget(QLabel("Horizontal:"))
        layout.addWidget(self.horizontal_input)

        # Create OK and Cancel buttons
        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Cancel")


        # Connect buttons
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)

        # Add buttons to a horizontal layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)

        # Add button layout to the main layout
        layout.addLayout(button_layout)

        self.setLayout(layout)
    def get_values(self):
        return self.vertical_input.value(), self.horizontal_input.value()


class MaxLengthDelegate(QStyledItemDelegate):
    def __init__(self, max_length=60, parent=None):
        super().__init__(parent)
        self.max_length = max_length

    def createEditor(self, parent, option, index):
        # Create a QLineEdit editor
        editor = QLineEdit(parent)
        # Set the maximum length of characters allowed
        editor.setMaxLength(self.max_length)
        return editor

            # Subclass to enable multifolder selection.


class MultiFolderSelector(QtWidgets.QDialog):
    def __init__(self, parent=None, preset_name="preset_1", stylesheet=""):
        super(MultiFolderSelector, self).__init__(parent)
        self.setWindowTitle("Select Folders")

        self.setMinimumWidth(400)
        self.setMinimumHeight(300)

        # Remove the question mark button by setting the window flags
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)

        # Initialize selected folders list
        self.selected_folders = []

        # Layout
        layout = QtWidgets.QVBoxLayout(self)

        # List widget to display selected folders
        self.list_widget = QtWidgets.QListWidget(self)
        layout.addWidget(self.list_widget)

        # Preset Name Input (below the list widget)
        self.preset_name_edit = QtWidgets.QLineEdit(self)
        self.preset_name_edit.setPlaceholderText("Enter Preset Name")
        self.preset_name_edit.setText(preset_name)
        layout.addWidget(self.preset_name_edit)

        # Buttons
        button_layout = QtWidgets.QHBoxLayout()

        # Only one button for adding folders, renamed to "Add Folder(s)"
        self.add_folders_button = QtWidgets.QPushButton("Add Folder(s)", self)
        self.add_folders_button.clicked.connect(self.multi_select_folders)
        self.add_folders_button.setAutoDefault(False)
        button_layout.addWidget(self.add_folders_button)

        self.remove_button = QtWidgets.QPushButton("Remove folder", self)
        self.remove_button.clicked.connect(self.remove_folder)
        self.remove_button.setAutoDefault(False)
        button_layout.addWidget(self.remove_button)

        self.ok_button = QtWidgets.QPushButton("OK", self)
        self.ok_button.clicked.connect(self.accept)
        self.ok_button.setAutoDefault(True)
        button_layout.addWidget(self.ok_button)

        self.cancel_button = QtWidgets.QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.reject)
        self.cancel_button.setAutoDefault(False)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)

        # Apply passed stylesheet
        self.setStyleSheet(stylesheet)

        # Set the default focus to the list widget or any other widget except the preset name edit
        self.list_widget.setFocus()  # Set focus to the list widget instead of the text input

        # Ensure Enter triggers OK button
        self.ok_button.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.init_message_boxes()

    def init_message_boxes(self):
        """Initialize custom message box settings."""
        self.message_box = QtWidgets.QMessageBox(self)
        self.message_box.setIcon(QtWidgets.QMessageBox.NoIcon)  # Set to no icon by default
    
    def show_info_message(self, title, message):
        """Show an information message box without an icon."""
        self.message_box.setWindowTitle(title)
        self.message_box.setText(message)
        self.message_box.exec_()

    def format_folder_path(self, folder_path):
        """Format the folder path to display only the end part."""
        # Normalize the path to use backslashes
        normalized_path = folder_path.replace('/', os.sep).replace('\\', os.sep)

        # Split the normalized path into parts
        parts = normalized_path.split(os.sep)

        # If there are more than 3 parts, show the last three parts
        if len(parts) > 3:
            return '...\\' + os.sep.join(parts[-3:])  # Show the last three parts of the path
        return normalized_path  # If less than or equal, return as is

      
    def multi_select_folders(self):
        file_dialog = QtWidgets.QFileDialog(self)
        file_dialog.setFileMode(QtWidgets.QFileDialog.DirectoryOnly)
        file_dialog.setOption(QtWidgets.QFileDialog.DontUseNativeDialog, True)
        file_dialog.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)

        file_view = file_dialog.findChild(QtWidgets.QListView, 'listView')
        if file_view:
            file_view.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)

        f_tree_view = file_dialog.findChild(QtWidgets.QTreeView)
        if f_tree_view:
            f_tree_view.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)

            # Customize the columns
            header = f_tree_view.header()
            header.setStretchLastSection(True)  # Enable stretching for the last column
            header.setSectionsMovable(True)    # Allow columns to be reordered
            header.setSectionsClickable(True)  # Allow column header interaction
            header.setSectionResizeMode(QtWidgets.QHeaderView.Interactive)  # Enable resizing for all columns

            # Set column visibility for desired columns: Name, Size, Type, Date Modified
            for col_index in range(header.count()):
                if col_index not in [0, 1, 2, 3]:  # Adjust these indices to match your desired columns
                    header.hideSection(col_index)

        last_directory = None

        def update_last_directory(directory):
            nonlocal last_directory
            last_directory = directory

        file_dialog.directoryEntered.connect(update_last_directory)

        if file_dialog.exec():
            folders = file_dialog.selectedFiles()
            filtered_folders = [folder for folder in folders if folder != last_directory]
            for folder in filtered_folders:
                if folder and folder not in self.selected_folders:
                    self.selected_folders.append(folder)
                    formatted_path = self.format_folder_path(folder)
                    self.list_widget.addItem(formatted_path)



    def remove_folder(self):
        selected_items = self.list_widget.selectedItems()
        if selected_items:
            for item in selected_items:
                # Find the full path corresponding to the formatted path in the list
                formatted_path = item.text()
                full_path = None

                # Iterate through the selected_folders to find the matching full path
                for folder in self.selected_folders:
                    if self.format_folder_path(folder) == formatted_path:
                        full_path = folder
                        break

                # If full path is found, remove it
                if full_path:
                    self.selected_folders.remove(full_path)

                # Remove the item from the list widget
                self.list_widget.takeItem(self.list_widget.row(item))

    def get_selected_folders(self):
        return self.selected_folders

    def get_preset_name(self):
        return self.preset_name_edit.text()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
            # Trigger OK button click
            self.ok_button.click()
        else:
            super(MultiFolderSelector, self).keyPressEvent(event)

    def accept(self):
        """Accept the dialog and check for existing presets before processing."""
        preset_name = self.get_preset_name().strip()

        # Check if the preset name already exists
        images_presets_dir = self.parent().images_presets_dir  # Assume parent has this attribute
        preset_filename = f'{preset_name}.txt'
        preset_filepath = os.path.join(images_presets_dir, preset_filename)

        if os.path.exists(preset_filepath):
            self.show_info_message('Duplicate Preset', f'The preset "{preset_name}" already exists. Please choose a different name.')
            return  # Do not accept the dialog

        super(MultiFolderSelector, self).accept()





# Custom QTableWidget that enforces at least one selected row
class EnforcedSelectionTable(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_row = 0
        # Install event filter to catch mouse clicks
        self.viewport().installEventFilter(self)
        
    def selectionCommand(self, index, event):
        # This method gets called whenever selection is about to change
        # Get the current selection command
        command = super().selectionCommand(index, event)
        
        # If this would clear selection, adjust the command
        if command == QItemSelectionModel.Clear:
            # Store the last selected row
            selected_rows = self.selectionModel().selectedRows()
            if selected_rows:
                self.current_row = selected_rows[0].row()
            return QItemSelectionModel.NoUpdate
            
        return command
        
    def mousePressEvent(self, event):
        # Store the current selected row before handling the mouse press
        selected_rows = self.selectionModel().selectedRows()
        if selected_rows:
            self.current_row = selected_rows[0].row()
        
        # Let QTableWidget handle the mouse press
        super().mousePressEvent(event)
        
        # Ensure we still have a selection after the event
        if not self.selectionModel().selectedRows():
            # No row is selected, re-select the previous row
            self.selectRow(self.current_row)
            
    def mouseReleaseEvent(self, event):
        # Store the current selected row
        selected_rows = self.selectionModel().selectedRows()
        if selected_rows:
            self.current_row = selected_rows[0].row()
            
        # Let QTableWidget handle the mouse release
        super().mouseReleaseEvent(event)
        
        # Check if we have a selection after the event
        if not self.selectionModel().selectedRows():
            # No row is selected, re-select the previous row
            self.selectRow(self.current_row)
            
    def viewportEvent(self, event):
        # Additional protection for viewport events
        result = super().viewportEvent(event)
        
        # After any viewport event, check if we have a selection
        if event.type() in (QEvent.MouseButtonPress, QEvent.MouseButtonRelease, QEvent.MouseButtonDblClick):
            if not self.selectionModel().selectedRows():
                self.selectRow(self.current_row)
                
        return result


class LabelManagerDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, labels_dict=None):
        super().__init__(parent)
        self.parent = parent
        self.labels_dict = labels_dict or {"Default": "#00000000"}
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Label Manager")
        self.setMinimumSize(400, 300)
        
        layout = QVBoxLayout()
        
        # Label list
        self.label_list = EnforcedSelectionTable()  # Using custom table widget
        self.label_list.setColumnCount(2)
        self.label_list.setHorizontalHeaderLabels(["Label Name", "Color"])
        self.label_list.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.label_list.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Fixed)
        self.label_list.horizontalHeader().setFocusPolicy(Qt.NoFocus)
        self.label_list.setColumnWidth(1, 80)
        self.label_list.setEditTriggers(QTableWidget.NoEditTriggers)
        self.label_list.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.label_list.verticalHeader().setVisible(False)
        # Populate the list
        self.refresh_label_list()
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        self.add_button = QPushButton("Add Label")
        self.edit_button = QPushButton("Edit Label")
        self.delete_button = QPushButton("Delete Label")
        
        buttons_layout.addWidget(self.add_button)
        buttons_layout.addWidget(self.edit_button)
        buttons_layout.addWidget(self.delete_button)
        
        # Connect signals
        self.add_button.clicked.connect(self.add_label)
        self.edit_button.clicked.connect(self.edit_label)
        self.delete_button.clicked.connect(self.delete_label)
        # Add selection change handler to control the delete button state
        self.label_list.itemSelectionChanged.connect(self.update_button_states)
            
        # Dialog buttons
        dialog_buttons = QHBoxLayout()
        self.ok_button = QPushButton("OK")
        
        dialog_buttons.addStretch()
        dialog_buttons.addWidget(self.ok_button)
        
        self.ok_button.clicked.connect(self.accept)
        
        # Add everything to main layout
        layout.addWidget(self.label_list)
        layout.addLayout(buttons_layout)
        layout.addLayout(dialog_buttons)
        
        self.setLayout(layout)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        color_delegate = LabelColorDelegate(self.label_list)
        self.label_list.setItemDelegateForColumn(1, color_delegate)
        
        # Select the first row by default
        self.label_list.selectRow(0)
        # Initially update button states based on the first row selection
        self.update_button_states()
        self.init_message_boxes()

    def update_button_states(self):
        """Update button states based on current selection"""
        current_row = self.label_list.currentRow()
        if current_row >= 0:
            current_name = self.label_list.item(current_row, 0).text()
            # Disable delete button if "Default" is selected
            self.delete_button.setEnabled(current_name != "Default")
        else:
            # If nothing is selected, disable delete button
            self.delete_button.setEnabled(False)

    def init_message_boxes(self):
        """Initialize custom message box settings."""
        self.message_box = QtWidgets.QMessageBox(self)
        self.message_box.setIcon(QtWidgets.QMessageBox.NoIcon)  # Set to no icon by default
    
    def show_info_message(self, title, message):
        """Show an information message box without an icon."""
        self.message_box.setWindowTitle(title)
        self.message_box.setText(message)
        self.message_box.exec_()



    def refresh_label_list(self):
        self.label_list.setRowCount(0)
        
        for name, color in self.labels_dict.items():
            row = self.label_list.rowCount()
            self.label_list.insertRow(row)
            
            # Label name
            name_item = QTableWidgetItem(name)
            self.label_list.setItem(row, 0, name_item)
            
            # Color swatch
            color_item = QTableWidgetItem("")
            color_item.setBackground(QColor(color))
            self.label_list.setItem(row, 1, color_item)
    
    def add_label(self):
        name, ok = QInputDialog.getText(self, "New Label", "Enter label name:")
        if ok and name:
            if name in self.labels_dict:
                self.show_info_message('Duplicate', "Label name already exists.")
                return
            
            color = QColorDialog.getColor()
            if color.isValid():
                self.labels_dict[name] = color.name()
                self.refresh_label_list()
    
    def edit_label(self):
        current_row = self.label_list.currentRow()
        if current_row < 0:
            self.show_info_message("No Selection", "Please select a label to edit.")
            return
        
        current_name = self.label_list.item(current_row, 0).text()
        
        # Don't allow editing the Default label
        if current_name == "Default":
            color = QColorDialog.getColor(QColor(self.labels_dict["Default"]))
            if color.isValid():
                self.labels_dict["Default"] = color.name()
                self.refresh_label_list()
                print("Color Updated", "Default label color has been updated.")
            return
        
        new_name, ok = QInputDialog.getText(self, "Edit Label", "Enter new label name:", text=current_name)
        if ok and new_name:
            if new_name != current_name and new_name in self.labels_dict:
                self.show_info_message("Duplicate", "Label name already exists.")
                return
            
            color = QColorDialog.getColor(QColor(self.labels_dict[current_name]))
            if color.isValid():
                # If name changed, we need to update any presets using this label
                if new_name != current_name:
                    # Store the color value
                    color_value = self.labels_dict[current_name]
                    # Delete the old key
                    del self.labels_dict[current_name]
                    # Create new key with same color
                    self.labels_dict[new_name] = color_value
                    
                    # Update preset assignments
                    if hasattr(self.parent, 'preset_labels_dictionary'):
                        for preset, label in self.parent.preset_labels_dictionary.items():
                            if label == current_name:
                                self.parent.preset_labels_dictionary[preset] = new_name
                
                # Update the color value
                self.labels_dict[new_name] = color.name()
                self.refresh_label_list()
    
    def delete_label(self):
        current_row = self.label_list.currentRow()
        if current_row < 0:
            self.show_info_message("No Selection", "Please select a label to delete.")
            return
        
        current_name = self.label_list.item(current_row, 0).text()
        
        # Don't allow deleting the Default label
        if current_name == "Default":
            self.show_info_message("Reserved", "Cannot delete the Default label.")
            return
        

        # Remove the label
        del self.labels_dict[current_name]
        
        # Reassign any presets using this label to Default
        if hasattr(self.parent, 'preset_labels_dictionary'):
            for preset, label in self.parent.preset_labels_dictionary.items():
                if label == current_name:
                    self.parent.preset_labels_dictionary[preset] = "Default"
        
        self.refresh_label_list()
            
    def get_labels(self):
        return self.labels_dict



class ThemeSelectorDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, theme_presets_dir="", session_settings_file=""):
        super(ThemeSelectorDialog, self).__init__(parent)
        self.setWindowTitle("Select Theme")
        self.setMinimumWidth(300)  
        self.setMinimumHeight(100)  

        self.setMaximumWidth(300)  
        self.setMaximumHeight(150)  
        # Remove the question mark button by setting the window flags
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)

        self.theme_presets_dir = theme_presets_dir
        self.current_theme = self.load_current_theme(session_settings_file)


        # Initialize selected theme
        self.selected_theme = None

        # Layout
        layout = QtWidgets.QVBoxLayout(self)

        # List widget to display theme files
        self.list_widget = QtWidgets.QListWidget(self)

        layout.addWidget(self.list_widget)

        
        

        # Populate list with theme files
        self.load_theme_files()

        # Buttons
        button_layout = QtWidgets.QHBoxLayout()
        self.ok_button = QtWidgets.QPushButton("OK", self)
        self.ok_button.clicked.connect(self.accept)
        self.ok_button.setAutoDefault(True)
        button_layout.addWidget(self.ok_button)

        self.cancel_button = QtWidgets.QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.reject)
        self.cancel_button.setAutoDefault(False)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)

        # Set the default focus to the list widget
        self.list_widget.setFocus()  # Set focus to the list widget

        # Ensure Enter triggers OK button
        self.ok_button.setFocusPolicy(QtCore.Qt.StrongFocus)

        # Connect double click to select theme
        self.list_widget.itemDoubleClicked.connect(self.accept)

    def load_current_theme(self, session_settings_file):
        """Load the current theme from the session settings file."""
        if not os.path.exists(session_settings_file):
            return ""  # Default if settings file does not exist

        with open(session_settings_file, 'r') as file:
            settings = json.load(file)
        
        return settings.get("theme_settings", "").replace('.txt', '')

    def load_theme_files(self):
        """Load theme files from the theme presets directory and set the current theme as selected."""
        theme_files = [f for f in os.listdir(self.theme_presets_dir) if f.endswith('.txt')]

        # Separate the default theme, if it exists
        default_theme = "default_theme.txt"
        other_themes = [f for f in theme_files if f != default_theme]

        # Sort the other themes alphabetically
        sorted_themes = sorted([f.replace('.txt', '') for f in other_themes])

        # Add the default theme at the top
        if default_theme in theme_files:
            sorted_themes.insert(0, default_theme.replace('.txt', ''))

        # Add themes to the list widget
        for theme_name in sorted_themes:
            item = QtWidgets.QListWidgetItem(theme_name)

            if theme_name == self.current_theme:
                item.setSelected(True)

                self.list_widget.setCurrentItem(item)  # Update the current item to reflect the selection
            self.list_widget.addItem(item)

    def accept(self):
        """Accept the dialog and set the selected theme."""
        selected_items = self.list_widget.selectedItems()
        if selected_items:
            self.selected_theme = selected_items[0].text() + ".txt" # Add back the .txt extension

        super(ThemeSelectorDialog, self).accept()

    def get_selected_theme(self):
        """Get the selected theme."""
        return self.selected_theme 



if __name__ == "__main__":
    import sys
    import argparse
    import json
    import random
    from PyQt5 import QtWidgets

    app = QtWidgets.QApplication(sys.argv)
    parser = argparse.ArgumentParser(description="Image Session Tool")
    subparsers = parser.add_subparsers(dest="command")

    # Subparser for "create_preset"
    create_preset_parser = subparsers.add_parser("create_preset", help="Open a folder and process its contents")
    create_preset_parser.add_argument("-folder_list", required=True, nargs="+", help="List of folder paths to use instead of dialog")
    create_preset_parser.add_argument("-preset_name", default="preset_output", help="Name of the preset to use instead of dialog")
    create_preset_parser.add_argument("-output_folder", default=None, help="Folder to save the preset file. Defaults to images_presets_dir if not provided.")

    # Subparser for "update_preset"
    update_preset_parser = subparsers.add_parser("update_preset", help="Update a preset with refreshed file paths")
    update_preset_parser.add_argument("-preset_path", required=True, help="Path of the preset to update")

    # Subparser for "start_session_from_files"
    start_session_parser = subparsers.add_parser("start_session_from_files", help="Start session from files")
    start_session_parser.add_argument("-image_preset_path", help="Path to the image preset file")
    start_session_parser.add_argument("-session_preset_path", help="Path to the session preset file")
    start_session_parser.add_argument("-randomize_settings", type=lambda x: x.lower() == "true", default=True,
                                       help="Randomize settings (True/False)")

    # Parse arguments
    args = parser.parse_args()

    if args.command == "create_preset":
        view = MainApp(show_main_window=False)
        folder_list = args.folder_list
        preset_name = args.preset_name
        output_folder = args.output_folder
        view.create_preset(folder_list=folder_list, preset_name=preset_name, output_folder=output_folder, is_gui=False)
        app.quit()

    elif args.command == "update_preset":
        view = MainApp(show_main_window=False)
        preset_path = args.preset_path
        view.update_preset(preset_path=preset_path, is_gui=False)

    elif args.command == "start_session_from_files":
        view = MainApp(show_main_window=False)
        image_preset_path = args.image_preset_path
        session_preset_path = args.session_preset_path
        randomize_settings = args.randomize_settings
        view.start_session_from_files(image_preset_path=image_preset_path,
                                      session_preset_path=session_preset_path,
                                      randomize_settings=randomize_settings)
        sys.exit(app.exec_())

    else:
        # Default behavior: Start the GUI
        view = MainApp(show_main_window=True)
        sys.exit(app.exec_())
