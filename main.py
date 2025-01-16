import sys
import json
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                            QComboBox, QTextEdit, QCheckBox, QGroupBox,
                            QScrollArea, QMessageBox, QFileDialog, QSplitter)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QPalette, QColor
from hugchat import hugchat
from hugchat.login import Login

class LLMWorker(QThread):
    finished = pyqtSignal(str, str)  
    
    def __init__(self, cookies, model_index, model_id, prompt, response_length):
        super().__init__()
        self.cookies = cookies
        self.model_index = model_index
        self.model_id = model_id
        self.prompt = prompt
        self.response_length = response_length
        
    def run(self):
        try:
            chatbot = hugchat.ChatBot(cookies=self.cookies)
            chatbot.switch_llm(self.model_index)
            
            length_params = {
                "short": {"max_length": 100},
                "medium": {"max_length": 300},
                "detailed": {"max_length": 1000}
            }
            
            response = chatbot.chat(
                self.prompt,
                **length_params.get(self.response_length, {"max_length": 300})
            ).wait_until_done()
            
            
            formatted_response = self.format_response(response)
            self.finished.emit(self.model_id, formatted_response)
        except Exception as e:
            self.finished.emit(self.model_id, f"Error: {str(e)}")
    
    def format_response(self, response):
       
        lines = response.split('\n')
        formatted_lines = []
        
        for line in lines:
            
            if line.startswith('#'):
                line = line.strip('# ').upper()
                formatted_lines.append(f"\n=== {line} ===\n")
           
            elif line.strip().startswith('-'):
                formatted_lines.append(f"  • {line.strip('- ')}")
          
            elif line.strip().startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.')):
                formatted_lines.append(f"  {line.strip()}")
            else:
                formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.cookies = None
        self.available_models = []
        self.model_map = {}
        self.workers = []
        self.setup_ui()
    
        
    def setup_ui(self):
        self.setWindowTitle("LLM Comparison Dashboard")
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QLabel {
                color: #333333;
                font-family: 'Segoe UI';
            }
            QPushButton {
                background-color: #2196F3;
                color: #FFFFFF;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 14px;
                font-family: 'Roboto', sans-serif;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }

            QLineEdit, QTextEdit {
                border: 1px solid #BDBDBD;
                border-radius: 5px;
                padding: 10px;
                background-color: #FAFAFA;
                font-family: 'Roboto', sans-serif;
                font-size: 13px;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 1px solid #2196F3;
            }

            QComboBox {
                border: 1px solid #BDBDBD;
                border-radius: 4px;
                padding: 8px;
                background-color: white;
                font-family: 'Segoe UI';
            }
            QScrollArea {
                border: none;
                background-color: #FAFAFA;
            }

            QGroupBox {
                border: 1px solid #BDBDBD;
                border-radius: 8px;
                margin-top: 15px;
                font-family: 'Segoe UI';
                font-weight: bold;
                padding: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 5px;
            }
        """)
        
        # Define Material Design Colors
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#ffffff"))  
        palette.setColor(QPalette.ColorRole.WindowText, QColor("#212121")) 
        palette.setColor(QPalette.ColorRole.Base, QColor("#f5f5f5"))  
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#eeeeee"))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor("#000000"))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor("#ffffff"))
        palette.setColor(QPalette.ColorRole.Text, QColor("#212121"))
        palette.setColor(QPalette.ColorRole.Button, QColor("#2196F3"))  
        palette.setColor(QPalette.ColorRole.ButtonText, QColor("#ffffff"))
        palette.setColor(QPalette.ColorRole.Highlight, QColor("#448AFF"))  
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))

        self.setPalette(palette)

        # Main container
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create main splitter
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        self.setCentralWidget(main_splitter)
        
        # Left side - Control Panel
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(10, 10, 10, 10)
        left_layout.setSpacing(10)
        
        # Login section
        login_group = QGroupBox("Login")
        login_layout = QVBoxLayout()
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        login_button = QPushButton("Login")
        login_button.clicked.connect(self.handle_login)
        
        login_layout.addWidget(self.email_input)
        login_layout.addWidget(self.password_input)
        login_layout.addWidget(login_button)
        login_group.setLayout(login_layout)
        
        # Model selection section
        model_group = QGroupBox("Model Selection")
        model_layout = QVBoxLayout()
        
        self.model_checkboxes = []
        self.model_layout = QVBoxLayout()
        model_layout.addLayout(self.model_layout)
        model_group.setLayout(model_layout)
        
        # Input section
        input_group = QGroupBox("Input")
        input_layout = QVBoxLayout()
        
        self.prompt_input = QTextEdit()
        self.prompt_input.setPlaceholderText("Enter your prompt here...")
        self.prompt_input.setMinimumHeight(100)
        
        length_layout = QHBoxLayout()
        length_label = QLabel("Response Length:")
        self.length_combo = QComboBox()
        self.length_combo.addItems(["short", "medium", "detailed"])
        length_layout.addWidget(length_label)
        length_layout.addWidget(self.length_combo)
        
        generate_button = QPushButton("Generate Responses")
        generate_button.clicked.connect(self.generate_responses)
        
        save_button = QPushButton("Save Responses")
        save_button.clicked.connect(self.save_responses)
        
        input_layout.addWidget(self.prompt_input)
        input_layout.addLayout(length_layout)
        input_layout.addWidget(generate_button)
        input_layout.addWidget(save_button)
        input_group.setLayout(input_layout)
        
       
        left_layout.addWidget(login_group)
        left_layout.addWidget(model_group)
        left_layout.addWidget(input_group)
        left_layout.addStretch()
        
       
        right_widget = QWidget()
        self.response_layout = QVBoxLayout(right_widget)
        self.response_layout.setContentsMargins(10, 10, 10, 10)
        self.response_layout.setSpacing(10)
        
       
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(right_widget)
        
      
        main_splitter.addWidget(left_widget)
        main_splitter.addWidget(scroll_area)
        
        
        main_splitter.setSizes([300, 700])  
        
        
        self.resize(1200, 800)
        
    def handle_login(self):
        try:
            email = self.email_input.text()
            password = self.password_input.text()
            
            sign = Login(email, password)
            self.cookies = sign.login()
            
            chatbot = hugchat.ChatBot(cookies=self.cookies.get_dict())
            self.available_models = chatbot.get_available_llm_models()
            
            for checkbox in self.model_checkboxes:
                checkbox.deleteLater()
            self.model_checkboxes.clear()
            
            for i, model in enumerate(self.available_models):
                model_id = f"model_{i}"
                model_name = f"Model {i+1}: {str(model)}"
                self.model_map[model_id] = i
                
                checkbox = QCheckBox(model_name)
                checkbox.setProperty("model_id", model_id)
                self.model_checkboxes.append(checkbox)
                self.model_layout.addWidget(checkbox)
            
            QMessageBox.information(self, "Success", "Login successful!")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Login failed: {str(e)}")
    
    def generate_responses(self):
        if not self.cookies:
            QMessageBox.warning(self, "Warning", "Please login first!")
            return
            
       
        for i in reversed(range(self.response_layout.count())): 
            self.response_layout.itemAt(i).widget().deleteLater()
            
        selected_models = []
        for checkbox in self.model_checkboxes:
            if checkbox.isChecked():
                model_id = checkbox.property("model_id")
                model_index = self.model_map[model_id]
                selected_models.append((model_id, model_index))
        
        
        response_height = min(600, int(800 / len(selected_models)))
        
      
        self.response_widgets = {}
        for model_id, model_index in selected_models:
            response_group = QGroupBox(f"Response from Model {model_index + 1}")
            response_layout = QVBoxLayout()
            
            response_text = QTextEdit()
            response_text.setReadOnly(True)
            response_text.setMinimumHeight(response_height)
            response_text.setPlaceholderText(f"Waiting for response...")
            response_text.setFont(QFont("Segoe UI", 10))
            
            response_layout.addWidget(response_text)
            response_group.setLayout(response_layout)
            
            self.response_layout.addWidget(response_group)
            self.response_widgets[model_id] = response_text
            
       
        self.workers = []
        for model_id, model_index in selected_models:
            worker = LLMWorker(
                self.cookies.get_dict(),
                model_index,
                model_id,
                self.prompt_input.toPlainText(),
                self.length_combo.currentText()
            )
            worker.finished.connect(self.handle_response)
            self.workers.append(worker)
            worker.start()
    
    def handle_response(self, model_id, response):
        if model_id in self.response_widgets:
            self.response_widgets[model_id].setPlainText(response)
    
    def save_responses(self):
        if not self.response_widgets:
            QMessageBox.warning(self, "Warning", "No responses to save!")
            return
            
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Responses",
            f"responses_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            "Text Files (*.txt)"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(f"Prompt: {self.prompt_input.toPlainText()}\n\n")
                    for model_id, widget in self.response_widgets.items():
                        model_index = self.model_map[model_id]
                        model_name = f"Model {model_index + 1}"
                        f.write(f"=== Response from {model_name} ===\n")
                        f.write(widget.toPlainText())
                        f.write("\n\n")
                QMessageBox.information(self, "Success", "Responses saved successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save responses: {str(e)}")
                
class ResponseBox(QWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.is_expanded = False
        
        
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        
        self.text_edit = QTextEdit(text)
        self.text_edit.setReadOnly(True)
        self.text_edit.setMaximumHeight(50)  
        self.layout.addWidget(self.text_edit)

        
        self.toggle_button = QPushButton("Expand")
        self.toggle_button.clicked.connect(self.toggle_expand)
        self.layout.addWidget(self.toggle_button)

    def toggle_expand(self):
        if self.is_expanded:
            self.text_edit.setMaximumHeight(50)
            self.toggle_button.setText("Expand")
        else:
            dialog = QDialog(self)
            dialog.setWindowTitle("Full Response")
            dialog.setLayout(QVBoxLayout())
            
            full_text = QTextEdit(self.text_edit.toPlainText())
            full_text.setReadOnly(True)
            dialog.layout().addWidget(full_text)
            dialog.resize(600, 400)
            dialog.exec()


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
