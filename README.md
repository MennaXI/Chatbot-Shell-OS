AI Assistant + Terminal:
A Python project with a PyQt5 GUI that combines an AI assistant (powered by OpenAI) and a terminal emulator.
----------------------------------------------------------------------------------------------
chatbot_project/
├── src/                        # All project code here
│   ├── __init__.py              # Empty file to make src a package
│   ├── qtpyTerminal.py          # Terminal widget
│   └── shell.py                 # Main AI + Terminal code
├── requirements.txt             # Python dependencies
├── .env                         # Example environment variables (safe to share)
└── README.md                    # Project description

---------------------------------------------------------------------------------------------
Installation:
git clone https://github.com/MennaXI/Chatbot-Shell-OS
cd chatbot_project
-----------------------------------------------------------------------------------------------
Create a virtual environment:
python -m venv venv
-----------------------------------------------------------------------------------------------
Activate the environment in ubuntu:
source venv/bin/activate
-----------------------------------------------------------------------------------------------
Running the Project:
python src/shell.py
------------------------------------------------
Notes:
each user should create their own virtual environment.
Handle terminal commands carefully, avoid destructive commands unless necessary.
The .env file is sensitive; keep your API key secret.
----------------------
