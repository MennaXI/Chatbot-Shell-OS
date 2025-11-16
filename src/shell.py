import sys
import threading
import subprocess
import os
import platform
from PyQt5 import QtWidgets, QtGui, QtCore
from openai import OpenAI
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Set your OPENAI_API_KEY in environment variables")

ai_client = OpenAI(api_key=api_key)

class AIShell(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Assistant + Terminal")
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
                color: #ffffff;
            }
        """)

        container = QtWidgets.QWidget()
        self.setCentralWidget(container)
        layout = QtWidgets.QVBoxLayout(container)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)

        # Header
        header_label = QtWidgets.QLabel("AI Assistant & Terminal")
        header_label.setStyleSheet("""
            QLabel {
                color: #ff79c6;
                font-size: 24px;
                font-weight: bold;
                padding: 10px;
                background-color: #2d2d2d;
                border-radius: 8px;
            }
        """)
        header_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(header_label)

        # Create tab widget
        self.tab_widget = QtWidgets.QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #444;
                border-radius: 8px;
                background-color: #2d2d2d;
            }
            QTabBar::tab {
                background-color: #444;
                color: #fff;
                padding: 10px 20px;
                margin: 2px;
                border-radius: 5px;
            }
            QTabBar::tab:selected {
                background-color: #ff79c6;
                color: #000;
            }
        """)
        layout.addWidget(self.tab_widget)

        # AI Assistant Tab
        self.setup_ai_tab()
        
        # Terminal Tab
        self.setup_terminal_tab()

        # Progress bar
        self.progress = QtWidgets.QProgressBar()
        self.progress.setValue(0)
        self.progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid #555;
                border-radius: 8px;
                text-align: center;
                color: white;
                height: 20px;
                background-color: #2d2d2d;
            }
            QProgressBar::chunk {
                background-color: #ff79c6;
                border-radius: 6px;
            }
        """)
        layout.addWidget(self.progress)

        # Status bar
        self.status_bar = QtWidgets.QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready - Use tabs to switch between AI Assistant and Terminal")

        self.setup_signals()

    def setup_ai_tab(self):
        """Setup AI Assistant tab"""
        ai_tab = QtWidgets.QWidget()
        ai_layout = QtWidgets.QVBoxLayout(ai_tab)
        ai_layout.setSpacing(10)

        # AI description
        ai_desc = QtWidgets.QLabel("💡 Ask questions and get AI-powered responses")
        ai_desc.setStyleSheet("color: #bd93f9; font-size: 14px; padding: 5px;")
        ai_layout.addWidget(ai_desc)

        # AI Chat area
        self.ai_chat = QtWidgets.QTextEdit()
        self.ai_chat.setReadOnly(True)
        self.ai_chat.setStyleSheet("""
            QTextEdit {
                background-color: #111;
                color: #f8f8f2;
                border: 2px solid #444;
                border-radius: 8px;
                font-family: 'Consolas', monospace;
                font-size: 12px;
                padding: 10px;
            }
        """)
        ai_layout.addWidget(self.ai_chat)

        # AI Input area
        ai_input_layout = QtWidgets.QHBoxLayout()
        
        self.ai_input = QtWidgets.QLineEdit()
        self.ai_input.setPlaceholderText("Ask AI anything... (Press Enter to send)")
        self.ai_input.setStyleSheet("""
            QLineEdit {
                background-color: #222;
                color: #fff;
                border: 2px solid #444;
                border-radius: 6px;
                padding: 10px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border-color: #ff79c6;
            }
        """)
        self.ai_input.returnPressed.connect(self.send_ai_message)
        ai_input_layout.addWidget(self.ai_input)

        ai_send_btn = QtWidgets.QPushButton("Send")
        ai_send_btn.setStyleSheet("""
            QPushButton {
                background-color: #50fa7b;
                color: #000;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #69ff94;
            }
        """)
        ai_send_btn.clicked.connect(self.send_ai_message)
        ai_input_layout.addWidget(ai_send_btn)

        ai_layout.addLayout(ai_input_layout)

        self.tab_widget.addTab(ai_tab, "🤖 AI Assistant")

        # Welcome message
        self.ai_chat.append("🔮 AI Assistant ready! Ask me anything...\n")

    def setup_terminal_tab(self):
        """Setup Terminal tab"""
        terminal_tab = QtWidgets.QWidget()
        terminal_layout = QtWidgets.QVBoxLayout(terminal_tab)
        terminal_layout.setSpacing(10)

        # Terminal description
        term_desc = QtWidgets.QLabel("💻 Run Linux commands (Use with caution)")
        term_desc.setStyleSheet("color: #8be9fd; font-size: 14px; padding: 5px;")
        terminal_layout.addWidget(term_desc)

        # Terminal output
        self.terminal_output = QtWidgets.QTextEdit()
        self.terminal_output.setReadOnly(True)
        self.terminal_output.setStyleSheet("""
            QTextEdit {
                background-color: #000;
                color: #00ff00;
                border: 2px solid #444;
                border-radius: 8px;
                font-family: 'Consolas', monospace;
                font-size: 12px;
                padding: 10px;
            }
        """)
        terminal_layout.addWidget(self.terminal_output)

        # Terminal input area
        term_input_layout = QtWidgets.QHBoxLayout()
        
        self.terminal_input = QtWidgets.QLineEdit()
        self.terminal_input.setPlaceholderText("Enter Linux command... (Press Enter to execute)")
        self.terminal_input.setStyleSheet("""
            QLineEdit {
                background-color: #000;
                color: #00ff00;
                border: 2px solid #444;
                border-radius: 6px;
                padding: 10px;
                font-family: 'Consolas', monospace;
                font-size: 12px;
            }
            QLineEdit:focus {
                border-color: #ff5555;
            }
        """)
        self.terminal_input.returnPressed.connect(self.execute_terminal_command)
        term_input_layout.addWidget(self.terminal_input)

        term_exec_btn = QtWidgets.QPushButton("Execute")
        term_exec_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff5555;
                color: #000;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ff7979;
            }
        """)
        term_exec_btn.clicked.connect(self.execute_terminal_command)
        term_input_layout.addWidget(term_exec_btn)

        terminal_layout.addLayout(term_input_layout)

        # Terminal buttons
        term_btn_layout = QtWidgets.QHBoxLayout()
        
        clear_term_btn = QtWidgets.QPushButton("Clear Terminal")
        clear_term_btn.setStyleSheet("""
            QPushButton {
                background-color: #6272a4;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #7284b8;
            }
        """)
        clear_term_btn.clicked.connect(lambda: self.terminal_output.clear())
        term_btn_layout.addWidget(clear_term_btn)

        common_cmd_btn = QtWidgets.QPushButton("Common Commands")
        common_cmd_btn.setStyleSheet("""
            QPushButton {
                background-color: #bd93f9;
                color: #000;
                border: none;
                border-radius: 6px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #d6b6ff;
            }
        """)
        common_cmd_btn.clicked.connect(self.show_common_commands)
        term_btn_layout.addWidget(common_cmd_btn)

        terminal_layout.addLayout(term_btn_layout)

        self.tab_widget.addTab(terminal_tab, "💻 Terminal")

        # Welcome message with system info
        system_info = platform.system()
        self.terminal_output.append(f"🚀 Terminal ready - {system_info}\n")
        self.terminal_output.append("💡 Type 'help' for common commands\n")

    def send_ai_message(self):
        """Handle AI message sending"""
        question = self.ai_input.text().strip()
        if not question:
            return

        self.ai_chat.append(f"\n👤 You: {question}")
        self.ai_input.clear()
        self.update_progress_signal.emit(20)

        threading.Thread(target=self.get_ai_response, args=(question,), daemon=True).start()

    def get_ai_response(self, question):
        """Get response from AI in thread"""
        try:
            self.append_ai_signal.emit("\n🤖 AI: Thinking...")
            
            response = ai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": question}],
                timeout=30
            )
            
            answer = response.choices[0].message.content
            self.update_progress_signal.emit(100)
            self.append_ai_signal.emit(f"🤖 AI: {answer}\n")
            
        except Exception as e:
            self.append_ai_signal.emit(f"❌ AI Error: {str(e)}\n")
            self.update_progress_signal.emit(0)

    def execute_terminal_command(self):
        """Handle terminal command execution"""
        command = self.terminal_input.text().strip()
        if not command:
            return

        if command.lower() == 'help':
            self.show_common_commands()
            return

        self.terminal_output.append(f"\n$ {command}")
        self.terminal_input.clear()
        self.update_progress_signal.emit(20)

        threading.Thread(target=self.run_terminal_command, args=(command,), daemon=True).start()

    def run_terminal_command(self, command):
        """Run terminal command in thread"""
        try:
            # Update status
            self.update_status_signal.emit(f"Executing: {command}")
            
            # Execute command
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True, 
                timeout=30
            )
            
            self.update_progress_signal.emit(80)
            
            # Display results
            if result.stdout:
                self.append_terminal_signal.emit(result.stdout)
            if result.stderr:
                self.append_terminal_signal.emit(f"\033[91m{result.stderr}\033[0m")  # Red color for errors
            
            self.update_progress_signal.emit(100)
            self.update_status_signal.emit(f"Command completed - Return code: {result.returncode}")
            
        except subprocess.TimeoutExpired:
            self.append_terminal_signal.emit("\033[91m❌ Command timed out (30 seconds)\033[0m\n")
            self.update_progress_signal.emit(0)
            self.update_status_signal.emit("Command timed out")
        except Exception as e:
            self.append_terminal_signal.emit(f"\033[91m❌ Error: {str(e)}\033[0m\n")
            self.update_progress_signal.emit(0)
            self.update_status_signal.emit("Command failed")

    def show_common_commands(self):
        """Show common Linux commands"""
        commands = """
📋 Common Linux Commands:

📁 File Operations:
  ls -l              List files with details
  pwd                Show current directory
  cd <dir>           Change directory
  cp <src> <dest>    Copy files
  mv <src> <dest>    Move files
  rm <file>          Remove files

📊 System Info:
  whoami             Show current user
  uname -a           System information
  df -h              Disk space
  free -h            Memory usage
  top                Process monitor

🔍 Search & Text:
  grep <pattern>     Search text
  find <dir> -name   Find files
  cat <file>         Show file content
  head/tail <file>   Show file start/end

🌐 Network:
  ping <host>        Test connectivity
  ifconfig           Network interfaces
  curl <url>         Fetch URL content

⚠️  Be careful with rm -rf and sudo commands!
"""
        self.terminal_output.append(commands)

    # Signals for thread-safe operations
    append_ai_signal = QtCore.pyqtSignal(str)
    append_terminal_signal = QtCore.pyqtSignal(str)
    update_progress_signal = QtCore.pyqtSignal(int)
    update_status_signal = QtCore.pyqtSignal(str)

    def setup_signals(self):
        """Connect signals to slots"""
        self.append_ai_signal.connect(self.ai_chat.append)
        self.append_terminal_signal.connect(self.terminal_output.append)
        self.update_progress_signal.connect(self.progress.setValue)
        self.update_status_signal.connect(self.status_bar.showMessage)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    
    # Set application style
    app.setStyle('Fusion')
    
    window = AIShell()
    window.show()
    
    sys.exit(app.exec_())
